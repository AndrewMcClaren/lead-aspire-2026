"""Integridad de los datos del caso: detecta si alguien cambió las cifras, la política o los datos maestros.

Si alguien altera cifras.csv, el asistente "verifica" contra datos falsos; si altera maestros.json, el guardián
acepta una cuenta falsa. Es el envenenamiento de datos del que habla SANS, en pequeño. Por eso, cuando el equipo
termina de cargar los datos del cliente, los sella: se guarda la huella SHA-256 de cada archivo en huellas.json.
Desde ahí, el servidor y kit.verificar avisan si un archivo cambió sin volver a sellar.

Uso (desde la raíz del repo):
  python -m kit.integridad sellar     # después de cargar o corregir los datos del caso
  python -m kit.integridad revisar    # ¿cambió algo desde el último sello?
  KIT_DATOS=respaldo/dane python -m kit.integridad revisar

La huella ignora los cambios de fin de línea (Windows y Linux dan la misma huella). Límite: quien puede editar
los datos también puede volver a sellar; el sello prueba que nada cambió *por accidente o sin avisar*, y git
muestra quién selló y cuándo.
"""

import hashlib
import json
import sys
from pathlib import Path

from .cifras import carpeta_datos

ARCHIVOS = ("cifras.csv", "contexto.md", "politica.json", "maestros.json", "casos.json", "sugeridas.json", "mercados.json", "fincas.json")
SELLO = "huellas.json"


def huella_archivo(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def huellas(carpeta: Path | None = None) -> dict[str, str]:
    carpeta = carpeta or carpeta_datos()
    return {n: huella_archivo(carpeta / n) for n in ARCHIVOS if (carpeta / n).exists()}


def sellar(carpeta: Path | None = None) -> Path:
    carpeta = carpeta or carpeta_datos()
    ruta = carpeta / SELLO
    ruta.write_text(json.dumps(huellas(carpeta), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return ruta


def revisar(carpeta: Path | None = None) -> dict:
    """{"estado": "integra" | "alterada" | "sin_sello", "cambiados": [...], "nuevos": [...], "faltan": [...]}"""
    carpeta = carpeta or carpeta_datos()
    ruta = carpeta / SELLO
    if not ruta.exists():
        return {"estado": "sin_sello", "cambiados": [], "nuevos": [], "faltan": []}
    sello, ahora = json.loads(ruta.read_text(encoding="utf-8")), huellas(carpeta)
    r = {"cambiados": sorted(n for n in sello if n in ahora and ahora[n] != sello[n]),
         "nuevos": sorted(set(ahora) - set(sello)), "faltan": sorted(set(sello) - set(ahora))}
    r["estado"] = "alterada" if any(r.values()) else "integra"
    return r


def describir(r: dict) -> str:
    if r["estado"] == "sin_sello":
        return "sin sello: después de cargar los datos corran python -m kit.integridad sellar"
    if r["estado"] == "integra":
        return "los datos no cambiaron desde el último sello"
    partes = [f"{k}: {', '.join(v)}" for k, v in (("cambiaron", r["cambiados"]), ("nuevos", r["nuevos"]),
                                                    ("faltan", r["faltan"])) if v]
    return "ALTERADOS desde el último sello (" + "; ".join(partes) + "). Si el cambio fue suyo, vuelvan a sellar"


def main(argv: list[str]) -> int:
    from . import cargar_env
    cargar_env()
    orden = argv[0] if argv else "revisar"
    if orden == "sellar":
        ruta = sellar()
        print(f"Sellado: {ruta} ({len(huellas())} archivos). Súbanlo con git para que quede quién selló y cuándo.")
        return 0
    if orden == "revisar":
        r = revisar()
        print(f"{carpeta_datos().name}: {describir(r)}")
        return 1 if r["estado"] == "alterada" else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
