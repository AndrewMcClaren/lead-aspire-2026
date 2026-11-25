"""Servidor local de la demo: la página del asistente y una API pequeña. Solo usa la librería estándar.

Uso (desde la raíz del repo):
  python -m kit.servidor                          # modelo simulado, sin claves ni internet
  python -m kit.servidor --modelo azure:<deployment>
  python -m kit.servidor --modelo ollama:qwen2.5:7b
  KIT_DATOS=respaldo/dane python -m kit.servidor  # otro caso (otra carpeta de datos)
Luego abre http://localhost:8000 en Chrome o Edge.

Rutas:
  GET  /                      la página (web/index.html)
  GET  /api/estado            modelo, capas activas, sesión, preguntas sugeridas
  POST /api/preguntar         {"pregunta": "...", "documentos": ["..."]} -> respuesta verificada
  POST /api/voz               {"texto": "..."} -> audio WAV de Azure Speech (404 si no está configurado)
  GET  /api/acciones          acciones propuestas y su estado
  POST /api/acciones          {"tipo", "detalle", "monto", "destino", "cuenta", "peticion", "solicitante"}
  POST /api/acciones/<id>     {"aprobar": true, "aprobador": "nombre"} -> la decisión de una persona
  POST /api/sesion/reiniciar  {"revisor": "nombre"} -> vuelve la sesión a "limpia" (también una detenida)
  GET  /api/bitacora          verificación de la bitácora y sus últimas entradas
  GET  /swagger.json          definición OpenAPI 2.0 para un conector de Power Platform o Copilot Studio

Defensas de la API (probadas con python -m seguridad.pentest):
  - Toda solicitud POST debe ser JSON (Content-Type: application/json) y, si el navegador manda Origin, ser del
    mismo sitio: así una página maliciosa abierta en otra pestaña no puede aprobar acciones (CSRF).
  - Cuerpo máximo de 64 KB, tipos validados (documentos es una lista de máximo 5 textos; monto, un número >= 0).
  - Cabeceras de seguridad: CSP, sin iframes de otros sitios (clickjacking), nosniff y sin caché en la API.

Límite de uso: cada dirección puede hacer KIT_LIMITE_MINUTO solicitudes POST por minuto (60 por defecto);
la siguiente recibe 429. Frena a un script que intente miles de ataques o que gaste el crédito de Azure.
"""

import argparse
import hmac
import json
import os
import threading
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from . import integridad, modelos, privacidad
from . import decisiones
from .aprobacion import Bandeja, cargar_politica, nueva_sesion, registrar_incidentes
from .asistente import responder
from .bitacora import Bitacora, huella, proteger, verificar
from .cifras import RAIZ, Tabla, carpeta_datos
from .escudo import escudo_disponible, juez_activo, revisar_documentos
from .voz import texto_a_voz, voz_disponible

KIT = Path(__file__).resolve().parent
MAX_CUERPO = 64 * 1024
CABECERAS_SEGURIDAD = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
                               "img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'; "
                               "base-uri 'none'; form-action 'self'",
}
WEB = KIT / "web"
# Cámbialas por las del caso del cliente (o pon un sugeridas.json en la carpeta del caso).
# Deja siempre una sin dato: mostrar que dice "no sé" genera confianza.
SUGERIDAS = ["¿Cuánto vendió la cadena el último año?", "¿Qué porcentaje de las compras hechas por asistentes de IA se devuelve?",
             "¿Cuántas facturas de proveedores llegan al mes?", "¿Cuántos intentos de fraude por cambio de cuenta hubo?",
             "¿Cuánto vendió la tienda de Medellín?"]


def nombre_caso() -> str:
    try:
        return carpeta_datos().resolve().relative_to(RAIZ.resolve()).as_posix()
    except ValueError:
        return carpeta_datos().name


def sugeridas() -> list[str]:
    ruta = carpeta_datos() / "sugeridas.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else SUGERIDAS


def crear_app(nombre_modelo: str = "simulado", bitacora: Bitacora | None = None):
    tabla = Tabla()
    modelo = modelos.crear(nombre_modelo, tabla)
    bitacora = bitacora or Bitacora()
    bandeja = Bandeja(bitacora)
    decisiones.vigilar(bandeja, bitacora)  # decisiones tomadas en Teams que llegan por OneDrive (si KIT_DECISIONES)
    sesion = nueva_sesion()
    limite = int(os.environ.get("KIT_LIMITE_MINUTO", "60") or 0)
    recientes: dict[str, deque] = defaultdict(deque)
    candado = threading.Lock()

    def permitido(cliente: str) -> bool:
        """Ventana deslizante de 60 segundos por dirección. KIT_LIMITE_MINUTO=0 lo desactiva."""
        if limite <= 0:
            return True
        ahora = time.monotonic()
        with candado:
            cola = recientes[cliente]
            while cola and ahora - cola[0] > 60:
                cola.popleft()
            if len(cola) >= limite:
                return False
            cola.append(ahora)
            return True

    def escudo(docs, pregunta):
        return revisar_documentos(docs, pregunta, modelo_juez=None if nombre_modelo.startswith(("simulado", "ingenuo")) else modelo)

    class Manejador(BaseHTTPRequestHandler):
        timeout = 30  # cierra conexiones que no envían nada (ataque slowloris)
        def _enviar(self, cuerpo: bytes, tipo: str, codigo: int = 200):
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            for k, v in CABECERAS_SEGURIDAD.items():
                self.send_header(k, v)
            if self.path.startswith("/api/"):
                self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)

        def _json(self, datos, codigo=200):
            self._enviar(json.dumps(datos, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", codigo)

        def _leer(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_CUERPO:
                raise ValueError("cuerpo demasiado grande")
            datos = json.loads(self.rfile.read(n) or b"{}") if n else {}
            if not isinstance(datos, dict):
                raise ValueError("el cuerpo debe ser un objeto JSON")
            return datos

        def _rechazo_de_origen(self) -> str | None:
            """CSRF: exige JSON (un formulario de otro sitio no puede mandarlo sin permiso del navegador) y, si hay
            Origin, que sea este mismo servidor."""
            if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                return "Las solicitudes deben ser JSON (Content-Type: application/json)"
            origen = self.headers.get("Origin")
            if origen and origen != "null" and urlparse(origen).netloc != self.headers.get("Host", ""):
                return "Origen no permitido"
            if origen == "null":
                return "Origen no permitido"
            return None

        def log_message(self, *a):
            pass

        def _autorizado(self) -> bool:
            """Con KIT_API_KEY definida, toda ruta /api/ exige el encabezado X-API-Key con esa clave."""
            clave = os.environ.get("KIT_API_KEY", "")
            if not clave or not self.path.startswith("/api/"):
                return True
            return hmac.compare_digest(self.headers.get("X-API-Key", ""), clave)

        def do_GET(self):
            if not self._autorizado():
                return self._json({"error": "Falta la clave de API (encabezado X-API-Key)"}, 401)
            if self.path in ("/", "/index.html"):
                return self._enviar((WEB / "index.html").read_bytes(), "text/html; charset=utf-8")
            if self.path == "/swagger.json":
                definicion = json.loads((KIT / "conector" / "swagger.json").read_text(encoding="utf-8"))
                definicion["host"] = self.headers.get("Host", definicion.get("host"))
                return self._json(definicion)
            if self.path == "/api/estado":
                return self._json({"modelo": getattr(modelo, "nombre", nombre_modelo), "voz": voz_disponible(),
                                   "escudo": {"firmas": True, "prompt_shields": escudo_disponible(), "juez": juez_activo()},
                                   "sugeridas": sugeridas(), "cifras": len(tabla.cifras), "caso": nombre_caso(),
                                   "sesion": sesion, "autonomia": cargar_politica()["nivel_autonomia"],
                                   "tipos_accion": cargar_politica()["tipos_sensibles"] + cargar_politica()["tipos_solo_lectura"],
                                   "datos_personales": privacidad.activa(), "integridad": integridad.revisar()["estado"],
                                   "limite_minuto": limite, "teams": bool(os.environ.get("NOTIFICAR_URL")),
                                   "decisiones_teams": decisiones.carpeta() is not None})
            if self.path == "/api/acciones":
                return self._json(bandeja.lista())
            if self.path == "/api/bitacora":
                ok, n, problema = verificar(bitacora.ruta)
                lineas = bitacora.ruta.read_text(encoding="utf-8").splitlines() if bitacora.ruta.exists() else []
                return self._json({"integra": ok, "entradas": n, "detalle": problema,
                                   "ultimas": [json.loads(x) for x in lineas[-8:]][::-1]})
            return self._json({"error": "no existe"}, 404)

        def do_POST(self):
            if not self._autorizado():
                return self._json({"error": "Falta la clave de API (encabezado X-API-Key)"}, 401)
            rechazo = self._rechazo_de_origen()
            if rechazo:
                return self._json({"error": rechazo}, 415 if "JSON" in rechazo else 403)
            if not permitido(self.client_address[0]):
                bitacora.registrar("limite_excedido", {"ruta": self.path})
                return self._json({"error": f"Demasiadas solicitudes: máximo {limite} por minuto"}, 429)
            try:
                datos = self._leer()
            except json.JSONDecodeError:
                return self._json({"error": "JSON inválido"}, 400)
            except ValueError as e:
                return self._json({"error": str(e)}, 413 if "grande" in str(e) else 400)
            if self.path == "/api/preguntar":
                pregunta = str(datos.get("pregunta", "")).strip()[:500]
                if not pregunta:
                    return self._json({"error": "Falta la pregunta"}, 400)
                documentos = datos.get("documentos") or []
                if not isinstance(documentos, list) or len(documentos) > 5:
                    return self._json({"error": "documentos debe ser una lista de máximo 5 textos"}, 400)
                docs = [str(d)[:10_000] for d in documentos if str(d).strip()]
                r = responder(pregunta, modelo, tabla, docs, escudo)
                if registrar_incidentes(sesion, len(r["bloqueados"]) + len(r["saneados"])):
                    bitacora.registrar("sesion_detenida", {"incidentes": sesion["incidentes"]})
                r["sesion"] = sesion
                bitacora.registrar("pregunta", proteger({
                    "pregunta": r["pregunta_modelo"], "datos_personales": r.get("privacidad", {}).get("tipos", []),
                    "estado": r["estado"], "claves": r.get("claves", []), "capas": r.get("capas", []),
                    "problemas": r.get("problemas", []), "ms": r.get("ms"), "costo_usd": r.get("costo_usd"),
                    "documentos": [{"huella": huella(d), **inf} for d, inf in zip(docs, r["documentos"])]}, ("pregunta",)))
                return self._json(r)
            if self.path == "/api/voz":
                if not voz_disponible():
                    return self._json({"error": "Azure Speech no está configurado"}, 404)
                return self._enviar(texto_a_voz(str(datos.get("texto", ""))[:1000]), "audio/wav")
            if self.path == "/api/acciones":
                monto = datos.get("monto")
                try:
                    if isinstance(monto, (int, float)) and not isinstance(monto, bool):
                        monto = float(monto)
                    else:
                        monto = float(str(monto).replace(".", "").replace(",", ".")) if monto not in (None, "") else None
                except ValueError:
                    return self._json({"error": "El monto no es un número"}, 400)
                a = bandeja.proponer(str(datos.get("tipo", "otra")), str(datos.get("detalle", ""))[:300], monto,
                                     str(datos.get("destino", ""))[:120], str(datos.get("cuenta", ""))[:120],
                                     str(datos.get("peticion", ""))[:300], str(datos.get("solicitante", "asistente"))[:60],
                                     sesion["estado"])
                return self._json(a.publica(), 201)
            if self.path.startswith("/api/acciones/"):
                try:
                    if not isinstance(datos.get("aprobar"), bool):
                        return self._json({"error": "aprobar debe ser true o false"}, 400)
                    a = bandeja.decidir(int(self.path.rsplit("/", 1)[1]), datos["aprobar"],
                                        str(datos.get("aprobador", "persona"))[:60])
                    return self._json({"id": a.id, "estado": a.estado, "decidida_por": a.decidida_por})
                except (KeyError, ValueError) as e:
                    return self._json({"error": str(e).strip("'")}, 400)
            if self.path == "/api/sesion/reiniciar":
                revisor = str(datos.get("revisor") or "persona")[:60]
                bitacora.registrar("sesion_reiniciada", {"revisor": revisor, "estado_anterior": sesion["estado"],
                                                         "incidentes": sesion["incidentes"]})
                sesion.clear()
                sesion.update(nueva_sesion())
                return self._json(sesion)
            return self._json({"error": "no existe"}, 404)

    return Manejador


def main():
    from . import cargar_env
    cargar_env()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelo", default="simulado", help="simulado | ingenuo | azure:<deployment> | ollama:<modelo>")
    p.add_argument("--puerto", type=int, default=int(os.environ.get("PORT", "8000")), help="por defecto 8000 o la variable PORT")
    p.add_argument("--host", default=os.environ.get("KIT_HOST", "127.0.0.1"),
                   help="127.0.0.1 = solo este computador; 0.0.0.0 en un servidor (por ejemplo Azure App Service)")
    a = p.parse_args()
    if a.host != "127.0.0.1" and not os.environ.get("KIT_API_KEY"):
        print("Aviso: el servidor queda abierto a la red sin KIT_API_KEY. Definan una clave antes de exponerlo.")
    revision = integridad.revisar()
    if revision["estado"] != "integra":
        print(f"Aviso de integridad de los datos: {integridad.describir(revision)}.")
    bitacora = Bitacora()
    # Inventario mínimo del sistema de IA: qué modelo, qué caso, qué capas y qué versión de los datos.
    bitacora.registrar("inicio", {"modelo": a.modelo, "caso": nombre_caso(), "datos": integridad.huellas(),
                                  "integridad": revision["estado"], "datos_personales": privacidad.activa(),
                                  "prompt_shields": escudo_disponible(), "juez": juez_activo()})
    servidor = ThreadingHTTPServer((a.host, a.puerto), crear_app(a.modelo, bitacora))
    print(f"Demo lista en http://localhost:{a.puerto}  (caso: {nombre_caso()} · modelo: {a.modelo} · "
          f"voz Azure: {voz_disponible()} · Prompt Shields: {escudo_disponible()} · juez: {juez_activo()})  Ctrl+C para salir.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
