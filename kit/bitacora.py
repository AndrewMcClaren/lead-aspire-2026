"""Bitácora de auditoría encadenada: cada decisión queda registrada y nadie la puede alterar sin que se note.

Cada entrada guarda el hash de la anterior. Si alguien cambia, borra o reordena una línea, la cadena se
rompe y `verificar` dice en qué entrada. Con BITACORA_CLAVE definida, cada entrada se firma con HMAC:
entonces ni siquiera quien edite el archivo puede recalcular la cadena sin la clave.

Qué se guarda: la pregunta, la respuesta, el estado, las claves de cifras usadas, las capas que actuaron y
las decisiones sobre acciones. De los documentos externos solo se guarda su huella (sha256), no el texto,
para no copiar datos del cliente en la bitácora.

Uso:  python -m kit.bitacora verificar      |   python -m kit.bitacora ver [N]
"""

import hashlib
import hmac
import json
import os
import sys
import threading
from datetime import datetime
from pathlib import Path

from .cifras import RAIZ

RUTA = RAIZ / "resultados" / "bitacora.jsonl"


def ruta_por_defecto() -> Path:
    """KIT_BITACORA si está definida (por ejemplo, una carpeta compartida del equipo); si no, resultados/bitacora.jsonl."""
    return Path(os.environ["KIT_BITACORA"]) if os.environ.get("KIT_BITACORA") else RUTA
GENESIS = "0" * 64


def _clave() -> bytes | None:
    k = os.environ.get("BITACORA_CLAVE")
    return k.encode("utf-8") if k else None


def _sello(entrada: dict, clave: bytes | None) -> str:
    cuerpo = json.dumps({k: v for k, v in entrada.items() if k != "sello"}, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hmac.new(clave, cuerpo, hashlib.sha256).hexdigest() if clave else hashlib.sha256(cuerpo).hexdigest()


def huella(texto: str) -> str:
    return hashlib.sha256((texto or "").encode("utf-8")).hexdigest()[:16]


def privada() -> bool:
    """KIT_BITACORA_PRIVADA=1: la bitácora guarda huellas en vez de textos que pueden traer datos personales."""
    return os.environ.get("KIT_BITACORA_PRIVADA", "").strip().lower() in ("1", "si", "sí", "true")


def proteger(datos: dict, campos: tuple[str, ...]) -> dict:
    """En modo privado, cambia esos campos por su huella (se puede comprobar un texto, pero no leerlo)."""
    if not privada():
        return datos
    return {k: (f"huella:{huella(str(v))}" if k in campos and v else v) for k, v in datos.items()}


class Bitacora:
    def __init__(self, ruta: Path | None = None):
        self.ruta = Path(ruta or ruta_por_defecto())
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._n, self._previo = 0, GENESIS
        if self.ruta.exists():
            for linea in self.ruta.read_text(encoding="utf-8").splitlines():
                if linea.strip():
                    e = json.loads(linea)
                    self._n, self._previo = e["n"], e["sello"]

    def registrar(self, tipo: str, datos: dict) -> dict:
        with self._lock:
            entrada = {"n": self._n + 1, "fecha": datetime.now().isoformat(timespec="seconds"), "tipo": tipo,
                       "datos": datos, "previo": self._previo, "firmada": _clave() is not None}
            entrada["sello"] = _sello(entrada, _clave())
            with self.ruta.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entrada, ensure_ascii=False) + "\n")
            self._n, self._previo = entrada["n"], entrada["sello"]
            return entrada


def verificar(ruta: Path | None = None) -> tuple[bool, int, str]:
    """(íntegra, entradas revisadas, problema). Revisa la cadena completa."""
    ruta = Path(ruta or ruta_por_defecto())
    if not Path(ruta).exists():
        return True, 0, "la bitácora está vacía"
    previo, n = GENESIS, 0
    for i, linea in enumerate(Path(ruta).read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip():
            continue
        try:
            e = json.loads(linea)
        except json.JSONDecodeError:
            return False, n, f"la línea {i} no es JSON válido"
        if e.get("n") != n + 1:
            return False, n, f"falta o sobra una entrada antes de la línea {i} (esperaba {n + 1}, hay {e.get('n')})"
        if e.get("previo") != previo:
            return False, n, f"la entrada {e['n']} no encadena con la anterior"
        if e.get("firmada") and _clave() is None:
            return False, n, f"la entrada {e['n']} está firmada: define BITACORA_CLAVE para verificarla"
        if e.get("sello") != _sello(e, _clave() if e.get("firmada") else None):
            return False, n, f"la entrada {e['n']} fue modificada"
        previo, n = e["sello"], e["n"]
    return True, n, "íntegra"


def main():
    from . import cargar_env
    cargar_env()
    orden = sys.argv[1] if len(sys.argv) > 1 else "verificar"
    if orden == "verificar":
        ok, n, problema = verificar()
        print(f"[{'OK' if ok else '!!'}] Bitácora {ruta_por_defecto()}: {n} entradas · {problema}")
        return 0 if ok else 1
    if orden == "ver":
        cuantas = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        ruta = ruta_por_defecto()
        lineas = ruta.read_text(encoding="utf-8").splitlines() if ruta.exists() else []
        for linea in lineas[-cuantas:]:
            e = json.loads(linea)
            print(f"#{e['n']} {e['fecha']} {e['tipo']}: {json.dumps(e['datos'], ensure_ascii=False)[:160]}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
