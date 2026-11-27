"""WhatsApp con Twilio: el caficultor manda texto o una nota de voz y el acopio queda registrado.

Flujo (la IA propone, el código verifica):
  Twilio → POST /api/whatsapp (formulario firmado) → el servidor responde de inmediato (Twilio espera máx. 15 s)
  → en segundo plano: descarga la nota de voz → Azure AI Speech la pasa a texto → el modelo de Foundry/Azure
  OpenAI propone el registro → kit.acopio lo verifica → evento EPCIS + bitácora (+ Snowflake si está configurado)
  → Twilio le responde al caficultor por WhatsApp.

Seguridad:
  - Cada solicitud debe traer la firma X-Twilio-Signature válida (HMAC-SHA1 con TWILIO_AUTH_TOKEN sobre la URL
    pública + los parámetros). Sin TWILIO_AUTH_TOKEN, la ruta rechaza todo (falla cerrada).
  - Solo se descargan audios de api.twilio.com, con las credenciales enviadas solo a ese dominio.
  - El teléfono no se guarda: la bitácora y el evento llevan su huella. Los datos personales del texto se
    cambian por marcadores antes de llegar al modelo.

Variables (.env): TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM (el número del sandbox, por
ejemplo whatsapp:+14155238886) y KIT_URL_PUBLICA (la dirección https del túnel o de Azure, sin / al final).
Guía paso a paso: docs/WHATSAPP.md
"""

import base64
import hashlib
import hmac
import json
import os
import threading
import urllib.parse
import urllib.request
from typing import Callable

from . import acopio, privacidad, voz
from .bitacora import huella

RUTA = "/api/whatsapp"
MAX_AUDIO = 5_000_000
AYUDA = ("Hola 👋 Para registrar su entrega escriba o diga por nota de voz: nombre de la finca, cantidad y "
         "humedad. Ejemplo: «Finca La Loma, 3 arrobas, humedad 11».")


def configurado() -> bool:
    return all(os.environ.get(v) for v in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_WHATSAPP_FROM"))


def firma(url: str, params: dict[str, str], token: str) -> str:
    """La firma que Twilio calcula: URL + cada nombre y valor en orden alfabético, HMAC-SHA1, base64."""
    datos = url + "".join(k + params[k] for k in sorted(params))
    return base64.b64encode(hmac.new(token.encode(), datos.encode("utf-8"), hashlib.sha1).digest()).decode()


def firma_valida(url: str, params: dict[str, str], recibida: str) -> bool:
    token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    if not token or not recibida:
        return False
    return hmac.compare_digest(firma(url, params, token), recibida)


def url_publica(host: str) -> str:
    base = os.environ.get("KIT_URL_PUBLICA", "").rstrip("/") or f"https://{host}"
    return base + RUTA


def _sin_redireccion_de_clave(url: str) -> bytes:
    """Descarga el audio de Twilio. La clave va solo a api.twilio.com, nunca al destino de la redirección."""
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname != "api.twilio.com":
        raise ValueError("Solo se descargan audios de api.twilio.com")
    credencial = base64.b64encode(f"{os.environ['TWILIO_ACCOUNT_SID']}:{os.environ['TWILIO_AUTH_TOKEN']}".encode()).decode()
    req = urllib.request.Request(url)
    req.add_unredirected_header("Authorization", f"Basic {credencial}")
    with urllib.request.urlopen(req, timeout=20) as r:
        datos = r.read(MAX_AUDIO + 1)
    if len(datos) > MAX_AUDIO:
        raise ValueError("Audio demasiado largo")
    return datos


def enviar(para: str, texto: str) -> bool:
    """Responde por WhatsApp con la API de Twilio."""
    sid = os.environ["TWILIO_ACCOUNT_SID"]
    cuerpo = urllib.parse.urlencode({"From": os.environ["TWILIO_WHATSAPP_FROM"], "To": para, "Body": texto[:1500]}).encode()
    req = urllib.request.Request(f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json", data=cuerpo,
                                 method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
    credencial = base64.b64encode(f"{sid}:{os.environ['TWILIO_AUTH_TOKEN']}".encode()).decode()
    req.add_unredirected_header("Authorization", f"Basic {credencial}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return 200 <= r.status < 300


def respuesta(v: dict) -> str:
    """El mensaje para el caficultor, corto y claro."""
    if not v["ok"]:
        return "❌ No pude registrar la entrega: " + " ".join(v["problemas"]) + "\n" + AYUDA
    humedad = f", humedad {v['humedad']:g} %" if v["humedad"] is not None else ""
    texto = (f"✅ Recibido: {v['cantidad']:g} {v['unidad']} ({v['kg']:g} kg) de la finca {v['finca']}{humedad}. "
             f"Queda en el lote {v['lote']}.")
    for a in v["alertas"]:
        texto += f"\n⚠️ {a}"
    return texto


def procesar(params: dict[str, str], modelo=None, bitacora=None, guardar_snowflake: Callable | None = None,
             transcribir: Callable[[bytes, str], str] | None = None, descargar: Callable[[str], bytes] | None = None) -> dict:
    """Todo el flujo para un mensaje. Devuelve lo que se respondió y lo que se registró."""
    remitente = huella(params.get("From", ""))
    texto = (params.get("Body") or "").strip()
    origen = "texto"
    if int(params.get("NumMedia") or 0) > 0 and (params.get("MediaContentType0") or "").startswith("audio/"):
        origen = "nota_de_voz"
        try:
            audio = (descargar or _sin_redireccion_de_clave)(params["MediaUrl0"])
            texto = (transcribir or voz.voz_a_texto_audio)(audio, params["MediaContentType0"])
        except Exception as e:  # noqa: BLE001
            if bitacora:
                bitacora.registrar("whatsapp_error", {"remitente": remitente, "etapa": "voz", "error": type(e).__name__})
            return {"respuesta": "❌ No pude escuchar la nota de voz. ¿Me la escribe, por favor?\n" + AYUDA, "entrega": None}
    if not texto or texto.lower() in ("hola", "ayuda", "menu", "menú", "join twilio-trial"):
        return {"respuesta": AYUDA, "entrega": None}

    registro = acopio.cargar_registro()
    seud = privacidad.Seudonimos()
    texto_modelo = seud.ocultar(texto)  # el modelo no ve teléfonos, cédulas ni cuentas
    propuesta = acopio.proponer(texto_modelo, modelo, registro)
    v = acopio.verificar(propuesta, texto, registro)
    evento = None
    if v["ok"]:
        evento = acopio.evento_epcis(v, registro, f"whatsapp:{origen}", remitente)
        acopio.registrar(evento)
        if guardar_snowflake:
            try:
                guardar_snowflake([evento])
            except Exception as e:  # noqa: BLE001 - Snowflake caído no detiene el acopio
                if bitacora:
                    bitacora.registrar("snowflake_error", {"error": type(e).__name__})
    if bitacora:
        bitacora.registrar("entrega_whatsapp", {
            "remitente": remitente, "origen": origen, "texto": f"huella:{huella(texto)}",
            "propuesta_ia": {k: propuesta.get(k) for k in ("finca", "cantidad", "unidad", "humedad")},
            "verificado": v["ok"], "problemas": v["problemas"], "alertas": v["alertas"],
            "evento": evento["eventID"] if evento else None, "apto_ue": v["apto_ue"]})
    return {"respuesta": respuesta(v), "entrega": v, "evento": evento}


def atender_en_segundo_plano(params: dict[str, str], modelo, bitacora, guardar_snowflake=None) -> threading.Thread:
    def tarea():
        try:
            r = procesar(params, modelo, bitacora, guardar_snowflake)
            enviar(params["From"], r["respuesta"])
        except Exception as e:  # noqa: BLE001
            if bitacora:
                bitacora.registrar("whatsapp_error", {"etapa": "respuesta", "error": type(e).__name__})
    hilo = threading.Thread(target=tarea, daemon=True)
    hilo.start()
    return hilo


def leer_formulario(crudo: bytes) -> dict[str, str]:
    return {k: v[-1] for k, v in urllib.parse.parse_qs(crudo.decode("utf-8"), keep_blank_values=True).items()}


if __name__ == "__main__":
    import sys
    from . import cargar_env
    cargar_env()
    mensaje = " ".join(sys.argv[1:]) or "Finca La Loma, 3 arrobas, humedad 11"
    print(json.dumps(procesar({"From": "whatsapp:+570000000000", "Body": mensaje}), ensure_ascii=False, indent=2, default=str))
