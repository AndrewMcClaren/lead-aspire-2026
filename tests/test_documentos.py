"""Documentos adjuntos: lectura de archivos, señales sin IA, análisis comprobado, citas y la API."""

import base64
import io
import json
import threading
import urllib.error
import urllib.request
import zipfile
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from kit import documentos as d
from kit.aprobacion import Accion, resumen_para_aprobar, revisar_accion
from kit.asistente import responder
from kit.bitacora import Bitacora
from kit.cifras import Tabla

RAIZ = Path(__file__).resolve().parent.parent
CAFE = RAIZ / "casos" / "cafe"
EJEMPLOS = CAFE / "ejemplos"
MAESTROS = json.loads((CAFE / "maestros.json").read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def caso_cafe(monkeypatch):
    for v in ("CONTENT_SAFETY_ENDPOINT", "CONTENT_SAFETY_KEY", "KIT_JUEZ", "NOTIFICAR_URL", "BITACORA_CLAVE", "KIT_API_KEY",
              "KIT_BITACORA_PRIVADA", "KIT_DECISIONES"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("KIT_DATOS", "casos/cafe")
    monkeypatch.setenv("KIT_LIMITE_MINUTO", "0")


def leer(nombre):
    return d.extraer(nombre, (EJEMPLOS / nombre).read_bytes())


# ---------------------------------------------------------------- extracción
def test_lee_pdf_word_y_correo_con_lo_escondido():
    pdf = leer("instruccion_embarque_L-2026-0398.pdf")
    assert pdf["tipo"] == "PDF" and pdf["paginas"] == 1 and "L-2026-0398" in pdf["texto"] and not pdf["oculto"]
    word = leer("instruccion_embarque_L-2026-0412.docx")
    assert word["tipo"] == "Word" and "Nota para el asistente de IA" in word["oculto"][0]
    assert "Nota para el asistente" in word["texto"]  # lo escondido no se descarta: pasa por el escudo
    correo = leer("correo_cooperativa_cambio_de_cuenta.eml")
    assert correo["cabeceras"]["Reply-To"].endswith("ejemp1o.example") and "Instrucción para el asistente" in correo["oculto"][0]


def test_rechaza_lo_que_no_puede_leer():
    with pytest.raises(d.DocumentoInvalido, match="OCR"):
        d.extraer("foto.jpg", b"\xff\xd8\xff")
    with pytest.raises(d.DocumentoInvalido, match="no soportado"):
        d.extraer("macro.exe", b"MZ")
    with pytest.raises(d.DocumentoInvalido, match="máximo"):
        d.extraer("grande.txt", b"a" * (d.MAX_BYTES + 1))
    with pytest.raises(d.DocumentoInvalido):
        d.extraer("roto.pdf", b"%PDF-1.4 esto no es un pdf")
    bomba = io.BytesIO()
    with zipfile.ZipFile(bomba, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", "<a>" + "x" * (d.MAX_DESCOMPRIMIDO + 10) + "</a>")
    with pytest.raises(d.DocumentoInvalido, match="demasiado grande"):
        d.extraer("bomba.docx", bomba.getvalue())


def test_nombre_de_archivo_saneado():
    info = d.extraer("../../etc/<script>.txt", b"hola mundo")
    assert "/" not in info["nombre"] and "<" not in info["nombre"]


# ---------------------------------------------------------------- señales sin IA
def test_senales_del_correo_fraudulento():
    tipos = {s["tipo"]: s["nivel"] for s in d.senales(leer("correo_cooperativa_cambio_de_cuenta.eml"), MAESTROS)}
    assert tipos["texto_oculto"] == tipos["responder_a"] == tipos["cuenta_no_registrada"] == "alta"
    assert tipos["urgencia"] == "media"


def test_senal_del_reglamento_europeo_solo_si_falta_la_geolocalizacion():
    sin_geo = {s["tipo"] for s in d.senales(leer("instruccion_embarque_L-2026-0412.docx"), MAESTROS)}
    con_geo = {s["tipo"] for s in d.senales(leer("instruccion_embarque_L-2026-0398.pdf"), MAESTROS)}
    assert "eudr" in sin_geo and "eudr" not in con_geo


def test_una_fecha_no_es_una_cuenta():
    info = {"texto": "Abrimos la cuenta corriente el 2026-11-25 sin novedad.", "oculto": [], "cabeceras": {}}
    assert not [s for s in d.senales(info, MAESTROS) if s["tipo"] == "cuenta_no_registrada"]


# ---------------------------------------------------------------- análisis comprobado
class Mentiroso:
    """Un modelo que inventa una cuenta y un monto que no están en el documento."""
    nombre = "azure-prueba"

    def generar_json(self, sistema, usuario, imagen=None):
        return {"tipo_documento": "correo", "resumen": "Pide un pago",
                "solicitud": {"tipo": "pago", "destino": "Cooperativa Cafetera Ejemplo", "cuenta": "Banco Falso 9999-0000",
                              "monto": "99.999", "moneda": "USD", "lote": "", "cita": "Paguen ya a la cuenta nueva"}}


def test_analisis_descarta_lo_que_no_esta_en_el_documento_y_completa_con_reglas():
    texto = leer("correo_cooperativa_cambio_de_cuenta.eml")["texto"]
    a = d.analizar(texto, MAESTROS, Mentiroso())
    s = a["solicitud"]
    assert len(a["descartes"]) == 3  # cuenta, monto y cita inventados
    assert s["cuenta"] == "4410-778899-03" and s["monto"] == 48500  # las reglas leen el original
    assert s["destino"] == "Cooperativa Cafetera Ejemplo" and a["origen"] == "modelo"


def test_analisis_sin_modelo_usa_reglas():
    a = d.analizar(leer("instruccion_embarque_L-2026-0412.docx")["texto"], MAESTROS)
    assert a["origen"] == "reglas" and a["solicitud"]["tipo"] == "despachar_lote" and a["solicitud"]["lote"] == "L-2026-0412"


# ---------------------------------------------------------------- guardián
def test_guardian_bloquea_lote_sin_geolocalizacion_a_europa():
    estado, motivos = revisar_accion("despachar_lote", None, "Importadora Ejemplo GmbH", "", "Despacha el lote",
                                     maestros=MAESTROS, lote="L-2026-0412")
    assert estado == "bloqueada" and any("Reglamento europeo" in m for m in motivos)
    estado, _ = revisar_accion("despachar_lote", None, "Importadora Ejemplo GmbH", "", "Despacha el lote",
                               maestros=MAESTROS, lote="L-2026-0398")
    assert estado == "pendiente"
    estado, _ = revisar_accion("despachar_lote", None, "Tostadora Demo KK", "", "Despacha el lote",  # Japón: no aplica
                               maestros=MAESTROS, lote="L-2026-0412")
    assert estado == "pendiente"


def test_quien_aprueba_ve_los_datos_crudos():
    a = Accion(1, "pago", "Correo: x.eml", 48500, "Cooperativa Cafetera Ejemplo", "Banco Nuevo CO 4410-778899-03",
               "Pagar según el documento x.eml", estado="bloqueada", motivos=["La cuenta no es la registrada"])
    r = resumen_para_aprobar(a, MAESTROS)
    assert "NO COINCIDE" in r and "Banco Ficticio CO 7777-8888" in r and "48.500" in r


# ---------------------------------------------------------------- citas comprobadas
class Citador:
    def __init__(self, salida):
        self.salida, self.nombre = salida, "prueba"

    def generar_json(self, sistema, usuario, imagen=None):
        return self.salida


DOC = "Instrucción de embarque. Cantidad: 275 sacos de 60 kg. Puerto de destino: Hamburgo, Alemania."


def test_respuesta_citada_y_comprobada():
    m = Citador({"texto": "Según la instrucción, son 275 sacos de 60 kg con destino a Hamburgo.", "claves": [],
                 "citas": [{"doc": 1, "frase": "Cantidad: 275 sacos de 60 kg."}, {"doc": 1, "frase": "Puerto de destino: Hamburgo"}]})
    r = responder("¿Cuántos sacos y a dónde?", m, Tabla(), [DOC], nombres=["instruccion.pdf"], proteger_datos=False)
    assert r["estado"] == "documento" and len(r["citas"]) == 2 and r["citas"][0]["nombre"] == "instruccion.pdf"


def test_cita_inventada_bloquea_la_respuesta():
    m = Citador({"texto": "Son 900 sacos.", "claves": [], "citas": [{"doc": 1, "frase": "Cantidad: 900 sacos"}]})
    r = responder("¿Cuántos sacos?", m, Tabla(), [DOC], proteger_datos=False)
    assert r["estado"] == "bloqueada" and any("no está en ningún documento" in p for p in r["problemas"])


def test_numero_que_no_esta_en_la_cita_bloquea():
    m = Citador({"texto": "Son 275 sacos y 9.000 dólares.", "claves": [], "citas": [{"doc": 1, "frase": "Cantidad: 275 sacos de 60 kg"}]})
    r = responder("¿Cuántos sacos?", m, Tabla(), [DOC], proteger_datos=False)
    assert r["estado"] == "bloqueada" and any("9.000" in p for p in r["problemas"])


def test_el_mismo_numero_con_otro_formato_se_acepta():
    assert d.firma_numero("48.500") & d.numeros_de("USD 48,500.00") and not d.firma_numero("48.501") & d.numeros_de("48,500.00")


# ---------------------------------------------------------------- API
@pytest.fixture
def api(tmp_path):
    from kit.servidor import crear_app
    srv = ThreadingHTTPServer(("127.0.0.1", 0), crear_app("simulado", Bitacora(tmp_path / "b.jsonl")))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"

    def llamar(ruta, datos=None, crudo=None):
        cuerpo = crudo if crudo is not None else (json.dumps(datos).encode() if datos is not None else None)
        req = urllib.request.Request(base + ruta, data=cuerpo, headers={"Content-Type": "application/json"} if cuerpo else {})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}")
        except (urllib.error.URLError, ConnectionError, OSError):  # el servidor cortó la conexión ante un cuerpo enorme
            return 0, {}  # (en Linux llega como URLError; en Windows, como ConnectionAbortedError)
    yield llamar
    srv.shutdown()


def test_api_subir_analizar_y_proponer(api):
    contenido = base64.b64encode((EJEMPLOS / "correo_cooperativa_cambio_de_cuenta.eml").read_bytes()).decode()
    c, doc = api("/api/documentos", {"nombre": "correo.eml", "contenido": contenido})
    assert c == 201 and doc["accion"] == "saneado" and "texto" not in doc
    c, doc = api(f"/api/documentos/{doc['id']}/analizar", {})
    assert doc["analisis"]["guardian"]["estado"] == "bloqueada"
    c, accion = api(f"/api/documentos/{doc['id']}/proponer", {})
    assert c == 201 and accion["estado"] == "bloqueada" and "NO COINCIDE" in accion["resumen"]
    c, r = api("/api/preguntar", {"pregunta": "¿Qué cuenta pide el correo para el pago?", "documentos_ids": [doc["id"]]})
    assert c == 200 and r["estado"] in ("documento", "sin_dato", "verificada", "general")
    c, estado = api("/api/estado")
    assert estado["sesion"]["estado"] == "sospechosa" and estado["sesion"]["incidentes"] == 1  # no se cuenta dos veces
    _, bit = api("/api/bitacora")
    assert bit["integra"] and {"documento_recibido", "documento_analizado"} <= {e["tipo"] for e in bit["ultimas"]}


def test_api_ejemplos_y_limites(api):
    c, lista = api("/api/ejemplos")
    assert "instruccion_embarque_L-2026-0398.pdf" in lista
    assert api("/api/ejemplos/..%2Fcifras.csv", {})[0] == 404  # nada de rutas arbitrarias
    c, doc = api("/api/ejemplos/instruccion_embarque_L-2026-0398.pdf", {})
    assert c == 201 and doc["accion"] == "pasa"
    assert api("/api/documentos", {"nombre": "x.png", "contenido": "aGVsbG8="})[0] == 400
    assert api("/api/documentos", {"nombre": "x.pdf", "contenido": "%%no-base64%%"})[0] == 400
    grande = json.dumps({"nombre": "x.txt", "contenido": "a" * (9 * 1024 * 1024)}).encode()
    assert api("/api/documentos", crudo=grande)[0] in (413, 0)
    assert api(f"/api/documentos/{doc['id']}/quitar", {})[0] == 200
    assert api("/api/documentos")[1] == []


# ---------------------------------------------------------------- datos oficiales de mercado (sin internet)
TEXTO_FNC = """Noviembre 25 / 2026
PRECIO EXTERNO
Cierre contrato C Nueva York 270.00 USCent/Lb
PRECIO INTERNO DE REFERENCIA
Precio total por carga de 125 Kg de pergamino seco FR 94       2,180,000 COP"""


def test_lee_el_precio_diario_de_la_federacion():
    from kit.mercado import leer_texto_fnc
    assert leer_texto_fnc(TEXTO_FNC) == {"fecha": "2026-11-25", "contrato_c_usd_lb": 2.7, "precio_interno_cop_carga": 2180000}
    with pytest.raises(ValueError, match="cambió de formato"):
        leer_texto_fnc("Otro formato")


def test_cifras_de_mercado_se_actualizan_sin_tocar_las_demas(tmp_path, monkeypatch):
    import shutil
    from kit.mercado import actualizar_cifras, filas_de_mercado
    caso = tmp_path / "caso"
    shutil.copytree(CAFE, caso, ignore=shutil.ignore_patterns("ejemplos"))
    monkeypatch.setenv("KIT_DATOS", str(caso))
    antes = Tabla(caso / "cifras.csv")
    filas = filas_de_mercado({"fecha": "2026-11-26", "contrato_c_usd_lb": 2.75, "precio_interno_cop_carga": 2200000},
                             {"fecha": "2026-11-27", "trm": 3612.5}, "2026-11-27 07:00")
    actualizar_cifras(filas)
    t = Tabla(caso / "cifras.csv")
    assert t.cifras["precio_contrato_c_usd_lb"].texto() == "2,75 dólares por libra"
    assert t.cifras["trm_cop_usd"].texto() == "$ 3.612,50 por dólar" and "datos.gov.co" in t.cifras["trm_cop_usd"].fuente
    assert t.cifras["pct_lotes_con_geolocalizacion"] == antes.cifras["pct_lotes_con_geolocalizacion"]
    assert len(t.cifras) == len(antes.cifras)
