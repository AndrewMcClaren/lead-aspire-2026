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
  POST /api/preguntar         {"pregunta": "...", "documentos": ["..."], "documentos_ids": [1]} -> respuesta verificada
                              (sin documentos_ids usa todos los documentos adjuntos de la sesión)
  GET  /api/documentos        documentos adjuntos: escudo, señales y análisis
  POST /api/documentos        {"nombre": "factura.pdf", "contenido": "<base64>"} -> lo lee, lo revisa y lo guarda
  POST /api/documentos/<id>/analizar   qué pide el documento, cada dato comprobado, y qué diría el guardián
  POST /api/documentos/<id>/proponer   envía esa solicitud a la bandeja de aprobación (y a Teams)
  POST /api/documentos/<id>/quitar
  GET  /api/ejemplos          documentos de ejemplo del caso (carpeta ejemplos/)
  GET  /api/mercados          pasos para exportar y mercados (demanda, arancel, tránsito, requisitos)
  POST /api/cotizar           {"destino": "china", "sacos": 10, "tipo": "excelso", "produccion_sacos_mes": null}
  POST /api/comprador         {"nombre": "...", "cuenta": "..."} -> conocimiento del cliente contra los datos maestros
  POST /api/ejemplos/<nombre> adjunta un documento de ejemplo
  POST /api/voz               {"texto": "..."} -> audio WAV de Azure Speech (404 si no está configurado)
  GET  /api/acciones          acciones propuestas y su estado
  POST /api/acciones          {"tipo", "detalle", "monto", "destino", "cuenta", "peticion", "solicitante"}
  POST /api/acciones/<id>     {"aprobar": true, "aprobador": "nombre"} -> la decisión de una persona
  POST /api/sesion/reiniciar  {"revisor": "nombre"} -> vuelve la sesión a "limpia" (también una detenida)
  GET  /api/bitacora          verificación de la bitácora y sus últimas entradas
  GET  /swagger.json          definición OpenAPI 2.0 para un conector de Power Platform o Copilot Studio
  POST /api/whatsapp          webhook de Twilio (formulario firmado con X-Twilio-Signature, no JSON): entrega al acopio
  GET  /api/acopio/eventos    entregas registradas (eventos EPCIS)
  GET  /api/acopio/expediente/<lote>   debida diligencia del lote para la UE (bloqueado si falta un polígono)

Defensas de la API (probadas con python -m seguridad.pentest):
  - Toda solicitud POST debe ser JSON (Content-Type: application/json) y, si el navegador manda Origin, ser del
    mismo sitio: así una página maliciosa abierta en otra pestaña no puede aprobar acciones (CSRF).
  - Cuerpo máximo de 64 KB (8 MB solo para subir un documento), tipos validados (documentos es una lista de máximo 5 textos; monto, un número >= 0).
  - Cabeceras de seguridad: CSP, sin iframes de otros sitios (clickjacking), nosniff y sin caché en la API.

Límite de uso: cada dirección puede hacer KIT_LIMITE_MINUTO solicitudes POST por minuto (60 por defecto);
la siguiente recibe 429. Frena a un script que intente miles de ataques o que gaste el crédito de Azure.
"""

import argparse
import base64
import copy
import hmac
import itertools
import json
import os
import threading
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from . import integridad, modelos, privacidad
from . import acopio, decisiones, whatsapp
from . import documentos as docmod
from . import exportar
from .aprobacion import Bandeja, cargar_maestros, cargar_politica, nueva_sesion, registrar_incidentes, revisar_accion
from .asistente import responder
from .bitacora import Bitacora, huella, proteger, verificar
from .cifras import RAIZ, Tabla, carpeta_datos
from .escudo import escudo_disponible, juez_activo, revisar_documentos
from .voz import texto_a_voz, voz_disponible

KIT = Path(__file__).resolve().parent
MAX_CUERPO = 64 * 1024
MAX_CUERPO_ARCHIVO = 8 * 1024 * 1024  # un archivo de 5 MB en base64 ocupa unos 6,7 MB
MAX_ADJUNTOS = 5
VERBO = {"pago": "Pagar", "despachar_lote": "Despachar", "cambiar_cuenta": "Cambiar la cuenta",
         "aprobar_contrato": "Aprobar el contrato", "gasto": "Aprobar el gasto"}
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


def ejemplos() -> list[str]:
    carpeta = carpeta_datos() / "ejemplos"
    if not carpeta.is_dir():
        return []
    return sorted(p.name for p in carpeta.iterdir() if p.is_file() and docmod._ext(p.name) in docmod.TIPOS)


def accion_ejemplo() -> dict | None:
    ruta = carpeta_datos() / "ejemplo_accion.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


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

    adjuntos: dict[int, dict] = {}   # documentos adjuntos de la sesión (en memoria, nunca en disco)
    ids_doc = itertools.count(1)
    revisados: dict[str, dict] = {}  # huella del texto revisado -> informe del escudo (no se paga dos veces lo mismo)

    def escudo(docs, pregunta):
        faltan = [d for d in docs if huella(d) not in revisados]
        if faltan:
            juez = None if nombre_modelo.startswith(("simulado", "ingenuo")) else modelo
            for d, inf in zip(faltan, revisar_documentos(faltan, pregunta, modelo_juez=juez)):
                revisados[huella(d)] = inf
        return [copy.deepcopy(revisados[huella(d)]) for d in docs]

    def publico(doc: dict) -> dict:
        return {k: doc[k] for k in ("id", "nombre", "tipo", "paginas", "caracteres", "bytes", "accion", "motivos", "capas",
                                    "senales", "oculto", "cabeceras", "adjuntos", "avisos", "analisis")} | {
            "huella": doc["huella"][:12], "vista": doc["texto"][:1500]}

    def adjuntar(nombre: str, crudo: bytes) -> dict:
        info = docmod.extraer(nombre, crudo)
        seud = privacidad.Seudonimos() if privacidad.activa() else None
        para_escudo = seud.ocultar(info["texto"]) if seud else info["texto"]
        inf = escudo([para_escudo], "")[0]
        doc = {**info, "id": next(ids_doc), "bytes": len(crudo), "huella": docmod.huella(crudo),
               "caracteres": len(info["texto"]), "accion": inf["accion"], "motivos": inf["motivos"], "capas": inf["capas"],
               "senales": docmod.senales(info, cargar_maestros()), "analisis": None}
        adjuntos[doc["id"]] = doc
        if registrar_incidentes(sesion, 1 if inf["accion"] in ("bloqueado", "saneado") else 0):
            bitacora.registrar("sesion_detenida", {"incidentes": sesion["incidentes"]})
        bitacora.registrar("documento_recibido", {
            "nombre": doc["nombre"], "tipo": doc["tipo"], "bytes": doc["bytes"], "huella": doc["huella"],
            "accion": doc["accion"], "motivos": doc["motivos"], "texto_oculto": bool(doc["oculto"]),
            "senales": [x["tipo"] for x in doc["senales"] if x["nivel"] != "info"]})
        return doc

    def analizar_doc(doc: dict) -> dict:
        maestros = cargar_maestros()
        bloqueado = doc["accion"] == "bloqueado"
        seud = privacidad.Seudonimos() if privacidad.activa() and not bloqueado else None
        # Un documento bloqueado por el escudo no llega al modelo: se analiza solo con reglas, en este computador.
        if bloqueado:
            texto = doc["texto"]
        else:
            revisado = escudo([seud.ocultar(doc["texto"]) if seud else doc["texto"]], "")[0]
            texto = revisado["texto"]
        a = docmod.analizar(texto, maestros, None if bloqueado else modelo,
                            original=seud.ocultar(doc["texto"]) if seud else doc["texto"])
        if a["tipo_documento"] == "documento":  # sin IA no se sabe qué es: se usa el tipo de archivo
            a["tipo_documento"] = doc["tipo"]
        if seud:
            for k in ("destino", "cuenta", "lote", "cita"):
                a["solicitud"][k] = seud.restaurar(a["solicitud"][k])
        s = a["solicitud"]
        if s["tipo"] != "ninguna":
            estado, motivos = revisar_accion(s["tipo"], s["monto"], s["destino"], s["cuenta"],
                                             f"{VERBO.get(s['tipo'], s['tipo'])} según el documento {doc['nombre']}",
                                             sesion["estado"], maestros=maestros, lote=s["lote"])
            a["guardian"] = {"estado": estado, "motivos": motivos}
        else:
            a["guardian"] = None
        doc["analisis"] = a
        bitacora.registrar("documento_analizado", {"huella": doc["huella"], "solicitud": s["tipo"], "origen": a["origen"],
                                                   "comprobados": a["comprobados"], "descartes": len(a["descartes"]),
                                                   "guardian": (a["guardian"] or {}).get("estado")})
        return a

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
            if n > (MAX_CUERPO_ARCHIVO if self.path == "/api/documentos" else MAX_CUERPO):
                raise ValueError("cuerpo demasiado grande")
            datos = json.loads(self.rfile.read(n) or b"{}") if n else {}
            if not isinstance(datos, dict):
                raise ValueError("el cuerpo debe ser un objeto JSON")
            return datos

        def _descartar_cuerpo(self):
            """Antes de rechazar, lee el cuerpo pequeño que nadie va a usar. Si se cierra la conexión con datos sin
            leer, Windows corta con un reinicio y el cliente no alcanza a ver el 401, 403 o 429 (ve "conexión
            abortada"). Un cuerpo grande no se lee: se cierra la conexión."""
            try:
                n = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                n = -1
            if 0 < n <= MAX_CUERPO:
                self.rfile.read(n)
            elif n:
                self.close_connection = True

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
                                   "decisiones_teams": decisiones.carpeta() is not None,
                                   "documentos": {"tipos": sorted(docmod.TIPOS), "max_mb": docmod.MAX_BYTES // 1_000_000,
                                                  "maximo": MAX_ADJUNTOS},
                                   "ejemplos": ejemplos(), "accion_ejemplo": accion_ejemplo()})
            if self.path == "/api/documentos":
                return self._json([publico(d) for d in adjuntos.values()])
            if self.path == "/api/ejemplos":
                return self._json(ejemplos())
            if self.path == "/api/mercados":
                try:
                    return self._json(exportar.mercados())
                except FileNotFoundError as e:
                    return self._json({"error": str(e)}, 404)
            if self.path == "/api/acciones":
                return self._json(bandeja.lista())
            if self.path == "/api/acopio/eventos":
                return self._json(acopio.eventos()[-50:][::-1])
            if self.path.startswith("/api/acopio/expediente/"):
                try:
                    return self._json(acopio.expediente(self.path.rsplit("/", 1)[1]))
                except FileNotFoundError as e:
                    return self._json({"error": str(e)}, 404)
            if self.path == "/api/bitacora":
                ok, n, problema = verificar(bitacora.ruta)
                lineas = bitacora.ruta.read_text(encoding="utf-8").splitlines() if bitacora.ruta.exists() else []
                return self._json({"integra": ok, "entradas": n, "detalle": problema,
                                   "ultimas": [json.loads(x) for x in lineas[-8:]][::-1]})
            return self._json({"error": "no existe"}, 404)

        def _whatsapp(self):
            """Webhook de Twilio: no usa X-API-Key ni JSON; lo protege la firma de Twilio (falla cerrada)."""
            if not permitido(self.client_address[0]):
                self._descartar_cuerpo()
                return self._json({"error": "Demasiadas solicitudes"}, 429)
            try:
                n = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                n = -1
            if n < 0 or n > MAX_CUERPO:
                self.close_connection = True
                return self._json({"error": "cuerpo demasiado grande"}, 413)
            tipo = self.headers.get("Content-Type", "").split(";")[0].strip().lower()
            if tipo != "application/x-www-form-urlencoded":
                self._descartar_cuerpo()
                return self._json({"error": "Se espera el formulario de Twilio"}, 415)
            try:
                params = whatsapp.leer_formulario(self.rfile.read(n))
            except UnicodeDecodeError:
                return self._json({"error": "El formulario no es UTF-8"}, 400)
            if not whatsapp.firma_valida(whatsapp.url_publica(self.headers.get("Host", "")), params,
                                         self.headers.get("X-Twilio-Signature", "")):
                bitacora.registrar("whatsapp_rechazado", {"motivo": "firma inválida o sin TWILIO_AUTH_TOKEN"})
                return self._json({"error": "Firma de Twilio inválida"}, 403)
            guardar = None
            if os.environ.get("SNOWFLAKE_TABLA_EVENTOS"):
                from .snowflake import guardar_eventos as guardar
            whatsapp.atender_en_segundo_plano(params, modelo, bitacora, guardar)
            return self._enviar(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response></Response>", "text/xml")

        def do_POST(self):
            if self.path == whatsapp.RUTA:
                return self._whatsapp()
            if not self._autorizado():
                self._descartar_cuerpo()
                return self._json({"error": "Falta la clave de API (encabezado X-API-Key)"}, 401)
            rechazo = self._rechazo_de_origen()
            if rechazo:
                self._descartar_cuerpo()
                return self._json({"error": rechazo}, 415 if "JSON" in rechazo else 403)
            if not permitido(self.client_address[0]):
                self._descartar_cuerpo()
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
                ids = datos.get("documentos_ids")
                if ids is None:
                    ids = list(adjuntos)
                if not isinstance(ids, list) or not all(isinstance(i, int) and not isinstance(i, bool) for i in ids):
                    return self._json({"error": "documentos_ids debe ser una lista de números"}, 400)
                guardados = [adjuntos[i] for i in ids if i in adjuntos][:MAX_ADJUNTOS]
                pegados = [str(d)[:10_000] for d in documentos if str(d).strip()]
                docs = [d["texto"] for d in guardados] + pegados
                nombres = [d["nombre"] for d in guardados] + [f"texto pegado {i}" for i in range(1, len(pegados) + 1)]
                r = responder(pregunta, modelo, tabla, docs, escudo, nombres=nombres)
                # Los adjuntos ya contaron como incidente al subirlos: aquí solo cuentan los textos pegados.
                nuevos = [x for i, x in enumerate(r["documentos"]) if i >= len(guardados) and x["accion"] != "pasa"]
                if registrar_incidentes(sesion, len(nuevos)):
                    bitacora.registrar("sesion_detenida", {"incidentes": sesion["incidentes"]})
                r["sesion"] = sesion
                bitacora.registrar("pregunta", proteger({
                    "pregunta": r["pregunta_modelo"], "datos_personales": r.get("privacidad", {}).get("tipos", []),
                    "estado": r["estado"], "claves": r.get("claves", []), "capas": r.get("capas", []),
                    "problemas": r.get("problemas", []), "ms": r.get("ms"), "costo_usd": r.get("costo_usd"),
                    "documentos": [{"huella": huella(d), **inf} for d, inf in zip(docs, r["documentos"])],
                    "citas": len(r.get("citas", []))}, ("pregunta",)))
                return self._json(r)
            if self.path == "/api/documentos":
                if len(adjuntos) >= MAX_ADJUNTOS:
                    return self._json({"error": f"Máximo {MAX_ADJUNTOS} documentos por sesión: quita uno"}, 400)
                contenido = datos.get("contenido")
                if not isinstance(contenido, str):
                    return self._json({"error": "Falta el contenido del archivo (en base64)"}, 400)
                try:
                    crudo = base64.b64decode(contenido, validate=True)
                except ValueError:
                    return self._json({"error": "El contenido debe ir en base64"}, 400)
                try:
                    return self._json(publico(adjuntar(str(datos.get("nombre") or "documento.txt"), crudo)), 201)
                except docmod.DocumentoInvalido as e:
                    bitacora.registrar("documento_rechazado", {"nombre": str(datos.get("nombre"))[:120], "motivo": str(e)})
                    return self._json({"error": str(e)}, 400)
            if self.path == "/api/cotizar":
                sacos, prod = datos.get("sacos"), datos.get("produccion_sacos_mes")
                try:
                    sacos = float(sacos)
                    prod = float(prod) if prod not in (None, "") else None
                    r = exportar.cotizar(str(datos.get("destino", "")), sacos, str(datos.get("tipo", "excelso")), prod, tabla)
                except (TypeError, ValueError, FileNotFoundError) as e:
                    return self._json({"error": str(e)}, 400)
                bitacora.registrar("cotizacion", {"destino": r["destino"], "sacos": r["sacos"], "total_usd": r["total_usd"],
                                                  "alertas": [a["nivel"] for a in r["alertas"]]})
                return self._json(r)
            if self.path == "/api/comprador":
                nombre = str(datos.get("nombre", "")).strip()[:120]
                if not nombre:
                    return self._json({"error": "Falta el nombre del comprador"}, 400)
                r = exportar.conocer_comprador(nombre, str(datos.get("cuenta", ""))[:120])
                bitacora.registrar("conocimiento_cliente", proteger({"nombre": nombre, "estado": r["estado"]}, ()))
                return self._json(r)
            if self.path.startswith("/api/ejemplos/"):
                nombre = self.path.rsplit("/", 1)[1]
                from urllib.parse import unquote
                nombre = unquote(nombre)
                if nombre not in ejemplos():  # solo los de la carpeta: nada de rutas arbitrarias
                    return self._json({"error": "no existe"}, 404)
                if len(adjuntos) >= MAX_ADJUNTOS:
                    return self._json({"error": f"Máximo {MAX_ADJUNTOS} documentos por sesión: quita uno"}, 400)
                try:
                    return self._json(publico(adjuntar(nombre, (carpeta_datos() / "ejemplos" / nombre).read_bytes())), 201)
                except docmod.DocumentoInvalido as e:
                    return self._json({"error": str(e)}, 400)
            if self.path.startswith("/api/documentos/"):
                partes = self.path.split("/")
                if len(partes) != 5 or not partes[3].isdigit() or int(partes[3]) not in adjuntos:
                    return self._json({"error": "no existe"}, 404)
                doc, orden = adjuntos[int(partes[3])], partes[4]
                if orden == "quitar":
                    adjuntos.pop(doc["id"])
                    bitacora.registrar("documento_quitado", {"huella": doc["huella"]})
                    return self._json({"id": doc["id"], "quitado": True})
                if orden == "analizar":
                    analizar_doc(doc)
                    return self._json(publico(doc))
                if orden == "proponer":
                    a = doc["analisis"] or analizar_doc(doc)
                    s = a["solicitud"]
                    if s["tipo"] == "ninguna":
                        return self._json({"error": "El documento no pide ninguna acción"}, 400)
                    accion = bandeja.proponer(s["tipo"], f"{a['tipo_documento'][:1].upper()}{a['tipo_documento'][1:]}: "
                                              f"{doc['nombre']}"[:300], s["monto"],
                                              s["destino"], s["cuenta"],
                                              f"{VERBO.get(s['tipo'], s['tipo'])} según el documento {doc['nombre']}",
                                              "asistente", sesion["estado"], lote=s["lote"],
                                              documento=f"{doc['nombre']} (huella {doc['huella'][:12]})")
                    return self._json(accion.publica(), 201)
                return self._json({"error": "no existe"}, 404)
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
                                     sesion["estado"], lote=str(datos.get("lote", ""))[:40])
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
                adjuntos.clear()  # una sesión nueva empieza sin documentos
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
