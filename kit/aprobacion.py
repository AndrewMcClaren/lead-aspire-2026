"""Aprobación humana: el agente propone una acción y una persona la aprueba o la rechaza.

Es la compuerta del Guardián (y lo que hizo ganar a AlignBuddy en LEAD ASPIRE Nueva York): la IA no
ejecuta sola lo delicado. La política es código, no un prompt:
  - acciones de tipos sensibles (pagos, envío de datos, cambios de cuenta) -> esperan aprobación
  - montos sobre UMBRAL_APROBACION -> esperan aprobación
  - lo demás se permite y queda registrado

Las acciones pendientes se ven y se deciden en la página del kit. Si se define NOTIFICAR_URL, además se
envía un aviso JSON a esa dirección: por ejemplo, el disparador HTTP de un flujo de Power Automate que
publica el aviso en Teams. Ese flujo se arma en Power Automate y no se probó desde este repositorio;
la demo funciona igual sin él.
"""

import itertools
import json
import os
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime

TIPOS_SENSIBLES = {"pago", "transferencia", "enviar_datos", "cambiar_cuenta", "borrar"}
UMBRAL_APROBACION = float(os.environ.get("UMBRAL_APROBACION", "1000000"))


@dataclass
class Accion:
    id: int
    tipo: str
    detalle: str
    monto: float | None = None
    estado: str = "pendiente"  # permitida, pendiente, aprobada o rechazada
    motivo: str = ""
    creada: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    decidida_por: str = ""


def politica(tipo: str, monto: float | None) -> tuple[str, str]:
    """(estado, motivo). Solo endurece: nada sensible pasa sin una persona."""
    if tipo in TIPOS_SENSIBLES:
        return "pendiente", f"'{tipo}' es una acción sensible: la decide una persona"
    if monto is not None and monto > UMBRAL_APROBACION:
        return "pendiente", f"el monto supera el umbral de {UMBRAL_APROBACION:,.0f}".replace(",", ".")
    return "permitida", "acción de bajo riesgo"


class Bandeja:
    def __init__(self):
        self.acciones: dict[int, Accion] = {}
        self._ids = itertools.count(1)

    def proponer(self, tipo: str, detalle: str, monto: float | None = None) -> Accion:
        estado, motivo = politica(tipo, monto)
        a = Accion(next(self._ids), tipo, detalle, monto, estado, motivo)
        self.acciones[a.id] = a
        if estado == "pendiente":
            notificar(a)
        return a

    def decidir(self, id_: int, aprobar: bool, quien: str = "persona") -> Accion:
        a = self.acciones[id_]
        if a.estado != "pendiente":
            raise ValueError(f"La acción {id_} ya está {a.estado}")
        a.estado, a.decidida_por = ("aprobada" if aprobar else "rechazada"), quien
        return a

    def lista(self) -> list[dict]:
        return [asdict(a) for a in sorted(self.acciones.values(), key=lambda x: -x.id)]


def notificar(accion: Accion) -> bool:
    """Envía la acción pendiente a NOTIFICAR_URL si existe. Nunca bloquea la demo si falla."""
    url = os.environ.get("NOTIFICAR_URL")
    if not url:
        return False
    try:
        req = urllib.request.Request(url, data=json.dumps(asdict(accion), ensure_ascii=False).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10).close()
        return True
    except Exception:  # noqa: BLE001
        return False
