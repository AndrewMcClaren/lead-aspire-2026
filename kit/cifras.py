"""La tabla de cifras verificadas: la única fuente de números del asistente.

Cada fila tiene una clave, una descripción, el valor, la unidad, cuántos decimales mostrar y la fuente.
El modelo nunca escribe un número: escribe {clave} y este módulo pone el valor. Si la clave no existe,
la respuesta no sale. Así una cifra vieja o inventada en un prompt no puede llegar a la persona.

Para el caso del cliente: reemplaza datos/cifras.csv por un CSV con las mismas columnas.
"""

import csv
import re
from dataclasses import dataclass
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos"
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
            return f"$ {numero}"
        return f"{numero} {self.unidad}".strip() if self.unidad not in ("", "unidades") else numero


class Tabla:
    def __init__(self, ruta: Path = DATOS / "cifras.csv"):
        with open(ruta, encoding="utf-8") as fh:
            self.cifras = {f["clave"]: Cifra(f["clave"], f["descripcion"], float(f["valor"]), f.get("unidad", ""),
                                             int(f.get("decimales") or 0), f.get("fuente", ""), f.get("sinonimos") or "")
                           for f in csv.DictReader(fh)}

    def catalogo(self) -> str:
        """Las claves con su descripción, para el prompt del modelo."""
        return "\n".join(f"- {c.clave}: {c.descripcion}" for c in self.cifras.values())

    def poner_cifras(self, texto: str) -> tuple[str, list[str], list[str]]:
        """Reemplaza {clave} por su valor. Devuelve (texto, claves usadas, claves que no existen)."""
        usadas, desconocidas = [], []

        def reemplazo(m):
            clave = m.group(1)
            if clave in self.cifras:
                usadas.append(clave)
                return self.cifras[clave].texto()
            desconocidas.append(clave)
            return m.group(0)

        return MARCADOR.sub(reemplazo, texto), usadas, desconocidas
