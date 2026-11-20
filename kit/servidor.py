"""Servidor local de la demo: la página del asistente y una API pequeña. Solo usa la librería estándar.

Uso (desde la raíz del repo):
  python -m kit.servidor                          # modelo simulado, sin claves ni internet
  python -m kit.servidor --modelo azure:<deployment>
  python -m kit.servidor --modelo ollama:qwen2.5:7b
Luego abre http://localhost:8000 en Chrome o Edge.

Rutas:
  GET  /                      la página (web/index.html)
  GET  /api/estado            modelo, voz, escudo y preguntas sugeridas
  POST /api/preguntar         {"pregunta": "...", "documentos": ["..."]} -> respuesta verificada
  POST /api/voz               {"texto": "..."} -> audio WAV de Azure Speech (404 si no está configurado)
  GET  /api/acciones          acciones propuestas y su estado
  POST /api/acciones          {"tipo": "pago", "detalle": "...", "monto": 1500000} -> la política decide
  POST /api/acciones/<id>     {"aprobar": true} -> la decisión de la persona
"""

import argparse
import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import modelos
from .aprobacion import Bandeja
from .asistente import responder
from .cifras import Tabla
from .escudo import escudo_cerrado, escudo_disponible
from .voz import texto_a_voz, voz_disponible

WEB = Path(__file__).resolve().parent / "web"
# Cámbialas por las del caso del cliente. Deja siempre una sin dato: mostrar que dice "no sé" genera confianza.
SUGERIDAS = ["¿Cuánto vendió la cadena el último año?", "¿Qué porcentaje de las compras hechas por asistentes de IA se devuelve?",
             "¿Cuántas facturas de proveedores llegan al mes?", "¿Cuántos intentos de fraude por cambio de cuenta hubo?",
             "¿Cuánto vendió la tienda de Medellín?"]


def crear_app(nombre_modelo: str = "simulado"):
    tabla = Tabla()
    modelo = modelos.crear(nombre_modelo, tabla)
    bandeja = Bandeja()

    class Manejador(BaseHTTPRequestHandler):
        def _json(self, datos, codigo=200):
            cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)

        def _leer(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(n) or b"{}") if n else {}

        def log_message(self, *a):
            pass

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                cuerpo = (WEB / "index.html").read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(cuerpo)))
                self.end_headers()
                self.wfile.write(cuerpo)
            elif self.path == "/api/estado":
                self._json({"modelo": getattr(modelo, "nombre", nombre_modelo), "voz": voz_disponible(),
                            "escudo": escudo_disponible(), "sugeridas": SUGERIDAS, "cifras": len(tabla.cifras)})
            elif self.path == "/api/acciones":
                self._json(bandeja.lista())
            else:
                self._json({"error": "no existe"}, 404)

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
                escudo = escudo_cerrado if (docs and escudo_disponible()) else None
                r = responder(pregunta, modelo, tabla, docs, escudo)
                r["escudo_activo"] = escudo is not None
                return self._json(r)
            if self.path == "/api/voz":
                if not voz_disponible():
                    return self._json({"error": "Azure Speech no está configurado"}, 404)
                audio = texto_a_voz(str(datos.get("texto", ""))[:1000])
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(len(audio)))
                self.end_headers()
                self.wfile.write(audio)
                return None
            if self.path == "/api/acciones":
                monto = datos.get("monto")
                a = bandeja.proponer(str(datos.get("tipo", "otra")), str(datos.get("detalle", ""))[:300],
                                     float(monto) if monto not in (None, "") else None)
                return self._json(asdict(a), 201)
            if self.path.startswith("/api/acciones/"):
                try:
                    a = bandeja.decidir(int(self.path.rsplit("/", 1)[1]), bool(datos.get("aprobar")))
                    return self._json({"id": a.id, "estado": a.estado})
                except (KeyError, ValueError) as e:
                    return self._json({"error": str(e)}, 400)
            return self._json({"error": "no existe"}, 404)

    return Manejador


def main():
    from . import cargar_env
    cargar_env()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelo", default="simulado", help="simulado | azure:<deployment> | ollama:<modelo>")
    p.add_argument("--puerto", type=int, default=8000)
    p.add_argument("--host", default="127.0.0.1", help="127.0.0.1 = solo este computador")
    a = p.parse_args()
    servidor = ThreadingHTTPServer((a.host, a.puerto), crear_app(a.modelo))
    print(f"Demo lista en http://localhost:{a.puerto}  (modelo: {a.modelo} · voz Azure: {voz_disponible()} · "
          f"escudo: {escudo_disponible()})  Ctrl+C para salir.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
