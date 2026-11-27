"""Trae las cifras verificadas desde Snowflake: una consulta → cifras.csv → sello de integridad → bitácora.

Por qué una copia sellada y no una consulta en vivo en cada pregunta: así cada respuesta sale de una versión
conocida de los datos (con su huella), la demo no depende de la red, y si alguien cambia los datos en Snowflake
el equipo lo sabe al volver a traerlos. "Snowflake es la fuente única de la verdad; el kit trabaja sobre una
versión sellada de esa verdad."

Uso (desde la raíz del repo):
  pip install snowflake-connector-python
  python -m kit.snowflake traer                                   # SELECT * FROM CIFRAS
  python -m kit.snowflake traer --consulta "SELECT ... FROM CAFE.PUBLIC.CIFRAS"
  KIT_DATOS=casos/cafe python -m kit.snowflake traer              # escribe en la carpeta de ese caso

Variables (en .env):
  SNOWFLAKE_ACCOUNT    el identificador de la cuenta: lo que va antes de .snowflakecomputing.com en su URL
  SNOWFLAKE_USER       su usuario
  SNOWFLAKE_PASSWORD   su contraseña (o deje vacío y use SNOWFLAKE_AUTHENTICATOR=externalbrowser para entrar
                       con el navegador; sirve si la cuenta pide verificación en dos pasos)
  SNOWFLAKE_WAREHOUSE  por defecto COMPUTE_WH
  SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA   por ejemplo CAFE y PUBLIC

La consulta debe devolver las columnas de cifras.csv: clave, descripcion, valor, unidad y, si las tiene,
decimales, fuente y sinonimos (en mayúsculas o minúsculas, da igual). Si falta la fuente, se pone
"Snowflake: <base>.<esquema>, consultado el <fecha>".
"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime

from .cifras import carpeta_datos

COLUMNAS = ["clave", "descripcion", "valor", "unidad", "decimales", "fuente", "sinonimos"]
OBLIGATORIAS = {"clave", "descripcion", "valor", "unidad"}


def conectar():
    import warnings
    # Aviso de la librería sobre un cambio futuro de su comportamiento al cerrar: no afecta y ensucia la demo.
    warnings.filterwarnings("ignore", category=FutureWarning, module=r"snowflake\.connector")
    try:
        import snowflake.connector as sf
    except ImportError as e:
        raise SystemExit("Falta el conector: pip install snowflake-connector-python") from e
    faltan = [v for v in ("SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER") if not os.environ.get(v)]
    if faltan:
        raise SystemExit("Faltan variables en .env: " + ", ".join(faltan))
    params = {"account": os.environ["SNOWFLAKE_ACCOUNT"], "user": os.environ["SNOWFLAKE_USER"],
              "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE") or "COMPUTE_WH",
              "database": os.environ.get("SNOWFLAKE_DATABASE") or None, "schema": os.environ.get("SNOWFLAKE_SCHEMA") or None,
              "application": "lead-aspire-kit", "login_timeout": 60}
    if os.environ.get("SNOWFLAKE_AUTHENTICATOR"):
        params["authenticator"] = os.environ["SNOWFLAKE_AUTHENTICATOR"]
    if os.environ.get("SNOWFLAKE_PASSWORD"):
        params["password"] = os.environ["SNOWFLAKE_PASSWORD"]
    return sf.connect(**{k: v for k, v in params.items() if v is not None})


def filas_desde_snowflake(consulta: str, conexion=None) -> list[dict]:
    """Corre la consulta (solo lectura) y devuelve las filas con las columnas de cifras.csv."""
    if not re.match(r"^\s*(select|with)\b", consulta, re.I) or ";" in consulta.strip().rstrip(";"):
        raise ValueError("Solo se permite una consulta de lectura (SELECT o WITH)")
    con = conexion or conectar()
    try:
        cur = con.cursor()
        cur.execute(consulta)
        nombres = [d[0].lower() for d in cur.description]
        faltan = OBLIGATORIAS - set(nombres)
        if faltan:
            raise ValueError(f"A la consulta le faltan columnas: {', '.join(sorted(faltan))}")
        filas = [dict(zip(nombres, f)) for f in cur.fetchall()]
    finally:
        if conexion is None:
            con.close()
    return filas


def escribir_cifras(filas: list[dict], origen: str) -> tuple[int, str]:
    """Valida y escribe cifras.csv en la carpeta del caso activo. Devuelve (filas, ruta)."""
    if not filas:
        raise ValueError("La consulta no devolvió filas: no se reemplaza cifras.csv")
    claves = set()
    limpias = []
    for f in filas:
        clave = str(f.get("clave") or "").strip()
        if not re.fullmatch(r"[a-zA-Z0-9_]+", clave):
            raise ValueError(f"Clave inválida: {clave!r} (solo letras, números y _)")
        if clave in claves:
            raise ValueError(f"Clave repetida: {clave}")
        claves.add(clave)
        try:
            valor = float(f["valor"])
        except (TypeError, ValueError) as e:
            raise ValueError(f"El valor de {clave} no es un número: {f['valor']!r}") from e
        limpias.append({"clave": clave, "descripcion": str(f.get("descripcion") or "").strip(), "valor": str(int(valor)) if valor.is_integer() else repr(valor),
                        "unidad": str(f.get("unidad") or "").strip(), "decimales": int(f.get("decimales") or 0),
                        "fuente": str(f.get("fuente") or "").strip() or origen, "sinonimos": str(f.get("sinonimos") or "").strip()})
    ruta = carpeta_datos() / "cifras.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(limpias)
    return len(limpias), str(ruta)


def traer(consulta: str, sellar: bool = True, conexion=None) -> dict:
    from . import integridad
    from .bitacora import Bitacora
    origen = (f"Snowflake: {os.environ.get('SNOWFLAKE_DATABASE', '?')}.{os.environ.get('SNOWFLAKE_SCHEMA', '?')}, "
              f"consultado el {datetime.now():%Y-%m-%d %H:%M}")
    n, ruta = escribir_cifras(filas_desde_snowflake(consulta, conexion), origen)
    if sellar:
        integridad.sellar()
    huella = integridad.huellas().get("cifras.csv", "")
    Bitacora().registrar("datos_desde_snowflake", {"filas": n, "consulta": consulta[:300], "huella_cifras": huella,
                                                   "sellado": sellar})
    return {"filas": n, "ruta": ruta, "huella": huella, "sellado": sellar}


TABLA_EVENTOS = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*(\.[A-Za-z_][A-Za-z0-9_$]*){0,2}$")


def guardar_eventos(eventos: list[dict], conexion=None) -> int:
    """Escribe eventos del acopio (EPCIS) en la tabla SNOWFLAKE_TABLA_EVENTOS. La escribe el código, nunca el modelo.

    Tabla: casos/cafe/snowflake_eventos.sql. Usen un usuario con permiso solo de INSERT en esa tabla.
    """
    tabla = os.environ.get("SNOWFLAKE_TABLA_EVENTOS", "")
    if not TABLA_EVENTOS.match(tabla):
        raise ValueError("SNOWFLAKE_TABLA_EVENTOS no está definida o no es un nombre de tabla válido")
    import json
    filas = [(e["eventID"], e["eventTime"], e["ilmd"]["lote"], e["quantityList"][0]["epcClass"].removeprefix("finca:"),
              e["quantityList"][0]["quantity"], e["ilmd"]["humedad_pct"], e["ilmd"]["apto_ue"], e["ilmd"]["canal"],
              json.dumps(e, ensure_ascii=False)) for e in eventos]
    con = conexion or conectar()
    try:
        cur = con.cursor()
        cur.executemany(f"INSERT INTO {tabla} (EVENT_ID, EVENT_TIME, LOTE, FINCA_ID, KG, HUMEDAD_PCT, APTO_UE, CANAL, "
                        "EVENTO_JSON) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", filas)
    finally:
        if conexion is None:
            con.close()
    return len(filas)


def main(argv: list[str]) -> int:
    from . import cargar_env
    cargar_env()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("orden", choices=["traer"])
    p.add_argument("--consulta", default="SELECT * FROM CIFRAS")
    p.add_argument("--sin-sellar", action="store_true", help="no sella los datos después de traerlos")
    a = p.parse_args(argv)
    r = traer(a.consulta, sellar=not a.sin_sellar)
    print(f"{r['filas']} cifras traídas de Snowflake a {r['ruta']}"
          f"{' y selladas' if r['sellado'] else ''} (huella {r['huella'][:12]}…). Quedó registrado en la bitácora.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
