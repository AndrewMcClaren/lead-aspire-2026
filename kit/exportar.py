"""Exportar café: cotizador de costo y tiempo por mercado, validación de cifras imposibles y conocimiento del comprador.

Todo es código, sin IA: así cada número sale de una regla que se puede revisar. Los supuestos viven en el archivo
mercados.json del caso (casos/cafe/mercados.json): lo que tiene fuente es dato verificado; los fletes y trámites son
valores de ejemplo que se cambian por la cotización real de una naviera o agente de carga.

Uso desde Python:
    from kit.exportar import cotizar, conocer_comprador
    cotizar("china", sacos=10)
    conocer_comprador("Importadora Ejemplo GmbH")
"""

import json
import math
from datetime import date

from .cifras import Tabla, carpeta_datos, formatear

LB_POR_KG = 2.20462


def cargar_mercados() -> dict:
    ruta = carpeta_datos() / "mercados.json"
    if not ruta.exists():
        raise FileNotFoundError("Este caso no tiene mercados.json (el cotizador está en el caso del café: KIT_DATOS=casos/cafe)")
    return json.loads(ruta.read_text(encoding="utf-8"))


def _precio_c(tabla: Tabla | None = None) -> tuple[float, str]:
    """El contrato C de las cifras verificadas (el que trae kit.mercado), con su descripción y fuente."""
    tabla = tabla or Tabla()
    c = tabla.cifras.get("precio_contrato_c_usd_lb")
    if c is None:
        raise ValueError("Falta la cifra precio_contrato_c_usd_lb: corran python -m kit.mercado actualizar")
    return c.valor, f"{c.descripcion} ({c.fuente})"


def validar_volumen(sacos: float, produccion_sacos_mes: float | None, m: dict, kg_saco: float) -> list[dict]:
    """Cifras imposibles o poco realistas, comparadas con el país entero. Devuelve alertas."""
    col = m["colombia"]
    nacional = col["produccion_sacos_60kg_anio"]
    alertas = []

    def contra_el_pais(sacos_anio_60kg: float, que: str):
        veces = sacos_anio_60kg / nacional
        if veces >= 1:
            ha = sacos_anio_60kg / col["productividad_sacos_ha_anio"]
            alertas.append({"nivel": "alta", "texto":
                f"{que} equivale a {formatear(veces, 1)} veces todo el café que produce Colombia en un año "
                f"({formatear(nacional)} sacos de 60 kg). Necesitaría unas {formatear(ha)} hectáreas y el país tiene "
                f"{formatear(col['area_ha'])}. Revisen la unidad: ¿sacos al año, kilos o arrobas?"})
        elif veces >= 0.05:
            alertas.append({"nivel": "media", "texto":
                f"{que} sería el {formatear(veces * 100, 1)} % de la producción nacional: es volumen de los exportadores más grandes del país."})

    if produccion_sacos_mes:
        contra_el_pais(produccion_sacos_mes * 12, f"Producir {formatear(produccion_sacos_mes)} sacos al mes")
    contra_el_pais(sacos * kg_saco / 60, f"Exportar {formatear(sacos)} sacos de {kg_saco:g} kg")
    if produccion_sacos_mes and sacos * kg_saco / 60 > produccion_sacos_mes * 12:
        alertas.append({"nivel": "media", "texto": "Quieren exportar más de lo que la finca produce en un año: tendrían que comprar café a terceros."})
    return alertas


def cotizar(destino: str, sacos: float, tipo: str = "excelso", produccion_sacos_mes: float | None = None,
            tabla: Tabla | None = None) -> dict:
    """Costo y tiempo aproximados de poner N sacos de café verde en un mercado. Devuelve el desglose y sus supuestos."""
    m = cargar_mercados()
    if destino not in m["destinos"]:
        raise ValueError(f"Destino desconocido: {destino}. Opciones: {', '.join(m['destinos'])}")
    if not (isinstance(sacos, (int, float)) and 0 < sacos < 1e9):
        raise ValueError("La cantidad de sacos debe ser un número mayor que cero")
    d, s = m["destinos"][destino], m["supuestos"]
    kg_saco = s["kg_por_saco_exportacion"]
    kg = sacos * kg_saco
    lb = kg * LB_POR_KG
    precio_c, fuente_c = _precio_c(tabla)
    diferencial = s["diferenciales_usd_lb"].get(tipo, s["diferenciales_usd_lb"]["excelso"])

    # Modalidad de transporte según el volumen
    if sacos <= s["maximo_sacos_aereo"]:
        modalidad = "aéreo (muestras o microlote)"
        flete = kg * d["aereo_usd_kg"]
        transito = d["transito_aereo_dias"]
        espera = [0, 2]
    elif sacos < s["minimo_sacos_contenedor"]:
        modalidad = "carga consolidada (LCL): comparte contenedor con otros"
        flete = max(1.0, sacos * s["m3_por_saco"]) * d["lcl_usd_m3"]
        transito = d["transito_dias"]
        espera = s["dias_consolidacion_lcl"]
    else:
        contenedores = math.ceil(sacos / s["sacos_por_contenedor_20"])
        modalidad = f"{contenedores} contenedor{'es' if contenedores > 1 else ''} de 20 pies ({s['sacos_por_contenedor_20']} sacos cada uno)"
        flete = contenedores * d["flete_contenedor_20_usd"]
        transito = d["transito_dias"]
        espera = [0, 0]

    cafe = (precio_c + diferencial) * lb
    contribucion = m["colombia"]["contribucion_usd_lb"] * lb
    interno = sacos * s["transporte_interno_usd_saco"]
    tramites = s["tramites_por_embarque_usd"]
    fob = cafe + contribucion + interno + tramites
    seguro = (fob + flete) * s["seguro_pct_cif"] / 100
    cif = fob + flete + seguro
    arancel = cif * d["arancel_verde_pct"] / 100
    total = cif + arancel

    dias_doc = 6
    t = tabla or Tabla()
    if "dias_documentos_embarque" in t.cifras:
        dias_doc = int(t.cifras["dias_documentos_embarque"].valor)
    minimo = s["dias_preparacion"][0] + espera[0] + transito[0]
    maximo = s["dias_preparacion"][1] + max(dias_doc, 0) + espera[1] + transito[1]

    costos = [
        {"concepto": f"Café verde: {formatear(lb)} lb × (contrato C {formatear(precio_c, 2)} + diferencial "
                     f"{formatear(diferencial, 2)}) USD/lb", "usd": cafe,
         "fuente": f"{fuente_c}; diferencial: {s['diferencial_referencia']}"},
        {"concepto": "Contribución cafetera", "usd": contribucion, "fuente": m["colombia"]["contribucion_fuente"]},
        {"concepto": "Transporte interno a puerto", "usd": interno, "fuente": "ejemplo editable"},
        {"concepto": "Trámites del embarque (anuncio, certificados, agencia de aduanas)", "usd": tramites, "fuente": "ejemplo editable"},
        {"concepto": f"Flete internacional ({modalidad})", "usd": flete, "fuente": "ejemplo editable: cotizar con naviera o agente de carga"},
        {"concepto": f"Seguro ({formatear(s['seguro_pct_cif'], 2)} % del valor)", "usd": seguro, "fuente": "ejemplo editable"},
        {"concepto": f"Arancel en destino ({d['arancel_verde_pct']} %)", "usd": arancel, "fuente": d["arancel_fuente"]},
    ]
    for c in costos:
        c["usd"] = round(c["usd"], 2)
    alertas = validar_volumen(sacos, produccion_sacos_mes, m, kg_saco)
    if d["arancel_verde_pct"] and "VERIFICAR" in d["arancel_fuente"]:
        alertas.append({"nivel": "media", "texto": f"El arancel de {d['nombre']} ({d['arancel_verde_pct']} %) hay que verificarlo antes de cotizar."})
    if sacos <= s["maximo_sacos_aereo"]:
        alertas.append({"nivel": "info", "texto": "Con tan pocos sacos el flete pesa mucho en el precio: es la escala de una muestra o un microlote de café especial. Un contenedor lleva unos 275 sacos de 70 kg."})
    return {
        "destino": d["nombre"], "sacos": sacos, "kg": round(kg), "lb": round(lb), "tipo": tipo, "modalidad": modalidad,
        "ruta": f"{d['puerto_origen']} → {d['puerto_destino']}",
        "dias": [minimo, maximo], "costos": costos, "fob_usd": round(fob, 2), "cif_usd": round(cif, 2),
        "total_usd": round(total, 2), "usd_por_lb": round(total / lb, 3), "usd_por_kg": round(total / kg, 2),
        "contrato_c_usd_lb": precio_c, "requisitos": d["requisitos"], "certificaciones": d["certificaciones_frecuentes"],
        "participacion_pct": d["participacion_pct"], "participacion_fuente": d["participacion_fuente"],
        "alertas": alertas, "nota": s["nota_valores"],
    }


def mercados() -> dict:
    """Resumen para la página: destinos con demanda, arancel, tránsito y requisitos; y los pasos para exportar."""
    m = cargar_mercados()
    destinos = [{"id": k, "nombre": d["nombre"], "participacion_pct": d["participacion_pct"], "arancel_verde_pct": d["arancel_verde_pct"],
                 "transito_dias": d["transito_dias"], "requisitos": d["requisitos"], "fuente": d["participacion_fuente"]}
                for k, d in m["destinos"].items()]
    return {"destinos": sorted(destinos, key=lambda x: -x["participacion_pct"]), "pasos": m["pasos"],
            "produccion_nacional": m["colombia"]["produccion_sacos_60kg_anio"], "produccion_fuente": m["colombia"]["produccion_fuente"]}


LISTA_KYC = [
    "Existencia legal: registro mercantil del país del comprador y su número de identificación tributaria",
    "Referencias comerciales y bancarias; pedir estados financieros si el monto es grande",
    "Revisar listas restrictivas (OFAC de EE. UU., ONU, UE) en sus portales oficiales: este kit no las consulta",
    "Confirmar datos y cuentas por un canal conocido (el teléfono registrado), nunca por el que viene en el correo",
    "Contrato con calidad, cantidad, precio, Incoterm, fecha de embarque, arbitraje (contratos tipo GCA o ECF) y forma de pago",
]


def conocer_comprador(nombre: str, cuenta: str = "", maestros: dict | None = None) -> dict:
    """Conocimiento del cliente contra los datos maestros: ¿está registrado?, ¿desde cuándo?, ¿la cuenta coincide?
    y qué forma de pago conviene. No reemplaza revisar las listas restrictivas oficiales."""
    from .aprobacion import _norm, cargar_maestros
    maestros = maestros if maestros is not None else cargar_maestros()
    registros = {_norm(n): (n, d) for n, d in maestros.get("destinos", {}).items()}
    hallado = registros.get(_norm(nombre))
    if hallado is None:
        parecidos = [n for k, (n, _) in registros.items() if _norm(nombre) and (_norm(nombre) in k or k in _norm(nombre))]
        return {"estado": "desconocido", "nombre": nombre, "parecidos": parecidos,
                "recomendacion": "Comprador nuevo: pago anticipado o carta de crédito irrevocable y confirmada por un banco en "
                                 "Colombia. No despachar con pago contra documentos ni a plazo hasta completar la verificación.",
                "motivos": ["No está en los datos maestros"] + ([f"Se parece a: {', '.join(parecidos)} (¿suplantación?)"] if parecidos else []),
                "lista": LISTA_KYC}
    real, datos = hallado
    corte = date.fromisoformat(maestros.get("fecha_corte") or date.today().isoformat())
    dias = (corte - date.fromisoformat(datos["desde"])).days if datos.get("desde") else None
    motivos = [f"Registrado desde {datos.get('desde', '¿?')}" + (f" ({dias} días)" if dias is not None else ""),
               f"Región: {datos.get('region', 'sin dato')}"]
    estado = "registrado"
    if cuenta and datos.get("cuenta") and _norm(cuenta) != _norm(datos["cuenta"]):
        estado = "alerta"
        motivos.append(f"La cuenta {cuenta} NO es la registrada ({datos['cuenta']}): posible fraude por cambio de cuenta")
    if dias is not None and dias < 30:
        estado = "alerta" if estado == "alerta" else "nuevo"
        motivos.append("Registrado hace menos de 30 días: tratarlo como comprador nuevo")
    recomendacion = {
        "registrado": "Comprador conocido: se puede negociar pago contra documentos; para montos altos, mantener carta de crédito.",
        "nuevo": "Relación reciente: carta de crédito irrevocable y confirmada hasta tener historial.",
        "alerta": "No despachar ni cambiar datos de pago: verificar por el canal registrado y escalar a Tesorería.",
    }[estado]
    return {"estado": estado, "nombre": real, "recomendacion": recomendacion, "motivos": motivos, "lista": LISTA_KYC}
