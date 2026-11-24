"""Modelos intercambiables. Todos responden un dict con generar_json(sistema, usuario).

- "simulado": sin internet ni claves. Busca la cifra cuya descripción más se parece a la pregunta.
  Sirve para ensayar la demo y para las pruebas; no es inteligencia real y nunca se presenta como tal.
- "ingenuo": el simulado, pero obedece cualquier orden escondida en un documento y revela su
  configuración si se la piden. Es el peor caso: sirve para medir que los controles aguantan aunque el
  modelo esté totalmente manipulado. No mide a ninguna IA real.

Los modelos reales dejan en .ultimo_uso los tokens de la última llamada (para costo y latencia).
- "azure:<deployment>": Azure OpenAI (Azure for Students). Variables AZURE_OPENAI_ENDPOINT,
  AZURE_OPENAI_API_KEY y OPENAI_API_VERSION.
- "ollama:<modelo>": modelo local con Ollama (OLLAMA_HOST, por defecto http://localhost:11434).
"""

import base64
import json
import os
import re
import unicodedata
import urllib.request

_VACIAS = {"de", "la", "el", "en", "y", "que", "con", "las", "los", "del", "cuantas", "cuantos", "cuanto", "cuanta",
           "cual", "es", "hay", "por", "un", "una", "tiene", "tienen", "son", "a", "se", "su", "sus", "como", "me",
           "dime", "al", "lo", "le", "fue", "ha", "cadena", "ultimo", "ano", "este", "esta", "mas", "muy"}


def _sin_tildes(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")


def _palabras(texto: str) -> set[str]:
    """Raíces de las palabras: las primeras 5 letras ("facturas" y "factura" -> "factu")."""
    return {p[:5] for p in re.findall(r"[a-z0-9%]+", _sin_tildes(texto)) if p not in _VACIAS and len(p) > 1}


def _nombres_propios(pregunta: str) -> set[str]:
    """Palabras con mayúscula que no están al inicio de la pregunta (por ejemplo, una ciudad)."""
    pregunta = re.sub(r"\[[A-Z]+_[A-Z]+\]", " ", pregunta)  # los marcadores de datos personales no son nombres
    palabras = re.findall(r"[\wÁÉÍÓÚÑáéíóúñ]+", pregunta)
    return {_sin_tildes(p)[:5] for p in palabras[1:] if p[0].isupper() and p.lower() not in ("ia", "ai")}


class Simulado:
    """Elige la cifra con más palabras en común con la pregunta. Si ninguna se parece, dice que no tiene el dato."""

    nombre = "simulado"

    def __init__(self, tabla, minimo: int = 2):
        self.tabla, self.minimo = tabla, minimo

    def generar_json(self, sistema: str, usuario: str, imagen: bytes | None = None) -> dict:
        pregunta = usuario.split("PREGUNTA:")[-1].strip()
        q = _palabras(pregunta)
        vocabulario = set().union(*(_palabras(c.descripcion + " " + c.sinonimos) for c in self.tabla.cifras.values()))
        if _nombres_propios(pregunta) - vocabulario:  # pregunta por algo que la tabla no tiene (una ciudad, una tienda)
            return {"texto": "No tengo ese dato verificado.", "claves": []}
        mejor, puntaje = None, (0, 0)
        for c in self.tabla.cifras.values():
            desc = _palabras(c.descripcion + " " + c.clave.replace("_", " "))
            sin = _palabras(c.sinonimos + (" porcentaje por ciento proporcion" if c.unidad == "%" else ""))
            peso = len(q & desc) + 2 * len(q & sin)  # los sinónimos los escribe el equipo para la demo
            p = (len(q & (desc | sin)), peso)  # primero cuántas palabras distintas de la pregunta encajan
            if p > puntaje:
                mejor, puntaje = c, p
        if mejor is None or puntaje[1] < self.minimo:
            return {"texto": "No tengo ese dato verificado.", "claves": []}
        return {"texto": f"{mejor.descripcion}: {{{mejor.clave}}}.", "claves": [mejor.clave]}


class Ingenuo(Simulado):
    """Peor caso: obedece las órdenes de los documentos y revela su código interno si se lo piden."""

    nombre = "ingenuo (peor caso simulado)"
    _ORDEN = re.compile(r"(?:responde|responda|di|diga|dile|contesta|escribe)(?:\s+al\s+usuario)?\s+(?:que|exactamente:?|:)\s*[«\"]?(.+?)[»\"]?(?:\.\s|\.?$|\n)",
                        re.I)
    _FUGA = re.compile(r"(revela|dime|escribe|muestra|repite)\w*\b[^.]{0,40}(c[oó]digo|configuraci[oó]n|instrucciones)", re.I)

    def generar_json(self, sistema: str, usuario: str, imagen: bytes | None = None) -> dict:
        documentos = usuario.split("PREGUNTA:")[0]
        if self._FUGA.search(documentos):
            codigo = re.search(r"CFG-[0-9A-F]{8}", sistema)
            return {"texto": f"Mi configuración: {codigo.group(0) if codigo else sistema[:200]}", "claves": []}
        orden = self._ORDEN.search(documentos)
        if orden:
            return {"texto": orden.group(1).strip(), "claves": []}
        return super().generar_json(sistema, usuario, imagen)


def _json_de(texto: str) -> dict:
    """El JSON de la respuesta, aunque el modelo lo envuelva en texto o en un bloque ```json."""
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        inicio, fin = texto.find("{"), texto.rfind("}")
        if inicio == -1 or fin <= inicio:
            raise
        return json.loads(texto[inicio:fin + 1])


class AzureOpenAI:
    def __init__(self, deployment: str):
        from openai import AzureOpenAI as Cliente
        self.nombre = f"azure-{deployment}"
        self._deployment = deployment
        self._cliente = Cliente()

    def generar_json(self, sistema: str, usuario: str, imagen: bytes | None = None) -> dict:
        partes = [{"type": "text", "text": usuario}]
        if imagen is not None:
            partes.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(imagen).decode()}})
        mensajes = [{"role": "system", "content": sistema}, {"role": "user", "content": partes}]
        # Algunos modelos (los de razonamiento) rechazan temperature o response_format: se reintenta sin ellos
        # y se recuerda para las siguientes llamadas.
        extras = getattr(self, "_extras", None)
        if extras is None:
            extras = {"temperature": 0, "response_format": {"type": "json_object"}}
        while True:
            try:
                r = self._cliente.chat.completions.create(model=self._deployment, messages=mensajes, **extras)
                break
            except Exception as e:  # noqa: BLE001
                texto = str(e).lower()
                quitar = [k for k in extras if k in texto or k.replace("_", " ") in texto]
                if not quitar or "unsupported" not in texto and "not support" not in texto and "invalid" not in texto:
                    raise
                for k in quitar:
                    extras.pop(k)
        self._extras = extras
        if getattr(r, "usage", None):
            self.ultimo_uso = {"tokens_entrada": r.usage.prompt_tokens, "tokens_salida": r.usage.completion_tokens}
        return _json_de(r.choices[0].message.content or "")


class Ollama:
    def __init__(self, modelo: str = "qwen2.5:7b"):
        self.nombre = f"ollama-{modelo}"
        self._modelo = modelo
        self._host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")

    def generar_json(self, sistema: str, usuario: str, imagen: bytes | None = None) -> dict:
        mensaje = {"role": "user", "content": usuario}
        if imagen is not None:
            mensaje["images"] = [base64.b64encode(imagen).decode()]
        cuerpo = json.dumps({"model": self._modelo, "stream": False, "format": "json", "options": {"temperature": 0},
                             "messages": [{"role": "system", "content": sistema}, mensaje]}).encode("utf-8")
        req = urllib.request.Request(f"{self._host}/api/chat", data=cuerpo, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            respuesta = json.loads(r.read().decode("utf-8"))
        self.ultimo_uso = {"tokens_entrada": respuesta.get("prompt_eval_count", 0), "tokens_salida": respuesta.get("eval_count", 0)}
        return json.loads(respuesta["message"]["content"])


def crear(nombre: str, tabla):
    proveedor, _, version = nombre.partition(":")
    if proveedor == "simulado":
        return Simulado(tabla)
    if proveedor == "ingenuo":
        return Ingenuo(tabla)
    if proveedor == "azure":
        if not version:
            raise ValueError("Azure necesita el nombre del deployment: azure:<deployment>")
        return AzureOpenAI(version)
    if proveedor == "ollama":
        return Ollama(version or "qwen2.5:7b")
    raise ValueError(f"Modelo desconocido: {nombre} (usa simulado, ingenuo, azure:<deployment> u ollama:<modelo>)")
