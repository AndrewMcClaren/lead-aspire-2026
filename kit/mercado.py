"""Datos oficiales de mercado: tasa de cambio y precio del café, traídos de su fuente, sellados y registrados.

Fuentes, sin clave ni registro:
  - TRM (tasa de cambio representativa del mercado): Superintendencia Financiera, publicada en datos.gov.co con la
    API abierta de Socrata (conjunto 32sa-8pi3). https://www.datos.gov.co/resource/32sa-8pi3.json
  - Precio del café: la Federación Nacional de Cafeteros publica cada día hábil un PDF con el cierre del contrato C en
    Nueva York y el precio interno de referencia. No tiene API: el PDF trae texto y se lee con reglas.
    https://federaciondecafeteros.org/wp-content/uploads/2026/03/precio_cafe.pdf

Uso (desde la raíz del repo; necesita internet):
  KIT_DATOS=casos/cafe python -m kit.mercado actualizar     # pone TRM, contrato C y precio interno en cifras.csv y sella
  python -m kit.mercado trm --desde 2025-12-01 --csv plantillas/powerbi/datos/trm_oficial.csv   # serie para Power BI

Igual que con Snowflake: el asistente no consulta internet en cada pregunta. Trabaja sobre una copia sellada de los
datos oficiales, con la fecha y la fuente de cada cifra, y queda en la bitácora cuándo se trajeron.
Si una fuente no responde, no se toca nada: se conserva la cifra anterior.
"""

import argparse
import csv
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime

TRM_API = "https://www.datos.gov.co/resource/32sa-8pi3.json"
PRECIO_FNC = "https://federaciondecafeteros.org/wp-content/uploads/2026/03/precio_cafe.pdf"
MESES = {m: i for i, m in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                      "septiembre", "octubre", "noviembre", "diciembre"], 1)}
AGENTE = {"User-Agent": "lead-aspire-kit/1.0 (proyecto estudiantil)"}


def _get(url: str, timeout: int = 30) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENTE), timeout=timeout) as r:
        return r.read()


# ------------------------------------------------------------------------------------------------ TRM
def trm_serie(desde: str, hasta: str | None = None) -> list[dict]:
    """[{"fecha": "2026-11-25", "trm": 3592.03}, ...] ordenada por fecha. Cada fila vale desde 'vigenciadesde'."""
    donde = f"vigenciadesde >= '{date.fromisoformat(desde).isoformat()}T00:00:00'"
    if hasta:
        donde += f" AND vigenciadesde <= '{date.fromisoformat(hasta).isoformat()}T00:00:00'"
    q = urllib.parse.urlencode({"$select": "valor,vigenciadesde,vigenciahasta", "$where": donde,
                                "$order": "vigenciadesde", "$limit": 5000})
    filas = json.loads(_get(f"{TRM_API}?{q}"))
    return [{"fecha": f["vigenciadesde"][:10], "hasta": f["vigenciahasta"][:10], "trm": float(f["valor"])} for f in filas]


def trm_vigente(dia: date | None = None) -> dict:
    """La TRM vigente un día (por defecto hoy): la última publicada con vigencia desde ese día o antes."""
    dia = dia or date.today()
    q = urllib.parse.urlencode({"$where": f"vigenciadesde <= '{dia.isoformat()}T00:00:00'", "$order": "vigenciadesde DESC",
                                "$limit": 1})
    f = json.loads(_get(f"{TRM_API}?{q}"))[0]
    return {"fecha": f["vigenciadesde"][:10], "hasta": f["vigenciahasta"][:10], "trm": float(f["valor"])}


# --------------------------------------------------------------------------------------- precio FNC
def leer_precio_fnc(pdf: bytes) -> dict:
    """Del PDF diario de la Federación: fecha, cierre del contrato C (centavos de dólar por libra) y precio interno."""
    from pypdf import PdfReader
    return leer_texto_fnc("\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(pdf)).pages))


def leer_texto_fnc(texto: str) -> dict:
    m_fecha = re.search(r"(?i)\b(" + "|".join(MESES) + r")\s+(\d{1,2})\s*/\s*(\d{4})", texto)
    m_c = re.search(r"(?i)cierre contrato c[^\d]*([\d.,]+)\s*us\s*cent", texto)
    m_int = re.search(r"(?i)precio total por carga de 125 ?kg[^\n]*?([\d.,]{7,})\s*cop", texto)
    if not (m_fecha and m_c and m_int):
        raise ValueError("El PDF de la Federación cambió de formato: no se encontró la fecha, el contrato C o el precio interno")
    fecha = date(int(m_fecha.group(3)), MESES[m_fecha.group(1).lower()], int(m_fecha.group(2)))
    centavos = float(m_c.group(1).replace(",", ""))
    interno = int(re.sub(r"\D", "", m_int.group(1)))
    return {"fecha": fecha.isoformat(), "contrato_c_usd_lb": round(centavos / 100, 4), "precio_interno_cop_carga": interno}


def precio_fnc() -> dict:
    return leer_precio_fnc(_get(PRECIO_FNC))


# ------------------------------------------------------------------------------------------ cifras
def _fecha_larga(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} de {[m for m, i in MESES.items() if i == d.month][0]} de {d.year}"


def filas_de_mercado(precio: dict | None, trm: dict | None, consultado: str) -> list[dict]:
    filas = []
    if precio:
        fuente = (f"Federación Nacional de Cafeteros, precio de referencia del {precio['fecha']} (dato oficial de mercado, "
                  f"consultado el {consultado}): federaciondecafeteros.org")
        filas += [
            {"clave": "precio_contrato_c_usd_lb", "valor": precio["contrato_c_usd_lb"], "unidad": "dólares por libra",
             "decimales": 2, "fuente": fuente,
             "descripcion": f"Precio del contrato C de café arábica en la bolsa de Nueva York al cierre del {_fecha_larga(precio['fecha'])}",
             "sinonimos": "precio bolsa contrato c nueva york cotizacion libra cierre hoy mercado"},
            {"clave": "precio_interno_cop_carga", "valor": precio["precio_interno_cop_carga"], "unidad": "pesos por carga",
             "decimales": 0, "fuente": fuente,
             "descripcion": ("Precio interno de referencia de la carga de 125 kg de café pergamino seco publicado por la "
                             f"Federación el {_fecha_larga(precio['fecha'])}"),
             "sinonimos": "precio interno carga pesos federacion productor caficultor referencia pergamino"}]
    if trm:
        filas.append({"clave": "trm_cop_usd", "valor": trm["trm"], "unidad": "pesos por dólar", "decimales": 2,
                      "descripcion": f"Tasa de cambio representativa del mercado (TRM) vigente el {_fecha_larga(trm['fecha'])}",
                      "fuente": (f"Superintendencia Financiera, TRM publicada en datos.gov.co (API 32sa-8pi3), consultada el "
                                 f"{consultado} (dato oficial)"),
                      "sinonimos": "trm tasa de cambio dolar peso cuanto vale el dolar divisa"})
    return filas


def actualizar_cifras(filas: list[dict]) -> str:
    """Reemplaza (o agrega) esas claves en cifras.csv del caso activo, sin tocar las demás."""
    from .cifras import carpeta_datos
    from .snowflake import COLUMNAS
    ruta = carpeta_datos() / "cifras.csv"
    with open(ruta, encoding="utf-8") as fh:
        actuales = list(csv.DictReader(fh))
    nuevas = {f["clave"]: f for f in filas}
    salida = [nuevas.pop(f["clave"], f) for f in actuales] + list(nuevas.values())
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS, extrasaction="ignore")
        w.writeheader()
        for f in salida:
            valor = float(f["valor"])
            w.writerow({**{k: f.get(k, "") for k in COLUMNAS}, "valor": str(int(valor)) if valor.is_integer() else repr(valor)})
    return str(ruta)


def actualizar(sellar: bool = True) -> dict:
    from . import integridad
    from .bitacora import Bitacora
    consultado = datetime.now().strftime("%Y-%m-%d %H:%M")
    errores, precio, trm = [], None, None
    try:
        precio = precio_fnc()
    except Exception as e:  # noqa: BLE001 - si una fuente falla, se conserva la cifra anterior
        errores.append(f"Precio de la Federación: {type(e).__name__}: {e}")
    try:
        trm = trm_vigente()
    except Exception as e:  # noqa: BLE001
        errores.append(f"TRM de datos.gov.co: {type(e).__name__}: {e}")
    filas = filas_de_mercado(precio, trm, consultado)
    ruta = actualizar_cifras(filas) if filas else ""
    if filas and sellar:
        integridad.sellar()
    Bitacora().registrar("datos_de_mercado", {"claves": [f["clave"] for f in filas], "precio": precio, "trm": trm,
                                              "errores": errores, "sellado": bool(filas and sellar)})
    return {"filas": filas, "ruta": ruta, "errores": errores, "precio": precio, "trm": trm}


def main(argv: list[str]) -> int:
    from . import cargar_env
    cargar_env()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("orden", choices=["actualizar", "trm", "precio"])
    p.add_argument("--desde", default="2025-12-01")
    p.add_argument("--hasta")
    p.add_argument("--csv", help="con 'trm': archivo donde guardar la serie")
    a = p.parse_args(argv)
    if a.orden == "precio":
        print(json.dumps(precio_fnc(), ensure_ascii=False))
    elif a.orden == "trm":
        serie = trm_serie(a.desde, a.hasta)
        if a.csv:
            with open(a.csv, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=["fecha", "hasta", "trm"])
                w.writeheader()
                w.writerows(serie)
            print(f"{len(serie)} días de TRM oficial guardados en {a.csv} (del {serie[0]['fecha']} al {serie[-1]['fecha']}).")
        else:
            print(json.dumps(serie[-5:], ensure_ascii=False, indent=1))
    else:
        r = actualizar()
        for f in r["filas"]:
            print(f"  {f['clave']}: {f['valor']} {f['unidad']} · {f['descripcion']}")
        for e in r["errores"]:
            print(f"  No se actualizó: {e}")
        print(f"{len(r['filas'])} cifras oficiales en {r['ruta'] or '(nada cambió)'}"
              f"{', selladas' if r['filas'] else ''}. Quedó registrado en la bitácora.")
        return 0 if r["filas"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
