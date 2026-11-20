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
  POST /api/sesion/reiniciar  vuelve la sesión a "limpia"
  GET  /api/bitacora          verificación de la bitácora y sus últimas entradas
  GET  /swagger.json          definición OpenAPI 2.0 para un conector de Power Platform o Copilot Studio
"""

import argparse
import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import modelos
from .aprobacion import Bandeja, cargar_politica
from .asistente import responder
from .bitacora import Bitacora, huella, verificar
from .cifras import RAIZ, Tabla, carpeta_datos
from .escudo import escudo_disponible, juez_activo, revisar_documentos
from .voz import texto_a_voz, voz_disponible

KIT = Path(__file__).resolve().parent
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
    sesion = {"estado": "limpia", "motivos": []}

    def escudo(docs, pregunta):
        return revisar_documentos(docs, pregunta, modelo_juez=None if nombre_modelo.startswith(("simulado", "ingenuo")) else modelo)

    class Manejador(BaseHTTPRequestHandler):
        def _enviar(self, cuerpo: bytes, tipo: str, codigo: int = 200):
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)

        def _json(self, datos, codigo=200):
            self._enviar(json.dumps(datos, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", codigo)

        def _leer(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(n) or b"{}") if n else {}

        def log_message(self, *a):
            pass

        def do_GET(self):
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
                                   "sesion": sesion, "autonomia": cargar_politica()["nivel_autonomia"]})
            if self.path == "/api/acciones":
                return self._json(bandeja.lista())
            if self.path == "/api/bitacora":
                ok, n, problema = verificar(bitacora.ruta)
                lineas = bitacora.ruta.read_text(encoding="utf-8").splitlines() if bitacora.ruta.exists() else []
                return self._json({"integra": ok, "entradas": n, "detalle": problema,
                                   "ultimas": [json.loads(x) for x in lineas[-8:]][::-1]})
            return self._json({"error": "no existe"}, 404)

        def do_POST(self):
            try:
                datos = self._leer()
            except json.JSONDecodeError:
                return self._json({"error": "JSON inválido"}, 400)
            if self.path == "/api/preguntar":
                pregunta = str(datos.get("pregunta", "")).strip()[:500]
                if not pregunta:
                    return self._json({"error": "Falta la pregunta"}, 400)
                docs = [str(d)[:10_000] for d in datos.get("documentos") or [] if str(d).strip()]
                r = responder(pregunta, modelo, tabla, docs, escudo)
                if r["sospechosa"] and sesion["estado"] == "limpia":
                    sesion.update(estado="sospechosa", motivos=sesion["motivos"] + ["Documento con instrucciones escondidas"])
                r["sesion"] = sesion
                bitacora.registrar("pregunta", {"pregunta": pregunta, "estado": r["estado"], "claves": r.get("claves", []),
                                                "capas": r.get("capas", []), "problemas": r.get("problemas", []),
                                                "documentos": [{"huella": huella(d), **inf} for d, inf in zip(docs, r["documentos"])],
                                                "ms": r.get("ms"), "costo_usd": r.get("costo_usd")})
                return self._json(r)
            if self.path == "/api/voz":
                if not voz_disponible():
                    return self._json({"error": "Azure Speech no está configurado"}, 404)
                return self._enviar(texto_a_voz(str(datos.get("texto", ""))[:1000]), "audio/wav")
            if self.path == "/api/acciones":
                monto = datos.get("monto")
                try:
                    monto = float(str(monto).replace(".", "").replace(",", ".")) if monto not in (None, "") else None
                except ValueError:
                    return self._json({"error": "El monto no es un número"}, 400)
                a = bandeja.proponer(str(datos.get("tipo", "otra")), str(datos.get("detalle", ""))[:300], monto,
                                     str(datos.get("destino", ""))[:120], str(datos.get("cuenta", ""))[:120],
                                     str(datos.get("peticion", ""))[:300], str(datos.get("solicitante", "asistente"))[:60],
                                     sesion["estado"])
                return self._json({**asdict(a), "motivo": a.motivo}, 201)
            if self.path.startswith("/api/acciones/"):
                try:
                    a = bandeja.decidir(int(self.path.rsplit("/", 1)[1]), bool(datos.get("aprobar")),
                                        str(datos.get("aprobador", "persona"))[:60])
                    return self._json({"id": a.id, "estado": a.estado, "decidida_por": a.decidida_por})
                except (KeyError, ValueError) as e:
                    return self._json({"error": str(e).strip("'")}, 400)
            if self.path == "/api/sesion/reiniciar":
                sesion.update(estado="limpia", motivos=[])
                bitacora.registrar("sesion_reiniciada", {})
                return self._json(sesion)
            return self._json({"error": "no existe"}, 404)

    return Manejador


def main():
    from . import cargar_env
    cargar_env()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelo", default="simulado", help="simulado | ingenuo | azure:<deployment> | ollama:<modelo>")
    p.add_argument("--puerto", type=int, default=8000)
    p.add_argument("--host", default="127.0.0.1", help="127.0.0.1 = solo este computador")
    a = p.parse_args()
    servidor = ThreadingHTTPServer((a.host, a.puerto), crear_app(a.modelo))
    print(f"Demo lista en http://localhost:{a.puerto}  (caso: {nombre_caso()} · modelo: {a.modelo} · "
          f"voz Azure: {voz_disponible()} · Prompt Shields: {escudo_disponible()} · juez: {juez_activo()})  Ctrl+C para salir.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
