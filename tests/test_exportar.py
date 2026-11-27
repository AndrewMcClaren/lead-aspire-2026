"""Exportar: cotizador, cifras imposibles, conocimiento del comprador y cartas de crédito."""

import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from kit import documentos as d
from kit import exportar as e
from kit.bitacora import Bitacora

CAFE = Path(__file__).resolve().parent.parent / "casos" / "cafe"
MAESTROS = json.loads((CAFE / "maestros.json").read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def caso_cafe(monkeypatch):
    for v in ("CONTENT_SAFETY_ENDPOINT", "CONTENT_SAFETY_KEY", "KIT_JUEZ", "NOTIFICAR_URL", "KIT_API_KEY", "KIT_DECISIONES"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("KIT_DATOS", "casos/cafe")
    monkeypatch.setenv("KIT_LIMITE_MINUTO", "0")


def test_modalidad_segun_el_volumen():
    assert e.cotizar("china", 10)["modalidad"].startswith("aéreo")
    assert "LCL" in e.cotizar("china", 100)["modalidad"]
    assert e.cotizar("union_europea", 300)["modalidad"].startswith("2 contenedores")


def test_el_desglose_suma_el_total_y_tiene_fuentes():
    r = e.cotizar("union_europea", 275)
    assert abs(sum(c["usd"] for c in r["costos"]) - r["total_usd"]) < 1
    assert all(c["fuente"] for c in r["costos"]) and r["dias"][0] < r["dias"][1]
    assert any("deforestación" in x for x in r["requisitos"])


def test_china_paga_arancel_y_europa_no():
    china, ue = e.cotizar("china", 275), e.cotizar("union_europea", 275)
    assert next(c for c in china["costos"] if c["concepto"].startswith("Arancel"))["usd"] > 0
    assert next(c for c in ue["costos"] if c["concepto"].startswith("Arancel"))["usd"] == 0


def test_cifra_imposible_de_produccion():
    r = e.cotizar("china", 10, produccion_sacos_mes=10_000_000)
    alta = [a for a in r["alertas"] if a["nivel"] == "alta"]
    assert alta and "veces todo el café que produce Colombia" in alta[0]["texto"]
    assert not [a for a in e.cotizar("china", 10, produccion_sacos_mes=50)["alertas"] if a["nivel"] == "alta"]


def test_datos_invalidos():
    with pytest.raises(ValueError):
        e.cotizar("marte", 10)
    with pytest.raises(ValueError):
        e.cotizar("china", -5)


def test_conocimiento_del_comprador():
    assert e.conocer_comprador("Tostadores Nuevos Shanghai Co. Ltd.", maestros=MAESTROS)["estado"] == "desconocido"
    assert e.conocer_comprador("Importadora Ejemplo GmbH", maestros=MAESTROS)["estado"] == "registrado"
    assert e.conocer_comprador("Importadora Ejemplo GmbH", "Banco Nuevo 999", maestros=MAESTROS)["estado"] == "alerta"
    assert e.conocer_comprador("Tostadora Demo KK", maestros=MAESTROS)["estado"] == "nuevo"  # registrada hace menos de 30 días


def test_carta_de_credito_peligrosa():
    info = d.extraer("lc.txt", (CAFE / "ejemplos" / "carta_de_credito_LC-88231.txt").read_bytes())
    tipos = {s["tipo"]: s["nivel"] for s in d.senales(info, MAESTROS)}
    assert tipos["lc_revocable"] == tipos["lc_fechas"] == "alta"
    assert {"lc_sin_confirmar", "lc_sin_ucp", "lc_plazo", "lc_ordenante"} <= set(tipos)


def test_carta_de_credito_sana_no_alarma():
    texto = ("Carta de crédito irrevocable y confirmada por Banco Ficticio de Colombia, sujeta a UCP 600.\n"
             "Ordenante: Importadora Ejemplo GmbH\nÚltimo día de embarque: 1 de diciembre de 2026\n"
             "Fecha de vencimiento: 31 de diciembre de 2026\nPago a la vista")
    altas = [s for s in d.senales({"texto": texto, "oculto": [], "cabeceras": {}}, MAESTROS) if s["nivel"] in ("alta", "media")]
    assert altas == []


def test_api_cotizar_mercados_y_comprador(tmp_path):
    from kit.servidor import crear_app
    srv = ThreadingHTTPServer(("127.0.0.1", 0), crear_app("simulado", Bitacora(tmp_path / "b.jsonl")))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"

    def post(ruta, datos):
        req = urllib.request.Request(base + ruta, data=json.dumps(datos).encode(), headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())
    try:
        m = json.loads(urllib.request.urlopen(base + "/api/mercados").read())
        assert m["destinos"][0]["nombre"] == "Estados Unidos" and len(m["pasos"]) >= 8
        c, r = post("/api/cotizar", {"destino": "china", "sacos": "10", "produccion_sacos_mes": "10000000"})
        assert c == 200 and r["alertas"][0]["nivel"] == "alta"
        assert post("/api/cotizar", {"destino": "china", "sacos": "diez"})[0] == 400
        c, k = post("/api/comprador", {"nombre": "Tostadores Nuevos Shanghai Co. Ltd."})
        assert c == 200 and k["estado"] == "desconocido"
        bit = json.loads(urllib.request.urlopen(base + "/api/bitacora").read())
        assert {"cotizacion", "conocimiento_cliente"} <= {x["tipo"] for x in bit["ultimas"]}
    finally:
        srv.shutdown()
