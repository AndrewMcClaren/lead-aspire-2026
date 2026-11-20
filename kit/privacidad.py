"""Datos personales: lo que identifica a una persona no llega al modelo.

Antes de enviar la pregunta y los documentos al modelo (y a Prompt Shields), cada dato personal se cambia por
un marcador: "cédula 1.023.456.789" pasa a "cédula [CEDULA_A]". El modelo trabaja con los marcadores; la tabla
de equivalencias se queda en este computador y la respuesta vuelve a la persona con los datos originales.
Es la técnica de seudonimización (tokenización) que la guía de SANS llama "Limit Sensitive Prompt Content".
La bitácora guarda la pregunta con marcadores, no con los datos.

En la salida, si el modelo escribe un dato personal que no venía como marcador, se tacha.

Qué detecta, sin internet: correos, celulares y fijos de Colombia, tarjetas (13 a 19 dígitos que pasan la
prueba de Luhn), direcciones IP, y con su palabra al lado: cédula, NIT, número de cuenta y nombres después de
"señor", "señora", "don", "doña", "paciente" o "a nombre de".

Qué NO detecta: nombres sueltos sin esas palabras, direcciones de residencia, datos de salud en texto libre.
Para eso está la detección de datos personales de Azure AI Language (no integrada aquí).
Se desactiva con KIT_PRIVACIDAD=0.
"""

import os
import re

_SEP = r"\s*(?:(?:es|era|:)\s*)?(?:n[oº°]\.?|n[uú]mero|nro\.?|#)?\s*:?\s*"
# (tipo, patrón). Si el patrón tiene un grupo, solo se oculta el grupo (la palabra que lo anuncia se queda).
PATRONES = [
    ("CORREO", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")),
    ("TARJETA", re.compile(r"(?<!\d)(?<!\d[.,])(?:\d[ -]?){12,18}\d(?!\d)(?![.,]\d)")),
    ("CEDULA", re.compile(r"\b(?:c[eé]dula(?:\s+de\s+(?:ciudadan[ií]a|extranjer[ií]a))?|c\.\s?c\.?|cc|documento(?:\s+de\s+identidad)?|"
                          r"identificaci[oó]n|pasaporte)" + _SEP + r"(\d{1,3}(?:[.\s]?\d{3}){1,3})(?![\d])", re.I)),
    ("NIT", re.compile(r"\bnit\.?" + _SEP + r"(\d{3}[.\s]?\d{3}[.\s]?\d{3}(?:\s?-\s?\d)?)(?!\d)", re.I)),
    ("CUENTA", re.compile(r"\b(?:cuenta|cta\.?)(?:\s+(?:de\s+)?(?:ahorros|corriente|bancaria))?" + _SEP +
                          r"(\d[\d-]{5,22}\d)(?!\d)", re.I)),
    ("TELEFONO", re.compile(r"(?<!\d)(?<!\d[.,])(?:\+?57[\s-]?)?(?:3\d{2}|60\d)[\s-]?\d{3}[\s-]?\d{4}(?!\d)(?![.,]\d)")),
    ("IP", re.compile(r"(?<![\d.$])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\d.])")),
    ("NOMBRE", re.compile(r"\b(?:[Ss]eñora?|[Ss]ra?\.|[Dd]oña|[Dd]on|[Pp]aciente|a nombre de)\s+"
                          r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de\s+)?[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,3})")),
]
MARCADOR = re.compile(r"\[(?:" + "|".join(t for t, _ in PATRONES) + r")_[A-Z]+\]")
TACHADO = "[dato personal oculto]"


def activa() -> bool:
    return os.environ.get("KIT_PRIVACIDAD", "1").strip().lower() not in ("0", "no", "false")


def _luhn(digitos: str) -> bool:
    total = 0
    for i, d in enumerate(reversed(digitos)):
        n = int(d) * (2 if i % 2 else 1)
        total += n - 9 if n > 9 else n
    return total % 10 == 0


def detectar(texto: str) -> list[tuple[int, int, str]]:
    """(inicio, fin, tipo) de cada dato personal, sin solaparse. Gana el patrón que aparece primero en PATRONES."""
    hallados: list[tuple[int, int, str]] = []
    for tipo, patron in PATRONES:
        for m in patron.finditer(texto):
            ini, fin = m.span(1) if patron.groups else m.span()
            if tipo == "TARJETA" and not (13 <= len(re.sub(r"\D", "", m.group())) <= 19 and _luhn(re.sub(r"\D", "", m.group()))):
                continue
            if any(ini < f and i < fin for i, f, _ in hallados):
                continue
            hallados.append((ini, fin, tipo))
    return sorted(hallados)


def _letras(n: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA. Sin dígitos: así un marcador nunca parece una cifra escrita a mano."""
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


class Seudonimos:
    """Cambia datos personales por marcadores y los devuelve después. Un mismo dato recibe siempre el mismo marcador."""

    def __init__(self):
        self.originales: dict[str, str] = {}
        self._marcadores: dict[tuple[str, str], str] = {}
        self._cuenta: dict[str, int] = {}

    def ocultar(self, texto: str) -> str:
        partes, pos = [], 0
        for ini, fin, tipo in detectar(texto):
            valor = texto[ini:fin]
            llave = (tipo, re.sub(r"[\s.-]", "", valor).lower())
            if llave not in self._marcadores:
                n = self._cuenta.get(tipo, 0)
                self._cuenta[tipo] = n + 1
                marcador = f"[{tipo}_{_letras(n)}]"
                self._marcadores[llave] = marcador
                self.originales[marcador] = valor
            partes += [texto[pos:ini], self._marcadores[llave]]
            pos = fin
        return "".join(partes) + texto[pos:]

    def restaurar(self, texto: str) -> str:
        return MARCADOR.sub(lambda m: self.originales.get(m.group(), m.group()), texto)

    def tipos(self) -> list[str]:
        return sorted({m[1:].rsplit("_", 1)[0] for m in self.originales})


def tachar(texto: str) -> tuple[str, int]:
    """Para la salida: tacha los datos personales que el modelo escribió por su cuenta (no los marcadores)."""
    hallados = detectar(texto)
    for ini, fin, _ in reversed(hallados):
        texto = texto[:ini] + TACHADO + texto[fin:]
    return texto, len(hallados)
