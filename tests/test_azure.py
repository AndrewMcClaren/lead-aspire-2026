"""Pruebas de lo que necesita el kit en Azure, sin internet: decisiones de Teams por HTTP, Azure SQL y rutas persistentes."""

import json
import sys
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kit import acopio, decisiones, sqlazure, whatsapp  # noqa: E402
from kit.aprobacion import Bandeja  # noqa: E402
from kit.bitacora import Bitacora  # noqa: E402

PAGO = dict(tipo="pago", detalle="Pago", monto=200000, destino="Proveedor Demo S.A.S.",
            peticion="Paga la factura de Proveedor Demo", solicitante="asistente")


@pytest.fixture(autouse=True)
def limpio(monkeypatch, tmp_path):
    monkeypatch.setenv("KIT_DATOS", "casos/cafe")
    monkeypatch.setattr(acopio, "EVENTOS", tmp_path / "eventos.jsonl")
    for v in ("NOTIFICAR_URL", "KIT_DECISIONES", "KIT_API_KEY", "AZURE_SQL_SERVER", "AZURE_SQL_DATABASE",
              "SNOWFLAKE_TABLA_EVENTOS", "TWILIO_AUTH_TOKEN", "KIT_URL_PUBLICA", "KIT_EVENTOS"):
        monkeypatch.delenv(v, raising=False)


# ---------------------------------------------------------------- decisiones de Teams por HTTP
def test_decision_por_http_mismas_reglas_que_la_carpeta(tmp_path):
    b = Bandeja(Bitacora(tmp_path / "b.jsonl"))
    a1, a2, a3 = b.proponer(**PAGO), b.proponer(**PAGO), b.proponer(**PAGO)
    ok = decisiones.aplicar({"id": a1.id, "token": a1.token, "resultado": "Approve", "aprobador": "Ana Tesorería",
                             "comentario": "Revisado"}, b, b.bitacora)
    assert ok["resultado"] == "aplicado" and (a1.estado, a1.canal, a1.comentario) == ("aprobada", "Teams", "Revisado")
    assert decisiones.aplicar({"id": a2.id, "token": "adivinado", "resultado": "Approve", "aprobador": "Ana"}, b,
                              b.bitacora)["resultado"] == "rechazado"
    assert decisiones.aplicar({"id": a3.id, "token": a3.token, "resultado": "Approve", "aprobador": "asistente"}, b,
                              b.bitacora)["resultado"] == "rechazado"  # quien la pidió no la aprueba
    assert decisiones.aplicar({"id": a1.id, "token": a1.token, "resultado": "Reject"}, b)["resultado"] == "rechazado"
    assert decisiones.aplicar("no es un objeto", b)["resultado"] == "rechazado"
    assert a2.estado == a3.estado == "pendiente" and a1.estado == "aprobada"
    assert "decision_teams_rechazada" in (tmp_path / "b.jsonl").read_text(encoding="utf-8")


def test_post_api_decisiones_en_el_servidor(monkeypatch, tmp_path):
    from kit.servidor import crear_app
    monkeypatch.setenv("KIT_API_KEY", "clave")
    app = crear_app("simulado", Bitacora(tmp_path / "b.jsonl"))
    srv = ThreadingHTTPServer(("127.0.0.1", 0), app)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"

    def post(ruta, datos, clave="clave"):
        h = {"Content-Type": "application/json", **({"X-API-Key": clave} if clave else {})}
        try:
            with urllib.request.urlopen(urllib.request.Request(base + ruta, json.dumps(datos).encode(), h)) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}")

    try:
        codigo, accion = post("/api/acciones", PAGO)
        assert codigo == 201 and accion["estado"] == "pendiente" and "token" not in accion
        assert post("/api/decisiones", {"id": accion["id"], "token": "x", "resultado": "Approve"}, clave=None)[0] == 401
        codigo, r = post("/api/decisiones", {"id": accion["id"], "token": "falso", "resultado": "Approve", "aprobador": "Ana"})
        assert codigo == 400 and r["resultado"] == "rechazado"
    finally:
        srv.shutdown()


# ---------------------------------------------------------------- Azure SQL (con una conexión simulada)
class CursorFalso:
    def __init__(self, base):
        self.base, self.rowcount = base, 0

    def execute(self, sql, *params):
        if sql.lstrip().startswith("IF NOT EXISTS"):
            event_id = params[0]
            self.rowcount = 0 if event_id in self.base.filas else 1
            if self.rowcount:
                self.base.filas[event_id] = params[1:]
        else:
            self.base.ddl.append(sql)
        return self


class ConexionFalsa:
    def __init__(self):
        self.filas, self.ddl, self.commits = {}, [], 0

    def cursor(self):
        return CursorFalso(self)

    def commit(self):
        self.commits += 1

    def close(self):
        pass


def test_azure_sql_guarda_cada_entrega_una_sola_vez():
    r = whatsapp.procesar({"From": "whatsapp:+573001234567", "Body": "Finca Buenavista, 2 cargas"})
    con = ConexionFalsa()
    sqlazure.crear(con)
    assert any("CREATE TABLE dbo.EventosAcopio" in s for s in con.ddl) and any("AcopioPorLote" in s for s in con.ddl)
    assert sqlazure.guardar_eventos([r["evento"]], con) == 1
    assert sqlazure.guardar_eventos([r["evento"]], con) == 0  # la misma entrega no se duplica
    fila = con.filas[r["evento"]["eventID"]]
    assert fila[2] == "L-2026-0412" and fila[3] == "F-CAU-003" and fila[4] == "Buenavista" and fila[5] == 250
    assert fila[8] is False and fila[9] == "whatsapp:texto" and "3001234567" not in json.dumps(fila)  # sin teléfono


def test_whatsapp_guarda_en_sql_y_sql_caido_no_detiene_el_acopio(tmp_path):
    b = Bitacora(tmp_path / "b.jsonl")
    guardados = []
    r = whatsapp.procesar({"From": "whatsapp:+573001234567", "Body": "Finca La Loma, 3 arrobas"}, None, b,
                          guardar_sql=guardados.extend)
    assert guardados == [r["evento"]]

    def caido(eventos):
        raise ConnectionError("sin red")
    r = whatsapp.procesar({"From": "whatsapp:+573001234567", "Body": "Finca El Mirador, 4 arrobas"}, None, b,
                          guardar_sql=caido)
    assert r["entrega"]["ok"] and len(acopio.eventos()) == 2
    assert "sql_error" in (tmp_path / "b.jsonl").read_text(encoding="utf-8")


def test_sql_sin_configurar_no_hace_nada():
    assert not sqlazure.configurado() and sqlazure.preparar_al_arrancar() == ""


# ---------------------------------------------------------------- rutas persistentes en Azure
def test_kit_eventos_cambia_donde_se_guardan_las_entregas(monkeypatch, tmp_path):
    monkeypatch.setattr(acopio, "EVENTOS", acopio._EVENTOS_DEFECTO)
    monkeypatch.setenv("KIT_EVENTOS", str(tmp_path / "home" / "datos" / "eventos.jsonl"))
    whatsapp.procesar({"From": "whatsapp:+573001234567", "Body": "Finca La Loma, 3 arrobas"})
    assert (tmp_path / "home" / "datos" / "eventos.jsonl").exists() and len(acopio.eventos()) == 1
