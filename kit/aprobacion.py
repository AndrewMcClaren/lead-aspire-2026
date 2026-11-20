"""Guardián de acciones: la IA propone, el código revisa y una persona aprueba lo delicado.

La política vive en datos/politica.json y los destinos permitidos en datos/maestros.json: son archivos
del equipo, no texto que la IA pueda cambiar. Cada acción propuesta pasa por estas revisiones, y el
resultado solo puede endurecerse (permitida < pendiente < bloqueada):

  1. Nivel de autonomía: solo_lectura, confirmar_sensibles o confirmar_todo.
  2. Intención: ¿lo que pidió el usuario justifica esta acción? Si pidió "resúmeme el correo", un pago
     no fue pedido: se bloquea.
  3. Destino: ¿está en los datos maestros? Si la cuenta no es la registrada, se bloquea (un cambio de
     cuenta se hace por el proceso formal, nunca porque lo diga un documento). Una cuenta registrada
     hace pocos días pide confirmación.
  4. Monto: si supera lo que pidió el usuario, se bloquea; si supera el umbral, pide aprobación.
  5. Sesión: si en la conversación se bloqueó o saneó un documento, lo sensible pide aprobación (o se
     bloquea, según la política).
  6. Segregación de funciones: quien pide una acción no puede aprobarla.

Si se define NOTIFICAR_URL, cada acción pendiente se envía como JSON a esa dirección (por ejemplo, el
disparador HTTP de un flujo de Power Automate que avisa en Teams). Ese flujo se arma en Power Automate y
no se probó desde este repositorio; la demo funciona igual sin él.
"""

import itertools
import json
import os
import re
import unicodedata
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import date, datetime

from .bitacora import proteger
from .cifras import archivo_del_caso

NIVEL = {"permitida": 0, "pendiente": 1, "bloqueada": 2}
POLITICA_POR_DEFECTO = {"nivel_autonomia": "confirmar_sensibles",
                        "tipos_sensibles": ["pago", "transferencia", "enviar_datos", "cambiar_cuenta", "borrar"],
                        "tipos_solo_lectura": ["consulta", "resumen", "reporte"], "umbral_aprobacion": 1_000_000,
                        "tolerancia_monto": 0.05, "intencion": {}, "destino_requerido_para": [],
                        "dias_cuenta_nueva": 30, "sesion_sospechosa": "confirmar", "segregacion_de_funciones": True}


def cargar_politica() -> dict:
    ruta = archivo_del_caso("politica.json")
    datos = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    umbral = os.environ.get("UMBRAL_APROBACION")
    if umbral:
        datos["umbral_aprobacion"] = float(umbral)
    return {**POLITICA_POR_DEFECTO, **{k: v for k, v in datos.items() if not k.startswith("nota")}}


def cargar_maestros() -> dict:
    ruta = archivo_del_caso("maestros.json")
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {"destinos": {}}


def _norm(texto: str) -> str:
    t = "".join(c for c in unicodedata.normalize("NFD", (texto or "").lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9@]", "", t)


def montos_pedidos(texto: str) -> list[float]:
    """Montos que aparecen en lo que pidió el usuario: "1.500.000", "$ 2.000.000", "3 millones", "1,5 millones"."""
    montos = []
    for m in re.finditer(r"(\d+(?:[.,]\d+)*)\s*(millones|millón|mill|m\b)?", texto or "", re.I):
        numero, escala = m.group(1), m.group(2)
        if escala:
            valor = float(numero.replace(".", "").replace(",", ".")) * 1_000_000
        else:
            valor = float(numero.replace(".", "").replace(",", ""))
        if valor >= 1000:  # ignora números de factura cortos o días
            montos.append(valor)
    return montos


def revisar_accion(tipo: str, monto: float | None = None, destino: str = "", cuenta: str = "", peticion: str = "",
                   sesion: str = "limpia", politica: dict | None = None, maestros: dict | None = None) -> tuple[str, list[str]]:
    """Función pura: (estado, motivos). La misma acción con la misma política siempre da lo mismo."""
    pol = politica or cargar_politica()
    maestros = maestros if maestros is not None else cargar_maestros()
    estado, motivos = "permitida", []

    def subir(nuevo, motivo):
        nonlocal estado
        if NIVEL[nuevo] > NIVEL[estado]:
            estado = nuevo
        motivos.append(motivo)

    sensible = tipo in pol["tipos_sensibles"]
    nivel = pol["nivel_autonomia"]
    if nivel == "solo_lectura" and tipo not in pol["tipos_solo_lectura"]:
        subir("bloqueada", "La IA está en modo solo lectura: no puede ejecutar acciones")
    if tipo not in pol["tipos_sensibles"] and tipo not in pol["tipos_solo_lectura"]:
        subir("pendiente", f"'{tipo}' no está en la política: lo decide una persona")

    patron = pol["intencion"].get(tipo)
    if sensible and patron:
        if not peticion.strip():
            subir("pendiente", "No hay una petición del usuario que respalde la acción")
        elif not re.search(patron, _norm_texto(peticion)):
            subir("bloqueada", f"'{tipo}' no corresponde a lo que pidió el usuario")

    if tipo in pol["destino_requerido_para"]:
        registros = {_norm(n): d for n, d in maestros.get("destinos", {}).items()}
        registro = registros.get(_norm(destino))
        if not destino:
            subir("pendiente", "La acción no dice a quién va dirigida")
        elif registro is None:
            subir("pendiente", f"'{destino}' no está en los datos maestros")
        else:
            registrada = registro.get("cuenta") or registro.get("correo") or ""
            if cuenta and registrada and _norm(cuenta) != _norm(registrada):
                subir("bloqueada", f"La cuenta no es la registrada para '{destino}': un cambio de cuenta se hace por el "
                                   "proceso de datos maestros, nunca porque lo diga un documento")
            desde = registro.get("desde")
            corte = maestros.get("fecha_corte") or date.today().isoformat()
            if desde and (date.fromisoformat(corte) - date.fromisoformat(desde)).days < pol["dias_cuenta_nueva"]:
                subir("pendiente", f"El destino se registró hace menos de {pol['dias_cuenta_nueva']} días")

    if monto is not None:
        pedidos = montos_pedidos(peticion)
        if pedidos and monto > max(pedidos) * (1 + pol["tolerancia_monto"]):
            subir("bloqueada", f"El monto ({monto:,.0f}) supera lo que pidió el usuario ({max(pedidos):,.0f})".replace(",", "."))
        if monto > pol["umbral_aprobacion"]:
            subir("pendiente", f"El monto supera el umbral de {pol['umbral_aprobacion']:,.0f}".replace(",", "."))

    if sensible and sesion == "sospechosa":
        subir("bloqueada" if pol["sesion_sospechosa"] == "bloquear" else "pendiente",
              "En esta conversación se detectó un documento con instrucciones escondidas")
    if nivel == "confirmar_todo" or (sensible and nivel == "confirmar_sensibles"):
        subir("pendiente", f"'{tipo}' es una acción sensible: la decide una persona")
    if not motivos:
        motivos.append("Acción de bajo riesgo")
    return estado, motivos


def _norm_texto(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", (texto or "").lower()) if unicodedata.category(c) != "Mn")


@dataclass
class Accion:
    id: int
    tipo: str
    detalle: str
    monto: float | None = None
    destino: str = ""
    cuenta: str = ""
    peticion: str = ""
    solicitante: str = "asistente"
    estado: str = "pendiente"  # permitida, pendiente, bloqueada, aprobada o rechazada
    motivos: list = field(default_factory=list)
    creada: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    decidida_por: str = ""

    @property
    def motivo(self) -> str:
        return " · ".join(self.motivos)


class Bandeja:
    def __init__(self, bitacora=None):
        self.acciones: dict[int, Accion] = {}
        self._ids = itertools.count(1)
        self.bitacora = bitacora

    def proponer(self, tipo: str, detalle: str, monto: float | None = None, destino: str = "", cuenta: str = "",
                 peticion: str = "", solicitante: str = "asistente", sesion: str = "limpia") -> Accion:
        estado, motivos = revisar_accion(tipo, monto, destino, cuenta, peticion, sesion)
        a = Accion(next(self._ids), tipo, detalle, monto, destino, cuenta, peticion, solicitante or "asistente",
                   estado, motivos)
        self.acciones[a.id] = a
        if self.bitacora:
            datos = {k: v for k, v in asdict(a).items() if k != "creada"}
            self.bitacora.registrar("accion_propuesta", proteger(datos, ("detalle", "peticion", "cuenta")))
        if estado == "pendiente":
            notificar(a)
        return a

    def decidir(self, id_: int, aprobar: bool, aprobador: str = "persona") -> Accion:
        a = self.acciones[id_]
        if a.estado != "pendiente":
            raise ValueError(f"La acción {id_} está {a.estado}: solo se deciden las pendientes")
        pol = cargar_politica()
        if pol["segregacion_de_funciones"] and _norm(aprobador) == _norm(a.solicitante):
            raise ValueError("Quien pidió la acción no puede aprobarla (segregación de funciones)")
        a.estado, a.decidida_por = ("aprobada" if aprobar else "rechazada"), aprobador
        if self.bitacora:
            self.bitacora.registrar("accion_decidida", {"id": a.id, "estado": a.estado, "aprobador": aprobador})
        return a

    def lista(self) -> list[dict]:
        return [{**asdict(a), "motivo": a.motivo} for a in sorted(self.acciones.values(), key=lambda x: -x.id)]


def notificar(accion: Accion) -> bool:
    """Envía la acción pendiente a NOTIFICAR_URL si existe. Nunca bloquea la demo si falla."""
    url = os.environ.get("NOTIFICAR_URL")
    if not url:
        return False
    try:
        req = urllib.request.Request(url, data=json.dumps({**asdict(accion), "motivo": accion.motivo}, ensure_ascii=False).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10).close()
        return True
    except Exception:  # noqa: BLE001
        return False
