"""Entregas del acopio en Azure SQL Database: una tabla que la exportadora puede consultar, exportar o conectar a Power BI.

Cada entrega verificada (evento EPCIS) se guarda en la tabla dbo.EventosAcopio, además del archivo local y la bitácora.
La escribe el código, nunca el modelo. Si la base no responde, el acopio sigue y el error queda en la bitácora.

Sin contraseñas: se entra con Microsoft Entra ID.
  - En Azure App Service, con la identidad administrada de la aplicación.
  - En este computador, con la sesión de `az login`.

Variables (.env o configuración de la aplicación en Azure):
  AZURE_SQL_SERVER=mi-servidor.database.windows.net
  AZURE_SQL_DATABASE=acopio

Comandos:
  python -m kit.sqlazure crear     crea la tabla y la vista (si no existen)
  python -m kit.sqlazure subir     sube las entregas del archivo local que aún no estén en la tabla
  python -m kit.sqlazure ver       muestra las últimas entregas y el resumen por lote

Tabla y vista: casos/cafe/azure_sql_eventos.sql
"""

import argparse
import json
import os
import struct
import subprocess
import sys
import urllib.parse
import urllib.request

RECURSO = "https://database.windows.net/"
TABLA = "dbo.EventosAcopio"
_ACCESS_TOKEN = 1256  # SQL_COPT_SS_ACCESS_TOKEN del controlador ODBC de SQL Server

CREAR = [
    """IF OBJECT_ID('dbo.EventosAcopio', 'U') IS NULL
CREATE TABLE dbo.EventosAcopio (
    EventId        NVARCHAR(64)   NOT NULL PRIMARY KEY,
    FechaEvento    DATETIMEOFFSET NOT NULL,
    Lote           NVARCHAR(32)   NOT NULL,
    FincaId        NVARCHAR(32)   NOT NULL,
    Finca          NVARCHAR(100)  NULL,
    Kg             DECIMAL(12, 1) NOT NULL,
    CantidadReportada NVARCHAR(50) NULL,
    HumedadPct     DECIMAL(5, 2)  NULL,
    AptoUE         BIT            NOT NULL,
    Canal          NVARCHAR(40)   NULL,
    Remitente      NVARCHAR(64)   NULL,   -- huella del teléfono, nunca el número
    EventoJson     NVARCHAR(MAX)  NOT NULL,
    Cargado        DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET()
)""",
    """CREATE OR ALTER VIEW dbo.AcopioPorLote AS
SELECT Lote,
       COUNT(*)                                     AS Entregas,
       SUM(Kg)                                      AS KgTotal,
       SUM(CASE WHEN AptoUE = 1 THEN Kg ELSE 0 END) AS KgAptoUE,
       COUNT(DISTINCT FincaId)                      AS FincasConEntregas,
       MAX(FechaEvento)                             AS UltimaEntrega
FROM dbo.EventosAcopio
GROUP BY Lote""",
]


def configurado() -> bool:
    return bool(os.environ.get("AZURE_SQL_SERVER") and os.environ.get("AZURE_SQL_DATABASE"))


def _token() -> str:
    """Un token de Entra ID para Azure SQL: identidad administrada en App Service, `az login` en este computador."""
    punto, cabecera = os.environ.get("IDENTITY_ENDPOINT"), os.environ.get("IDENTITY_HEADER")
    if punto and cabecera:
        url = punto + "?" + urllib.parse.urlencode({"resource": RECURSO, "api-version": "2019-08-01"})
        with urllib.request.urlopen(urllib.request.Request(url, headers={"X-IDENTITY-HEADER": cabecera}), timeout=10) as r:
            return json.load(r)["access_token"]
    az = "az.cmd" if os.name == "nt" else "az"
    salida = subprocess.run([az, "account", "get-access-token", "--resource", RECURSO, "--query", "accessToken",
                             "-o", "tsv"], capture_output=True, text=True, timeout=60)
    if salida.returncode != 0 or not salida.stdout.strip():
        raise RuntimeError("No hay sesión de Azure: corran `az login` (o configuren la identidad administrada)")
    return salida.stdout.strip()


def _controlador() -> str:
    import pyodbc
    for nombre in ("ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"):
        if nombre in pyodbc.drivers():
            return nombre
    raise RuntimeError("Falta el controlador ODBC 18 de SQL Server (instalado en App Service; en Windows: "
                       "winget install Microsoft.msodbcsql.18)")


def conectar():
    import pyodbc
    token = _token().encode("utf-16-le")
    cadena = (f"Driver={{{_controlador()}}};Server=tcp:{os.environ['AZURE_SQL_SERVER']},1433;"
              f"Database={os.environ['AZURE_SQL_DATABASE']};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30")
    return pyodbc.connect(cadena, attrs_before={_ACCESS_TOKEN: struct.pack(f"<I{len(token)}s", len(token), token)})


def crear(conexion=None) -> None:
    con = conexion or conectar()
    try:
        cur = con.cursor()
        for sentencia in CREAR:
            cur.execute(sentencia)
        con.commit()
    finally:
        if conexion is None:
            con.close()


def fila(e: dict) -> tuple:
    i, q = e["ilmd"], e["quantityList"][0]
    return (e["eventID"], e["eventTime"], i["lote"], q["epcClass"].removeprefix("finca:"), i.get("finca"),
            q["quantity"], i.get("cantidad_reportada"), i.get("humedad_pct"), bool(i.get("apto_ue")), i.get("canal"),
            str(i.get("remitente") or "").removeprefix("huella:"), json.dumps(e, ensure_ascii=False))


def guardar_eventos(eventos: list[dict], conexion=None) -> int:
    """Inserta los eventos que aún no estén en la tabla (por EventId). Devuelve cuántos insertó."""
    con = conexion or conectar()
    nuevos = 0
    try:
        cur = con.cursor()
        for e in eventos:
            cur.execute(f"""IF NOT EXISTS (SELECT 1 FROM {TABLA} WHERE EventId = ?)
INSERT INTO {TABLA} (EventId, FechaEvento, Lote, FincaId, Finca, Kg, CantidadReportada, HumedadPct, AptoUE, Canal,
                     Remitente, EventoJson) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", e["eventID"], *fila(e))
            nuevos += max(cur.rowcount, 0)
        con.commit()
    finally:
        if conexion is None:
            con.close()
    return nuevos


def preparar_al_arrancar() -> str:
    """Al arrancar el servidor: crea la tabla si falta. Devuelve una línea para el registro (nunca tumba el servidor)."""
    if not configurado():
        return ""
    try:
        crear()
        return f"Azure SQL: tabla {TABLA} lista en {os.environ['AZURE_SQL_DATABASE']}"
    except Exception as e:  # noqa: BLE001
        return f"AVISO: Azure SQL no disponible ({type(e).__name__}: {str(e)[:200]}). El acopio sigue en el archivo local."


def main(argv: list[str]) -> int:
    from . import acopio, cargar_env
    cargar_env()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("orden", choices=["crear", "subir", "ver"])
    a = p.parse_args(argv)
    if not configurado():
        print("Falta AZURE_SQL_SERVER y AZURE_SQL_DATABASE en el .env", file=sys.stderr)
        return 1
    con = conectar()
    try:
        crear(con)
        if a.orden == "subir":
            todos = acopio.eventos()
            print(f"{guardar_eventos(todos, con)} entregas nuevas subidas a {TABLA} ({len(todos)} en el archivo local)")
        elif a.orden == "ver":
            cur = con.cursor()
            print("Resumen por lote:")
            for r in cur.execute("SELECT Lote, Entregas, KgTotal, KgAptoUE, UltimaEntrega FROM dbo.AcopioPorLote ORDER BY Lote"):
                print(f"  {r.Lote}: {r.Entregas} entregas · {r.KgTotal} kg · {r.KgAptoUE} kg aptos UE · última {r.UltimaEntrega}")
            print("Últimas entregas:")
            for r in cur.execute(f"SELECT TOP 10 FechaEvento, Finca, Lote, Kg, HumedadPct, AptoUE, Canal FROM {TABLA} "
                                 "ORDER BY FechaEvento DESC"):
                print(f"  {r.FechaEvento} · {r.Finca} · {r.Lote} · {r.Kg} kg · humedad {r.HumedadPct} · UE {bool(r.AptoUE)} · {r.Canal}")
        else:
            print(f"Tabla {TABLA} y vista dbo.AcopioPorLote listas")
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
