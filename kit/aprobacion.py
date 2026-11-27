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
  4. Monto: si supera lo que pidió el usuario, se bloquea; si supera el umbral, pide aprobación. Si el
     destino es un rubro con presupuesto (maestros.json, "presupuestos"), el monto más lo ya comprometido en
     la sesión no puede superar el saldo disponible: así tampoco pasa un gasto partido en pedazos pequeños.
  5. Sesión: si en la conversación se bloqueó o saneó un documento, lo sensible pide aprobación (o se
     bloquea, según la política).
  6. Segregación de funciones: quien pide una acción no puede aprobarla.
  7. Parada automática: si en la conversación llegan varios documentos con trampa (parada_automatica en la
     política, 3 por defecto), la sesión queda "detenida" y ninguna acción pasa hasta que una persona la
     revise y la reinicie. Como la tarjeta que se bloquea al tercer intento con la clave equivocada.

Si se define NOTIFICAR_URL, cada acción pendiente se envía como JSON a esa dirección (por ejemplo, el
disparador HTTP de un flujo de Power Automate que avisa en Teams). Ese flujo se arma en Power Automate y
no se probó desde este repositorio; la demo funciona igual sin él.
"""

import itertools
import secrets
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
                        "dias_cuenta_nueva": 30, "sesion_sospechosa": "confirmar", "segregacion_de_funciones": True,
                        "parada_automatica": 3}


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
    """Para comparar nombres: sin tildes, mayúsculas, espacios, signos ni letras de otros alfabetos que se ven
    iguales ("аsistente" con una a cirílica es "asistente"). Así nadie se aprueba a sí mismo con un truco de escritura."""
    from .firmas import normalizar
    t = "".join(c for c in unicodedata.normalize("NFD", normalizar(texto or "")) if unicodedata.category(c) != "Mn")
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
                   sesion: str = "limpia", politica: dict | None = None, maestros: dict | None = None,
                   comprometido: float = 0, lote: str = "") -> tuple[str, list[str]]:
    """Función pura: (estado, motivos). La misma acción con la misma política siempre da lo mismo."""
    pol = politica or cargar_politica()
    maestros = maestros if maestros is not None else cargar_maestros()
    estado, motivos = "permitida", []

    def subir(nuevo, motivo):
        nonlocal estado
        if NIVEL[nuevo] > NIVEL[estado]:
            estado = nuevo
        motivos.append(motivo)

    if monto is not None and not (0 <= monto < 1e15):  # negativo, infinito, NaN o absurdo
        subir("bloqueada", "El monto no es válido")
    if sesion == "detenida":
        subir("bloqueada", "La sesión está detenida por intentos repetidos de engaño: una persona debe revisarla y "
                           "reiniciarla antes de cualquier acción")
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

    presupuestos = {_norm(n): (n, d) for n, d in maestros.get("presupuestos", {}).items()}
    rubro = presupuestos.get(_norm(destino))
    if tipo in pol["destino_requerido_para"]:
        registros = {_norm(n): d for n, d in maestros.get("destinos", {}).items()}
        registro = registros.get(_norm(destino))
        if not destino:
            subir("pendiente", "La acción no dice a quién va dirigida")
        elif registro is None and rubro is None:
            subir("pendiente", f"'{destino}' no está en los datos maestros")
        elif registro is not None:
            registrada = registro.get("cuenta") or registro.get("correo") or ""
            if cuenta and registrada and _norm(cuenta) != _norm(registrada):
                subir("bloqueada", f"La cuenta no es la registrada para '{destino}': un cambio de cuenta se hace por el "
                                   "proceso de datos maestros, nunca porque lo diga un documento")
            desde = registro.get("desde")
            corte = maestros.get("fecha_corte") or date.today().isoformat()
            if desde and (date.fromisoformat(corte) - date.fromisoformat(desde)).days < pol["dias_cuenta_nueva"]:
                subir("pendiente", f"El destino se registró hace menos de {pol['dias_cuenta_nueva']} días")

    if lote and tipo == "despachar_lote":
        lotes = {_norm(n): (n, d) for n, d in maestros.get("lotes", {}).items()}
        hallado = lotes.get(_norm(lote))
        registro = {_norm(n): d for n, d in maestros.get("destinos", {}).items()}.get(_norm(destino)) or {}
        if hallado is None:
            subir("pendiente", f"El lote {lote} no está en los datos maestros")
        elif not hallado[1].get("geolocalizado") and registro.get("region") == "UE":
            subir("bloqueada", f"Reglamento europeo contra la deforestación: el lote {hallado[0]} no tiene la geolocalización "
                               f"de sus fincas y '{destino}' está en la Unión Europea. Segunda opción: un comprador "
                               "en Estados Unidos, que no exige el polígono por finca")
        elif registro.get("region") == "Estados Unidos":
            subir("pendiente", f"Destino en Estados Unidos: no exige el polígono por finca, pero antes de despachar el "
                               f"lote {hallado[0]} hay que tener el registro de la instalación ante la FDA y enviar el "
                               "aviso previo (Prior Notice) del embarque")

    if monto is not None and rubro is not None:
        nombre, datos_rubro = rubro
        disponible = float(datos_rubro.get("disponible", 0))
        libre = disponible - comprometido
        if monto > libre:
            fmt = lambda v: f"{v:,.0f}".replace(",", ".")  # noqa: E731
            detalle = f"; {fmt(comprometido)} ya comprometidos en esta sesión" if comprometido else ""
            subir("bloqueada", f"El monto ({fmt(monto)}) supera el saldo disponible de '{nombre}' "
                               f"({fmt(max(0.0, libre))} libres de {fmt(disponible)}{detalle})")

    if monto is not None:
        pedidos = montos_pedidos(peticion)
        if pedidos and monto > max(pedidos) * (1 + pol["tolerancia_monto"]):
            subir("bloqueada", f"El monto ({monto:,.0f}) supera lo que pidió el usuario ({max(pedidos):,.0f})".replace(",", "."))
        if monto > pol["umbral_aprobacion"]:
            subir("pendiente", f"El monto supera el umbral de {pol['umbral_aprobacion']:,.0f}".replace(",", "."))

    if sensible and sesion in ("sospechosa", "detenida"):
        subir("bloqueada" if pol["sesion_sospechosa"] == "bloquear" else "pendiente",
              "En esta conversación se detectó un documento con instrucciones escondidas")
    if nivel == "confirmar_todo" or (sensible and nivel == "confirmar_sensibles"):
        subir("pendiente", f"'{tipo}' es una acción sensible: la decide una persona")
    if not motivos:
        motivos.append("Acción de bajo riesgo")
    return estado, motivos


def _norm_texto(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", (texto or "").lower()) if unicodedata.category(c) != "Mn")


def nueva_sesion() -> dict:
    return {"estado": "limpia", "motivos": [], "incidentes": 0}


def registrar_incidentes(sesion: dict, n: int, politica: dict | None = None) -> bool:
    """Suma n documentos con trampa a la sesión. Devuelve True si con esto la sesión quedó detenida.

    limpia -> sospechosa con el primero; -> detenida al llegar a parada_automatica (0 = nunca se detiene).
    Una sesión detenida solo vuelve a limpia cuando una persona la reinicia.
    """
    if n <= 0:
        return False
    tope = int((politica or cargar_politica()).get("parada_automatica") or 0)
    sesion["incidentes"] = sesion.get("incidentes", 0) + n
    antes = sesion["estado"]
    if tope and sesion["incidentes"] >= tope:
        sesion["estado"] = "detenida"
    elif antes == "limpia":
        sesion["estado"] = "sospechosa"
    if antes == "limpia":
        sesion["motivos"] = sesion.get("motivos", []) + ["Documento con instrucciones escondidas"]
    if sesion["estado"] == "detenida" and antes != "detenida":
        sesion["motivos"] = sesion.get("motivos", []) + [f"{sesion['incidentes']} intentos de engaño: sesión detenida"]
        return True
    return False


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
    canal: str = ""          # dónde se decidió: "página" o "Teams"
    comentario: str = ""     # lo que escribió quien decidió
    notificada: bool = False  # se avisó a Power Automate (NOTIFICAR_URL)
    token: str = field(default="", repr=False)  # código de un solo uso para aceptar la decisión desde Teams
    lote: str = ""
    documento: str = ""      # el documento de donde salió la acción (nombre y huella), si salió de uno
    resumen: str = ""        # los datos crudos para quien aprueba en Teams (no el resumen de la IA)

    def publica(self) -> dict:
        """Lo que se muestra por la API: todo menos el token."""
        return {**{k: v for k, v in asdict(self).items() if k != "token"}, "motivo": self.motivo}

    @property
    def motivo(self) -> str:
        return " · ".join(self.motivos)


class Bandeja:
    def __init__(self, bitacora=None):
        self.acciones: dict[int, Accion] = {}
        self._ids = itertools.count(1)
        self.bitacora = bitacora

    def proponer(self, tipo: str, detalle: str, monto: float | None = None, destino: str = "", cuenta: str = "",
                 peticion: str = "", solicitante: str = "asistente", sesion: str = "limpia", lote: str = "",
                 documento: str = "") -> Accion:
        # Lo ya comprometido con el mismo destino en esta sesión (para el saldo de un rubro con presupuesto)
        comprometido = sum(a.monto or 0 for a in self.acciones.values()
                           if _norm(a.destino) == _norm(destino) and a.estado in ("permitida", "pendiente", "aprobada"))
        estado, motivos = revisar_accion(tipo, monto, destino, cuenta, peticion, sesion, comprometido=comprometido,
                                         lote=lote)
        a = Accion(next(self._ids), tipo, detalle, monto, destino, cuenta, peticion, solicitante or "asistente",
                   estado, motivos, lote=lote, documento=documento)
        a.resumen = resumen_para_aprobar(a)
        self.acciones[a.id] = a
        if self.bitacora:
            datos = {k: v for k, v in asdict(a).items() if k not in ("creada", "token", "notificada", "canal", "comentario", "resumen")}
            self.bitacora.registrar("accion_propuesta", proteger(datos, ("detalle", "peticion", "cuenta")))
        if estado == "pendiente":
            a.token = secrets.token_urlsafe(16)
            a.notificada = notificar(a)
            if a.notificada and self.bitacora:
                self.bitacora.registrar("accion_enviada_a_teams", {"id": a.id})
        return a

    def decidir(self, id_: int, aprobar: bool, aprobador: str = "persona", canal: str = "página",
                comentario: str = "") -> Accion:
        a = self.acciones[id_]
        if not _norm(aprobador):
            raise ValueError("Falta el nombre de quien aprueba")
        if a.estado != "pendiente":
            raise ValueError(f"La acción {id_} está {a.estado}: solo se deciden las pendientes")
        pol = cargar_politica()
        if pol["segregacion_de_funciones"] and _norm(aprobador) == _norm(a.solicitante):
            raise ValueError("Quien pidió la acción no puede aprobarla (segregación de funciones)")
        a.estado, a.decidida_por, a.canal, a.comentario = ("aprobada" if aprobar else "rechazada"), aprobador, canal, comentario
        a.token = ""  # ya no sirve: una decisión por acción
        if self.bitacora:
            self.bitacora.registrar("accion_decidida", {"id": a.id, "estado": a.estado, "aprobador": aprobador, "canal": canal,
                                                        **({"comentario": comentario} if comentario else {})})
        return a

    def lista(self) -> list[dict]:
        return [a.publica() for a in sorted(self.acciones.values(), key=lambda x: -x.id)]


def _monto(v: float) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".").removesuffix(",00")


def resumen_para_aprobar(a: Accion, maestros: dict | None = None) -> str:
    """Lo que ve quien aprueba en Teams: los datos crudos y su contraste con los datos maestros, no un resumen de la IA
    (OWASP: quien aprueba tiende a confiar en un resumen convincente). Markdown simple, que Teams muestra bien."""
    maestros = maestros if maestros is not None else cargar_maestros()
    registro = {_norm(n): d for n, d in maestros.get("destinos", {}).items()}.get(_norm(a.destino)) or {}
    lineas = [f"**{a.tipo.replace('_', ' ').capitalize()}** · {a.detalle}"]
    if a.monto is not None:
        lineas.append(f"- Monto: {_monto(a.monto)}")
    if a.destino:
        lineas.append(f"- Destino: {a.destino}" + ("" if registro else " (NO está en los datos maestros)"))
    if a.cuenta:
        registrada = registro.get("cuenta", "")
        igual = registrada and _norm(registrada) == _norm(a.cuenta)
        lineas.append(f"- Cuenta pedida: {a.cuenta} · registrada: {registrada or 'ninguna'}"
                      f"{' · coincide' if igual else ' · NO COINCIDE'}")
    if a.lote:
        datos = {_norm(n): d for n, d in maestros.get("lotes", {}).items()}.get(_norm(a.lote))
        geo = "sin datos" if datos is None else ("sí" if datos.get("geolocalizado") else "NO")
        lineas.append(f"- Lote: {a.lote} · geolocalización: {geo}" + (f" · destino en {registro['region']}" if registro.get("region") else ""))
    if a.documento:
        lineas.append(f"- Origen: {a.documento}")
    lineas.append(f"- Lo pidió: {a.solicitante}" + (f" · «{a.peticion[:120]}»" if a.peticion else ""))
    lineas.append(f"- Guardián: {a.estado} · {a.motivo}")
    return "\n".join(lineas)


def notificar(accion: Accion) -> bool:
    """Envía la acción pendiente a NOTIFICAR_URL si existe. Nunca bloquea la demo si falla."""
    url = os.environ.get("NOTIFICAR_URL")
    if not url:
        return False
    try:
        cuerpo = {**{k: v for k, v in asdict(accion).items() if k not in ("notificada", "canal", "comentario")},
                  "motivo": accion.motivo}  # incluye el token: lo devuelve el flujo con la decisión
        req = urllib.request.Request(url, data=json.dumps(cuerpo, ensure_ascii=False).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10).close()
        return True
    except Exception:  # noqa: BLE001
        return False
