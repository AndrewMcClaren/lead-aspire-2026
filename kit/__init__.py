"""Kit de demo para LEAD ASPIRE 2026: asistente con cifras verificadas, voz y escudo contra inyección."""

import os
import sys
from pathlib import Path

# En Git Bash de Windows la consola a veces no acepta caracteres como "→": se reemplazan en vez de fallar.
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

RAIZ = Path(__file__).resolve().parents[1]


def cargar_env(ruta: Path = RAIZ / ".env") -> list[str]:
    """Carga las variables del archivo .env si existe. No pisa las que ya estén definidas.

    Acepta comillas, líneas vacías, comentarios con # y saltos de línea de Windows. Devuelve los nombres cargados.
    """
    cargadas = []
    if not ruta.exists():
        return cargadas
    for linea in ruta.read_text(encoding="utf-8-sig").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        nombre, valor = (x.strip() for x in linea.split("=", 1))
        valor = valor.strip('"').strip("'")
        if nombre and valor and nombre not in os.environ:
            os.environ[nombre] = valor
            cargadas.append(nombre)
    return cargadas
