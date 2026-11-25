"""Decisiones tomadas en Teams que vuelven al kit, solo con conectores estándar de Power Automate.

El recorrido completo:
  1. El guardián deja una acción "pendiente" y el kit la avisa a Power Automate (NOTIFICAR_URL), con un código
     de un solo uso (token) que solo conocen el kit y ese aviso.
  2. Power Automate pide la aprobación en Teams o por correo.
  3. Cuando la persona decide, el flujo crea un archivo JSON en una carpeta de OneDrive (conector estándar).
  4. OneDrive sincroniza esa carpeta en este computador (KIT_DECISIONES apunta a ella).
  5. Este módulo revisa la carpeta cada pocos segundos, valida el archivo y aplica la decisión con las reglas de
     siempre: solo acciones pendientes, quien la pidió no puede aprobarla, todo queda en la bitácora.

El archivo que deja el flujo:
  {"id": 1, "token": "…", "resultado": "Approve", "aprobador": "Nombre Apellido", "comentario": "…"}

Por qué el token: los números de acción vuelven a empezar en 1 cada vez que arranca el servidor. Sin el token,
un archivo viejo de ayer podría aprobar la acción #1 de hoy. Un archivo sin el token correcto se aparta en la
subcarpeta "rechazadas" y queda en la bitácora.
"""

import json
import os
import threading
import time
from pathlib import Path

APROBAR = {"approve", "approved", "aprobar", "aprobado", "aprobada", "si", "sí", "yes", "true"}
RECHAZAR = {"reject", "rejected", "rechazar", "rechazado", "rechazada", "no", "false"}
MAX_BYTES = 8 * 1024


def carpeta() -> Path | None:
    valor = os.environ.get("KIT_DECISIONES", "").strip().strip('"')
    return Path(valor) if valor else None


def _apartar(archivo: Path, subcarpeta: str):
    destino = archivo.parent / subcarpeta
    destino.mkdir(exist_ok=True)
    try:
        archivo.replace(destino / archivo.name)
    except OSError:
        pass  # OneDrive puede tener el archivo abierto: se reintenta en la siguiente vuelta


def leer(archivo: Path) -> dict:
    if archivo.stat().st_size > MAX_BYTES:
        raise ValueError("archivo demasiado grande")
    datos = json.loads(archivo.read_text(encoding="utf-8-sig"))
    if not isinstance(datos, dict):
        raise ValueError("el archivo no es un objeto JSON")
    resultado = str(datos.get("resultado", "")).strip().lower()
    if resultado not in APROBAR | RECHAZAR:
        raise ValueError(f"resultado desconocido: {datos.get('resultado')!r}")
    return {"id": int(datos["id"]), "token": str(datos.get("token", "")), "aprobar": resultado in APROBAR,
            "aprobador": str(datos.get("aprobador") or "").strip()[:60],
            "comentario": str(datos.get("comentario") or "").strip()[:300]}


def procesar(dir_: Path, bandeja, bitacora=None) -> list[dict]:
    """Una vuelta: aplica las decisiones nuevas de la carpeta. Devuelve lo que hizo (para pruebas y registro)."""
    hechos = []
    for archivo in sorted(dir_.glob("*.json")):
        try:
            d = leer(archivo)
        except Exception as e:  # noqa: BLE001 - un archivo malo no detiene a los demás
            hechos.append({"archivo": archivo.name, "resultado": "rechazado", "motivo": f"{type(e).__name__}: {e}"})
            _apartar(archivo, "rechazadas")
            continue
        accion = bandeja.acciones.get(d["id"])
        if accion is None or not accion.token or d["token"] != accion.token:
            hechos.append({"archivo": archivo.name, "resultado": "rechazado", "motivo": "token o acción desconocidos"})
            _apartar(archivo, "rechazadas")
            continue
        if accion.estado != "pendiente":
            hechos.append({"archivo": archivo.name, "resultado": "ignorado", "motivo": f"la acción ya estaba {accion.estado}"})
            _apartar(archivo, "procesadas")
            continue
        try:
            bandeja.decidir(d["id"], d["aprobar"], d["aprobador"] or "persona", canal="Teams", comentario=d["comentario"])
            hechos.append({"archivo": archivo.name, "resultado": "aplicado", "id": d["id"], "aprobar": d["aprobar"]})
            _apartar(archivo, "procesadas")
        except ValueError as e:  # por ejemplo, segregación de funciones
            hechos.append({"archivo": archivo.name, "resultado": "rechazado", "motivo": str(e)})
            _apartar(archivo, "rechazadas")
    if bitacora:
        for h in hechos:
            if h["resultado"] != "aplicado":  # lo aplicado ya lo registra la bandeja
                bitacora.registrar("decision_teams_rechazada", h)
    return hechos


def vigilar(bandeja, bitacora=None, cada: float = 2.0) -> threading.Thread | None:
    """Revisa la carpeta en segundo plano. No hace nada si KIT_DECISIONES no está definida."""
    dir_ = carpeta()
    if dir_ is None:
        return None
    dir_.mkdir(parents=True, exist_ok=True)

    def ciclo():
        while True:
            try:
                procesar(dir_, bandeja, bitacora)
            except Exception:  # noqa: BLE001 - la vigilancia nunca tumba la demo
                pass
            time.sleep(cada)

    hilo = threading.Thread(target=ciclo, daemon=True, name="decisiones-teams")
    hilo.start()
    return hilo
