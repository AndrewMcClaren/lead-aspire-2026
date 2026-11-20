"""Genera plantillas/una_pagina.docx y el ejemplo lleno (necesita: pip install python-docx).

Uso desde la raíz del repo:  python plantillas/fuente/una_pagina.py plantillas
Para el PDF del ejemplo, abran una_pagina_ejemplo.docx en Word y exporten a PDF.
"""
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AZUL = RGBColor(0x0B, 0x4F, 0x9C)
GRIS = RGBColor(0x55, 0x5F, 0x6B)

PLANTILLA = {
    "titulo": "[Cliente] · [La solución en menos de 8 palabras]",
    "meta": "Equipo [nombre] · LEAD ASPIRE Bogotá 2026 · 27 de noviembre de 2026",
    "titular": ("[Problema con un número del cliente: «hoy X les cuesta Y al mes»]. [Qué construimos, en una frase]. "
                "[Resultado medido: «en N casos de prueba, pasó de A a B»]."),
    "problema": ("[El problema con las palabras del cliente, entre comillas]. [Cuánto cuesta hoy: horas, dinero, clientes o "
                 "riesgo]. [Por qué no lo han resuelto: el freno para adoptar IA]. Palanca: [ingresos / productividad / "
                 "gastos / seguridad]."),
    "flujo": ["Entrada\n[dato, documento o solicitud]", "Validación\n[la IA propone, el código revisa con datos del cliente]",
              "Acción aprobada\n[lo delicado lo confirma una persona]"],
    "solucion": ("[Qué ve el usuario y dónde: Teams, Copilot Studio, Power Apps]. [Qué hace por detrás]. [Con qué se conecta de "
                 "lo que el cliente ya tiene: no reemplaza nada]. Herramientas de Microsoft: [lista]."),
    "prueba": ("[Cuántos casos y de dónde salieron: del cliente o escritos por alguien que no vio la solución]. [Contra qué "
               "comparamos: cómo se hace hoy o la IA sin controles, con el mismo modelo]."),
    "resultados": [("Métrica", "Hoy / sin la solución", "Con la solución"), ("[métrica 1]", "[A]", "[B]"),
                   ("[métrica 2]", "[A]", "[B]"), ("[errores o casos bloqueados por error]", "[A]", "[B]")],
    "roi": ("Con una adopción conservadora de [X %], la solución [libera N horas al mes / evita X pesos en pérdidas]. Beneficio "
            "neto: [X millones al mes] (escenario base: [Y]). El piloto se recupera en [Z meses]. Supuestos: [los 2 o 3 que "
            "más pesan, con su fuente]."),
    "riesgos": ("[Qué no resuelve]. [Qué pasa si la IA se equivoca: control humano, fuente visible, «no tengo ese dato»]. "
                "[Datos personales y cómo se protegen]. [Qué falta para producción]."),
    "siguiente": "Piloto de [2 semanas] con [área concreta], midiendo [una métrica]. Necesitamos de ustedes: [acceso o dato].",
    "pie": ("Datos: [del cliente / de ejemplo]. Herramientas: [lista]. Construido en un día con asistencia de IA y revisado "
            "por el equipo."),
}

EJEMPLO = {
    "titulo": "Cooperativa del ejemplo · Pagos a proveedores sin fraude",
    "meta": "Equipo de ejemplo · Simulacro LEAD ASPIRE · CASO FICTICIO: todas las cifras son inventadas",
    "titular": ("Dos personas revisan a mano 900 facturas al mes y un correo falso de cambio de cuenta les costó 38 millones. "
                "Construimos un asistente en Teams que lee las facturas y solo deja pagar a cuentas registradas, con firma de "
                "tesorería. En 20 facturas de prueba, los fraudes que pasaron bajaron de 3 de 4 a 0 de 4."),
    "problema": ("«Pagamos unas 900 facturas al mes y dos personas las revisan a mano; les toma casi todo el mes». El año pasado "
                 "un correo falso pidió cambiar la cuenta de un proveedor y se perdieron 38 millones. No usan IA porque temen "
                 "que pague sola. Palanca: seguridad y productividad."),
    "flujo": ["Entrada\nfactura o correo del proveedor", "Validación\nla IA extrae los datos; el código revisa cuenta, monto y proveedor",
              "Acción aprobada\ntesorería firma en Teams"],
    "solucion": ("La persona de tesorería ve en Teams cada factura con un sello: «cuenta registrada» o «cuenta distinta: "
                 "bloqueada». Por detrás, el asistente compara con el maestro de proveedores que ya tiene la cooperativa y nunca "
                 "paga solo. No reemplaza el software contable: lee su exportación a Excel. Herramientas: Azure OpenAI, Prompt "
                 "Shields, Power Automate, Teams."),
    "prueba": ("20 facturas de prueba (16 legítimas y 4 con fraude de cambio de cuenta) escritas por un integrante que no vio "
               "la solución. Comparamos con la misma IA sin controles."),
    "resultados": [("Métrica", "Sin la solución", "Con la solución"), ("Fraudes que pasaron", "3 de 4", "0 de 4"),
                   ("Facturas legítimas bloqueadas por error", "0 de 16", "1 de 16"),
                   ("Minutos de revisión por factura (estimado)", "20", "6")],
    "roi": ("Con una adopción conservadora del 30 %, la solución libera 63 horas al mes y deja un beneficio neto de 1,9 millones "
            "de pesos al mes (escenario base, 60 %: 4,3 millones). El piloto se recupera en 3,1 meses. Supuestos que más pesan: "
            "hora de trabajo a 25.000 pesos y 80 % de los fraudes evitados (medido en 4 casos: muestra pequeña)."),
    "riesgos": ("No detecta un fraude si el atacante logra cambiar la cuenta en el maestro de proveedores. Toda factura la firma "
                "una persona distinta de quien la carga. Una factura legítima se bloqueó por error: va a revisión, no se pierde. "
                "Falta probarlo con facturas reales y con la TI de la cooperativa."),
    "siguiente": ("Piloto de 2 semanas con tesorería, midiendo minutos por factura y pagos a cuentas no registradas. Necesitamos "
                  "acceso de solo lectura al maestro de proveedores."),
    "pie": "Datos de ejemplo, inventados. Herramientas: Azure OpenAI, Prompt Shields, Power Automate, Teams. Construido con asistencia de IA.",
}


def _sombra(celda, color):
    tc = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), color)
    tc.append(shd)


def _parrafo(doc, texto, tam=9.5, color=None, negrita=False, despues=3, cursiva=False):
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.font.size = Pt(tam); r.bold = negrita; r.italic = cursiva
    if color:
        r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(despues); p.paragraph_format.space_before = Pt(0)
    return p


def _seccion(doc, numero, titulo):
    p = doc.add_paragraph()
    r1 = p.add_run(f"{numero}  "); r1.font.size = Pt(10); r1.font.color.rgb = GRIS
    r2 = p.add_run(titulo); r2.font.size = Pt(11); r2.bold = True; r2.font.color.rgb = AZUL
    p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(1)


def construir(datos: dict, ruta: Path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(27.94), Cm(21.59)  # carta
    sec.top_margin = sec.bottom_margin = Cm(1.4); sec.left_margin = sec.right_margin = Cm(1.6)
    estilo = doc.styles["Normal"]; estilo.font.name = "Calibri"; estilo.font.size = Pt(9.5)

    _parrafo(doc, datos["titulo"], tam=17, negrita=True, despues=1)
    _parrafo(doc, datos["meta"], tam=8.5, color=GRIS, despues=5)
    _parrafo(doc, datos["titular"], tam=10.5, despues=4)

    _seccion(doc, "01", "El problema del cliente")
    _parrafo(doc, datos["problema"])

    _seccion(doc, "02", "La solución")
    t = doc.add_table(rows=1, cols=5); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, celda in enumerate(t.rows[0].cells):
        if i % 2 == 0:
            titulo, detalle = datos["flujo"][i // 2].split("\n", 1)
            celda.text = ""
            p = celda.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(titulo + "\n"); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = AZUL
            r2 = p.add_run(detalle); r2.font.size = Pt(8.5)
            _sombra(celda, "EAF1FB"); celda.width = Cm(5.3)
        else:
            celda.text = "→"; celda.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER; celda.width = Cm(0.7)
    _parrafo(doc, "", tam=3, despues=0)
    _parrafo(doc, datos["solucion"])

    _seccion(doc, "03", "Cómo lo probamos")
    _parrafo(doc, datos["prueba"])

    _seccion(doc, "04", "Resultados")
    filas = datos["resultados"]
    t = doc.add_table(rows=len(filas), cols=3); t.style = "Table Grid"
    for i, fila in enumerate(filas):
        for j, valor in enumerate(fila):
            c = t.rows[i].cells[j]; c.text = ""
            r = c.paragraphs[0].add_run(valor); r.font.size = Pt(9); r.bold = i == 0
            if i == 0:
                _sombra(c, "EEF2F6")
    _parrafo(doc, "", tam=3, despues=0)

    _seccion(doc, "05", "Impacto y retorno")
    _parrafo(doc, datos["roi"])

    _seccion(doc, "06", "Riesgos, límites y control humano")
    _parrafo(doc, datos["riesgos"])

    _seccion(doc, "07", "Siguiente paso")
    _parrafo(doc, datos["siguiente"])

    _parrafo(doc, datos["pie"], tam=7.5, color=GRIS, despues=0, cursiva=True)
    doc.save(ruta)


if __name__ == "__main__":
    salida = Path(sys.argv[1])
    construir(PLANTILLA, salida / "una_pagina.docx")
    construir(EJEMPLO, salida / "una_pagina_ejemplo.docx")
