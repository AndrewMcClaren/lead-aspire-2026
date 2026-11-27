"""Voz con Azure AI Speech (nivel gratis F0): texto a voz con voz colombiana y voz a texto en español.

F0 da 5 horas al mes de voz a texto y 500.000 caracteres al mes de texto a voz con voces neurales.
Variables: SPEECH_KEY y SPEECH_REGION (por ejemplo eastus). Usa las API REST, sin instalar el SDK.

Prueba rápida de ida y vuelta:  python -m kit.voz "La cadena tiene treinta y ocho tiendas."
"""

import json
import os
import sys
import urllib.request
from html import escape

VOZ = os.environ.get("SPEECH_VOZ", "es-CO-SalomeNeural")  # o es-CO-GonzaloNeural


def voz_disponible() -> bool:
    return bool(os.environ.get("SPEECH_KEY") and os.environ.get("SPEECH_REGION"))


def _pedir(url: str, cuerpo: bytes, cabeceras: dict) -> bytes:
    req = urllib.request.Request(url, data=cuerpo, method="POST",
                                 headers={"Ocp-Apim-Subscription-Key": os.environ["SPEECH_KEY"], **cabeceras})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def texto_a_voz(texto: str, voz: str = VOZ) -> bytes:
    """Devuelve un WAV de 16 kHz."""
    region = os.environ["SPEECH_REGION"]
    ssml = f"<speak version='1.0' xml:lang='es-CO'><voice name='{escape(voz)}'>{escape(texto)}</voice></speak>"
    return _pedir(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", ssml.encode("utf-8"),
                  {"Content-Type": "application/ssml+xml", "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
                   "User-Agent": "lead-aspire-2026"})


def voz_a_texto(wav: bytes, idioma: str = "es-CO") -> str:
    """Transcribe un WAV PCM de 16 kHz (máximo unos 60 segundos con esta API)."""
    region = os.environ["SPEECH_REGION"]
    url = (f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
           f"?language={idioma}&format=simple")
    r = json.loads(_pedir(url, wav, {"Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000"}))
    return r.get("DisplayText", "") if r.get("RecognitionStatus") == "Success" else f"[{r.get('RecognitionStatus')}]"


FORMATOS_AUDIO = {"audio/ogg": "audio/ogg; codecs=opus", "audio/wav": "audio/wav; codecs=audio/pcm; samplerate=16000"}


def voz_a_texto_audio(audio: bytes, tipo: str, idioma: str = "es-CO") -> str:
    """Transcribe una nota de voz de WhatsApp (OGG con Opus) o un WAV. Máximo unos 60 segundos con esta API."""
    formato = FORMATOS_AUDIO.get(tipo.split(";")[0].strip().lower())
    if formato is None:
        raise ValueError(f"Formato de audio no soportado: {tipo}")
    region = os.environ["SPEECH_REGION"]
    url = (f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
           f"?language={idioma}&format=simple")
    r = json.loads(_pedir(url, audio, {"Content-Type": formato}))
    if r.get("RecognitionStatus") != "Success":
        raise ValueError(f"Speech no reconoció el audio: {r.get('RecognitionStatus')}")
    return r.get("DisplayText", "")


if __name__ == "__main__":
    from . import cargar_env
    cargar_env()
    if not voz_disponible():
        sys.exit("Faltan SPEECH_KEY y SPEECH_REGION (portal de Azure → recurso de Speech → Claves y punto de conexión).")
    frase = sys.argv[1] if len(sys.argv) > 1 else "La cadena tiene treinta y ocho tiendas y cincuenta y dos mil clientes activos."
    audio = texto_a_voz(frase)
    print(f"[OK] Texto a voz: {len(audio)} bytes con {VOZ}")
    print(f"[OK] Voz a texto: {voz_a_texto(audio)}")
