"""La tabla de cifras verificadas: la única fuente de números del asistente.

Cada fila tiene una clave, una descripción, el valor, la unidad, cuántos decimales mostrar y la fuente.
El modelo nunca escribe un número: escribe {clave} y este módulo pone el valor. Si la clave no existe,
la respuesta no sale. Así una cifra vieja o inventada en un prompt no puede llegar a la persona.

Para el caso del cliente: reemplaza datos/cifras.csv por un CSV con las mismas columnas, o deja tu caso en
otra carpeta y apúntala con la variable KIT_DATOS (por ejemplo KIT_DATOS=respaldo/dane).
"""

import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos"  # el caso de ejemplo
RAIZ = DATOS.parents[1]


def carpeta_datos() -> Path:
    """La carpeta del caso activo: KIT_DATOS si está definida (relativa a la raíz del repo), si no kit/datos."""
    valor = os.environ.get("KIT_DATOS")
    if not valor:
        return DATOS
    ruta = Path(valor)
    return ruta if ruta.is_absolute() else RAIZ / ruta


def archivo_del_caso(nombre: str) -> Path:
    """Un archivo del caso activo; si el caso no lo trae, el de ejemplo (politica.json, maestros.json, casos.json)."""
    propio = carpeta_datos() / nombre
    return propio if propio.exists() else DATOS / nombre


MARCADOR = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def formatear(valor: float, decimales: int = 0) -> str:
    """Formato colombiano: 92335 -> '92.335'; 47.17 con 1 decimal -> '47,2'."""
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "§").replace(".", ",").replace("§", ".")


@dataclass(frozen=True)
class Cifra:
    clave: str
    descripcion: str
    valor: float
    unidad: str
    decimales: int
    fuente: str
    sinonimos: str = ""  # opcional: palabras que usaría una persona (solo las usa el modelo simulado)

    def texto(self) -> str:
        numero = formatear(self.valor, self.decimales)
        if self.unidad == "%":
            return f"{numero} %"
        if self.unidad.startswith("$") or self.unidad.lower().startswith("pesos"):
            resto = re.sub(r"^(\$|pesos)\s*", "", self.unidad, flags=re.I)  # "pesos por carga" -> "$ 2.180.000 por carga"
            return f"$ {numero}" + (f" {resto}" if resto else "")
        return f"{numero} {self.unidad}".strip() if self.unidad not in ("", "unidades") else numero


class Tabla:
    def __init__(self, ruta: Path | None = None):
        ruta = ruta or carpeta_datos() / "cifras.csv"
        self.ruta = ruta
        with open(ruta, encoding="utf-8") as fh:
            self.cifras = {f["clave"]: Cifra(f["clave"], f["descripcion"], float(f["valor"]), f.get("unidad", ""),
                                             int(f.get("decimales") or 0), f.get("fuente", ""), f.get("sinonimos") or "")
                           for f in csv.DictReader(fh)}

    def catalogo(self) -> str:
        """Las claves con su descripción, para el prompt del modelo."""
        return "\n".join(f"- {c.clave}: {c.descripcion}" for c in self.cifras.values())

    def poner_cifras(self, texto: str) -> tuple[str, list[str], list[str]]:
        """Reemplaza {clave} por su valor con unidad. Devuelve (texto, claves usadas, claves que no existen).

        Si el modelo escribió la unidad después de la clave ("{ventas} millones de pesos"), no se repite.
        """
        usadas, desconocidas, partes, pos = [], [], [], 0
        for m in MARCADOR.finditer(texto):
            partes.append(texto[pos:m.start()])
            pos = m.end()
            clave = m.group(1)
            c = self.cifras.get(clave)
            if c is None:
                desconocidas.append(clave)
                partes.append(m.group(0))
                continue
            usadas.append(clave)
            partes.append(c.texto())
            resto = texto[pos:]
            unidad = c.unidad.strip()
            if unidad and unidad != "%" and resto.lstrip().lower().startswith(unidad.lower()):
                pos += len(resto) - len(resto.lstrip()) + len(unidad)
            elif unidad == "%" and resto.lstrip().startswith("%"):
                pos += len(resto) - len(resto.lstrip()) + 1
        partes.append(texto[pos:])
        return "".join(partes), usadas, desconocidas
