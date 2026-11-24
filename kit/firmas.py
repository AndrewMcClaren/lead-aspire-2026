"""Escudo local en español: firmas de ataques conocidos, sin internet, sin claves y en milisegundos.

Antes de que la IA lea un documento externo, el código busca patrones conocidos de inyección de
instrucciones ("ignora tus instrucciones", "nota para el asistente", etiquetas falsas de sistema, texto
invisible, homoglifos, cambio de cuenta de pago...). Cada firma tiene código, descripción y severidad:
- "bloqueo": texto dirigido a la IA o escondido a propósito.
- "revision": señales que también aparecen en textos legítimos (un cambio de cuenta): se marcan para una persona.

Normaliza antes de buscar: NFKC, sin caracteres invisibles ni bidireccionales, homoglifos cirílicos y
griegos pasados a latín, leetspeak ("1gn0r4") y letras separadas por signos ("i.g.n.o.r.a").

sanear() retira solo las oraciones con firmas de bloqueo y deja el resto, para que la IA conserve la
información legítima del documento en vez de perderlo entero.

HUELLA identifica la versión exacta de las reglas (sha256 de este archivo): sirve para decir con qué
reglas se midió un resultado.

Límite de cualquier detector por firmas: solo ve ataques parecidos a los conocidos. Por eso hay más
capas: Prompt Shields, el juez, la verificación de cifras y el guardián de acciones.
"""

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Firma:
    id: str
    descripcion: str
    patron: re.Pattern
    severidad: str = "bloqueo"  # "bloqueo" o "revision"


def _firma(id_: str, descripcion: str, patron: str, severidad: str = "bloqueo") -> Firma:
    return Firma(id_, descripcion, re.compile(patron, re.I), severidad)


_IA = r"(asistente|sistema|modelo|ia|agente|chatbot|bot|assistant|system|model|ai|agent|llm)"

# Los patrones se buscan sobre el texto normalizado: minúsculas, sin tildes, sin caracteres
# invisibles y con los saltos de línea convertidos en espacios (el OCR parte las frases en renglones).
FIRMAS: tuple[Firma, ...] = (
    _firma("F01", "Pide ignorar u olvidar las instrucciones o reglas",
           r"\b(ignor|olvid|omit|descart|desobedec|disregard|forget)\w*\b[^.]{0,40}\b(instruccion|indicacion|regla|instruction|rule|prompt)"),
    _firma("F02", "Anuncia instrucciones nuevas o un cambio de rol",
           r"\b(nuevas? instrucciones?|new instructions?|a partir de ahora|from now on|en adelante debes|ahora eres|you are now|actua como|act as)\b"),
    _firma("F03", "Ordena responder con un texto exacto",
           r"\b(responde|responda|contesta|conteste|escribe|escriba|repite|repita|di|diga|answer|reply|respond|say|write|repeat)\b"
           r"[^.]{0,25}\b(exactamente|textualmente|literalmente|unicamente|solamente|exactly|verbatim|literally)\b"),
    _firma("F04", "Ordena decir una frase entre comillas",
           r"\b(responde|responda|contesta|conteste|escribe|escriba|di|diga|dile|answer|say)\b(\s+que)?\s*:?\s*[«\"“]"),
    _firma("F05", "Mensaje dirigido al asistente, al sistema o a la IA",
           r"\b(instruccion|nota|mensaje|orden|aviso|indicacion|message|note|instruction)\w*\b(\s+\w+){0,3}\s+"
           rf"(para|al|a la|to|for)\s+(el\s+|la\s+|the\s+)?{_IA}\b"),
    # v2: la configuración de la IA sigue siendo sospechosa por sí sola; las claves y contraseñas solo
    # cuentan cuando se le exige a la IA (tú / your) que las revele.
    _firma("F06", "Pide revelar la configuración, el prompt o una clave de la IA",
           r"\b(codigo interno|configuracion interna|codigo de configuracion|instrucciones (del|de) sistema|prompt (del|de) sistema"
           r"|system prompt|tus instrucciones|your (system )?instructions)\b"
           r"|\b(revela|revelar|muestra|mostrar|dime|dinos|imprime|escribe|comparte|reveal|show|print|tell me|share)\b[^.]{0,30}"
           r"\b(tu|tus|your)\b[^.]{0,15}\b(contrasena|password|clave de api|api key|credencial\w*|token|secreto|secret)"),
    _firma("F07", "Marcadores de plantillas de ataque conocidas",
           r"(<\s*/?\s*(information|informacion)\s*>|#{2,}\s*\(?\s*system|\[\s*/?\s*(system|sistema|inst)\s*\]|<\|im_(start|end)\|>"
           r"|mensaje importante de mi parte|this is an important message from me)"),
    _firma("F08", "Pide hacer algo antes de responder (plantilla 'important instructions')",
           r"\b(antes de (responder|contestar|resolver|continuar|seguir)|before you (can )?(answer|solve|respond|continue))\b"),
    _firma("F09", "Frases de fraude con facturas",
           r"(sistema de ia|nota para el sistema|para la ia|instruccion para|aprobar sin revisi"
           r"|\bignora\w*\b[^.]{0,30}\b(lo anterior|lo que (te|le) (dijeron|pidieron)|todo lo)"
           r"|\b(aprobar|aprueba|apruebe|approve)\w*\s+sin\s+(revision|verificacion|control|validacion)"
           r"|\b(total|subtotal|iva|valor)\s+(real|correcto|verdadero|actualizado)\s+es\b)"),
    # F10 y F11 se calculan sobre el texto original (ver buscar_firmas): la normalización los borra.
    _firma("F10", "Caracteres invisibles o de control bidireccional (texto escondido)", r"(?!x)x"),
    _firma("F11", "Homoglifos: letras cirílicas o griegas dentro de una palabra latina", r"(?!x)x"),
    _firma("F12", "Le habla al revisor, al filtro o imita su respuesta",
           r"\b((este|el|esta) (texto|mensaje|documento|contenido|correo)\s+ya (fue|ha sido|esta) (revisad|verificad|validad|aprobad)\w*"
           r"|(revisad|verificad|validad)\w* (por|by) (el|un|the|an?)? ?(filtro|sistema de seguridad|clasificador|moderador|filter|classifier|moderator)"
           r"|clasifi\w* (esto|este|el texto|el documento) como (seguro|benigno|legitimo|limpio)"
           r"|(classify|mark|label) (this|it) as (safe|benign)"
           r"|(nota|mensaje|note|message) (para|for) (el|la|the)? ?(moderador|revisor|filtro|clasificador|juez|moderator|reviewer|filter|classifier|judge))"
           r"|\"\s*(inyeccion|injection|veredicto|verdict|es_ataque)\s*\"\s*:"),
    _firma("F13", "Cambio de la cuenta de pago", severidad="revision",
           patron=r"\b(nueva cuenta|cuenta nueva|nuevos datos bancarios|cambi\w* (de |la |el |los |nuestra |nuestro )?(cuenta|cta|numero de cuenta|datos bancarios)"
                  r"|olvid\w* (la |esa )?(cuenta|cta)|(cuenta|cta\.?) (registrada|anterior|habitual|de siempre)\b[^.]{0,40}\b(ya no|no (la )?use|no sirve|cerrada|bloqueada)"
                  r"|ya no (use|usen|uses|utilice|consigne|consignen|transfiera) (a )?(la )?(cuenta|cta)"
                  r"|actualiz\w* (los |sus |nuestros )?datos bancarios|changed? (our |the )?(bank )?account|new (bank )?account details)"),
    _firma("F14", "Pide ocultarle algo al usuario o a quien revisa", severidad="revision",
           patron=r"\b(no (le |les )?(reporte|reportes|informe|informes|avise|avises|cuente|cuentes|diga|digas|notifique|notifiques|mencione|menciones)\w*"
                  r"( nada| esto| el cambio)? (al|a su|a tu|a los|a la)? ?(usuario|cliente|jefe|contador|contadora|duen\w*|nadie|persona)"
                  r"|sin (avisar|informar|notificar|que se entere)\w* (al|a la|a su|a tu)? ?(usuario|cliente|jefe|contador|nadie)"
                  r"|(do not|don't) (tell|inform|notify|mention)\w* (the )?(user|client|anyone)|without (telling|notifying) (the )?(user|client))"),
    # v3 (prueba de penetración del 24 de noviembre): etiquetas y formatos propios del kit dentro de un documento.
    _firma("F15", "Etiquetas falsas de documento o de rol (intenta salirse del documento)",
           r"(<\s*/?\s*documento\s*>|\b(sistema|system|developer|desarrollador)\s*:\s*(nueva|new|regla|rule|instruc|orden|ahora|now))"),
    _firma("F16", "Imita el formato de respuesta del asistente",
           r"[\"“]\s*(texto|claves)\s*[\"”]\s*:"),
)

_INVISIBLES = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\u00ad]")
# Letras cirílicas y griegas que se ven iguales a las latinas: se cambian antes de buscar.
_CONFUSIBLES = str.maketrans({"а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "i", "ј": "j",
                              "ѕ": "s", "ο": "o", "α": "a", "ε": "e", "ι": "i", "ρ": "p", "ν": "v", "τ": "t", "κ": "k"})
_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})

# Huella de las reglas: el sha256 de este archivo completo (patrones y normalización). Cualquier cambio
# la mueve, incluso uno en un comentario: es a propósito, así nada cambia sin volver a congelar.
HUELLA = hashlib.sha256(Path(__file__).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def normalizar(texto: str) -> str:
    """Minúsculas, NFKC, sin tildes, sin invisibles, homoglifos pasados a latín y espacios colapsados."""
    t = _INVISIBLES.sub("", unicodedata.normalize("NFKC", texto or "")).lower().translate(_CONFUSIBLES)
    sin_tildes = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
    # "i.g.n.o.r.a" o "i-g-n-o-r-a" -> "ignora" (letras sueltas separadas por un signo)
    juntas = re.sub(r"\b(?:\w[.\-_*]){3,}\w\b", lambda m: re.sub(r"[.\-_*]", "", m.group(0)), sin_tildes)
    return re.sub(r"\s+", " ", juntas)


def _mezcla_alfabetos(texto: str) -> bool:
    """True si una palabra mezcla letras latinas con cirílicas o griegas (por ejemplo 'іgnora' con i cirílica)."""
    for palabra in re.findall(r"\w{3,}", texto):
        alfabetos = {unicodedata.name(c, "?").split(" ")[0] for c in palabra if c.isalpha()}
        if "LATIN" in alfabetos and alfabetos & {"CYRILLIC", "GREEK"}:
            return True
    return False


def buscar_firmas(texto: str) -> list[str]:
    """Los códigos de las firmas que aparecen en el texto (lista vacía si está limpio)."""
    texto = texto or ""
    t = normalizar(texto)
    t_leet = t.translate(_LEET)
    ids = []
    for f in FIRMAS:
        if f.id == "F10":
            hit = bool(_INVISIBLES.search(texto))
        elif f.id == "F11":
            hit = _mezcla_alfabetos(unicodedata.normalize("NFKC", texto))
        else:
            hit = bool(f.patron.search(t) or (t_leet != t and f.patron.search(t_leet)))
        if hit:
            ids.append(f.id)
    return ids


def severidad(ids: list[str]) -> str | None:
    """'bloqueo' si alguna firma es de bloqueo, 'revision' si solo hay de revisión, None si no hay ninguna."""
    niveles = {f.id: f.severidad for f in FIRMAS}
    if any(niveles[i] == "bloqueo" for i in ids):
        return "bloqueo"
    return "revision" if ids else None


def describir(ids: list[str]) -> str:
    nombres = {f.id: f.descripcion for f in FIRMAS}
    return "; ".join(f"{i} ({nombres[i]})" for i in ids)


_CORTE = re.compile(r"(?<=[.!?])\s+|\n+")  # corta después de . ! ? seguidos de espacio: no parte "1.500.000"


def sanear(texto: str) -> tuple[str, list[str]]:
    """Retira las oraciones con firmas de bloqueo. Devuelve (texto saneado, firmas de lo retirado)."""
    partes, retiradas = [], []
    for oracion in _CORTE.split(texto or ""):
        if not oracion.strip():
            continue
        ids = buscar_firmas(oracion)
        if severidad(ids) == "bloqueo":
            retiradas += [i for i in ids if i not in retiradas]
        else:
            partes.append(oracion.strip())
    return " ".join(partes), retiradas
