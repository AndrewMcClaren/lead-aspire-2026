"""Escudo contra inyección de instrucciones en documentos: Prompt Shields de Azure AI Content Safety.

Antes de que el modelo lea un documento externo (un correo, un PDF, una página del cliente), Prompt
Shields dice si trae instrucciones escondidas para la IA. Los que sí, se quedan afuera.

Nivel gratis (F0): 5.000 registros de texto al mes (1.000 caracteres cada uno); al llegar al tope se
detiene, no cobra. Variables: CONTENT_SAFETY_ENDPOINT (https://<recurso>.cognitiveservices.azure.com) y
CONTENT_SAFETY_KEY. Sin ellas, escudo_disponible() es False y el asistente funciona sin escudo.

Revisen la versión de la API en la documentación de Azure antes del evento.
"""

import json
import os
import urllib.request

API_VERSION = "2024-09-01"


def escudo_disponible() -> bool:
    return bool(os.environ.get("CONTENT_SAFETY_ENDPOINT") and os.environ.get("CONTENT_SAFETY_KEY"))


def prompt_shields(documentos: list[str], peticion: str = "") -> list[bool]:
    """True por cada documento en el que Prompt Shields detecta un ataque. Si falla, lanza la excepción."""
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    cuerpo = json.dumps({"userPrompt": peticion, "documents": documentos}).encode("utf-8")
    req = urllib.request.Request(f"{endpoint}/contentsafety/text:shieldPrompt?api-version={API_VERSION}", data=cuerpo,
                                 method="POST", headers={"Ocp-Apim-Subscription-Key": os.environ["CONTENT_SAFETY_KEY"],
                                                         "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        respuesta = json.loads(r.read().decode("utf-8"))
    return [bool(d.get("attackDetected")) for d in respuesta.get("documentsAnalysis", [])]


def escudo_cerrado(documentos: list[str], peticion: str = "") -> list[bool]:
    """Como prompt_shields, pero si el servicio falla bloquea todos los documentos (falla cerrada)."""
    try:
        return prompt_shields(documentos, peticion)
    except Exception:  # noqa: BLE001
        return [True] * len(documentos)
