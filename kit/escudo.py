"""Escudo contra inyección de instrucciones en documentos externos, en capas (ver revisar_documentos).

Antes de que el modelo lea un documento externo (un correo, un PDF, una página del cliente), se revisa
con firmas locales, con Prompt Shields de Azure AI Content Safety y, si se activa, con un juez LLM.

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


def juez_activo() -> bool:
    return os.environ.get("KIT_JUEZ", "").strip().lower() in ("1", "si", "sí", "true")


def revisar_documentos(documentos: list[str], peticion: str = "", modelo_juez=None) -> list[dict]:
    """El escudo completo, en capas, de la más barata a la más cara. Una entrada por documento:

        {"accion": "pasa" | "saneado" | "bloqueado", "texto": lo que leerá la IA, "capas": [...], "motivos": [...]}

    1. Firmas locales (siempre, sin internet): retiran las oraciones con instrucciones para la IA. Si queda
       menos de una cuarta parte del documento, se bloquea entero.
    2. Prompt Shields (si está configurado): si ve un ataque en lo que queda, bloquea el documento.
       Si el servicio falla, bloquea (falla cerrada).
    3. Juez LLM (si KIT_JUEZ=1 y hay modelo): igual, con canario y falla cerrada.
    """
    from .firmas import buscar_firmas, describir, sanear, severidad

    informes = []
    for doc in documentos:
        texto, capas, motivos, accion = doc, [], [], "pasa"
        saneado, retiradas = sanear(doc)
        if retiradas:
            capas.append("firmas")
            motivos.append(f"Firmas locales: {describir(retiradas)}")
            # Si casi no queda nada, el documento era el ataque: se bloquea entero.
            accion = "bloqueado" if len(saneado) < max(20, len(doc) / 4) else "saneado"
            texto = saneado
        revision = [i for i in buscar_firmas(texto) if severidad([i]) == "revision"]
        if revision:
            motivos.append(f"Para revisar: {describir(revision)}")
        informes.append({"accion": accion, "texto": texto, "capas": capas, "motivos": motivos})

    vivos = [i for i, inf in enumerate(informes) if inf["accion"] != "bloqueado" and inf["texto"].strip()]
    if vivos and escudo_disponible():
        veredictos = escudo_cerrado([informes[i]["texto"] for i in vivos], peticion)
        for i, ataque in zip(vivos, veredictos):
            informes[i]["capas"].append("prompt_shields")
            if ataque:
                informes[i]["accion"] = "bloqueado"
                informes[i]["motivos"].append("Prompt Shields detectó un ataque (o el servicio no respondió)")
    if modelo_juez is not None and juez_activo():
        from .juez import juzgar
        for i in vivos:
            if informes[i]["accion"] == "bloqueado":
                continue
            v = juzgar(modelo_juez, informes[i]["texto"], peticion)
            informes[i]["capas"].append("juez")
            if v["inyeccion"]:
                informes[i]["accion"] = "bloqueado"
                informes[i]["motivos"].append(f"Juez LLM: {v['razon']}")
    for inf in informes:
        if inf["accion"] == "bloqueado":
            inf["texto"] = ""
    return informes
