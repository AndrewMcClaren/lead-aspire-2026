"""Genera los datos ficticios del tablero de Power BI de la exportadora de café (casos/cafe).

Los totales coinciden con casos/cafe/cifras.csv: 1.250.000 sacos, 71 % de lotes con geolocalización, 42 % del
volumen a la Unión Europea y 31 % a Estados Unidos, 57 reclamos que suman 3,1 millones de dólares, 6 días
promedio de documentos por embarque y los presupuestos de compras, logística y cumplimiento europeo.
Así el tablero y el asistente dicen los mismos números. También suman 520 millones de dólares en ventas.

Precios: una serie mensual ficticia del contrato C (centavos de dólar por libra, convertida a dólares) más un
diferencial por lote que depende de la calidad y del comprador. Es un ejemplo para practicar el tablero, no un
precio real del mercado.

Uso: python plantillas/powerbi/generar_datos.py   (siempre da los mismos datos: semilla fija)
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SALIDA = Path(__file__).resolve().parent / "datos"
rnd = random.Random(2026)
INICIO = date(2025, 12, 1)  # un año: diciembre de 2025 a noviembre de 2026
REGIONES = [("Huila", .22), ("Antioquia", .18), ("Tolima", .14), ("Cauca", .13), ("Nariño", .11), ("Caldas", .10), ("Santander", .12)]
COOPERATIVAS = ["Cooperativa Cafetera Ejemplo", "Asociación Productores del Sur (ficticia)", "Cooperativa La Montaña (ficticia)",
                "Productores Independientes"]
MERCADOS = [("Unión Europea", 42), ("Estados Unidos", 31), ("Japón", 12), ("Otros", 15)]
COMPRADORES = {"Unión Europea": ["Importadora Ejemplo GmbH", "Tostadores Demo BV"], "Estados Unidos": ["Ejemplo Coffee Imports Inc.", "Demo Roasters LLC"],
               "Japón": ["Tostadora Demo KK"], "Otros": ["Comprador Demo Corea", "Comprador Demo Australia"]}
# Contrato C ficticio, en USD por libra, de diciembre de 2025 a noviembre de 2026
PRECIO_C = [2.95, 3.05, 2.88, 2.80, 2.92, 3.10, 3.02, 2.84, 2.76, 2.70, 2.82, 2.90]
# Prima o descuento que paga cada comprador sobre el diferencial (USD por libra)
PRIMA_COMPRADOR = {"Importadora Ejemplo GmbH": 0.06, "Tostadores Demo BV": 0.02, "Ejemplo Coffee Imports Inc.": -0.02,
                   "Demo Roasters LLC": 0.04, "Tostadora Demo KK": 0.10, "Comprador Demo Corea": 0.00, "Comprador Demo Australia": 0.03}
LIBRAS_POR_SACO = 60 * 2.20462
PUERTOS = [("Buenaventura", .55), ("Cartagena", .35), ("Santa Marta", .10)]


def elegir(pares):
    return rnd.choices([p for p, _ in pares], weights=[w for _, w in pares])[0]


def escribir(nombre, filas):
    with open(SALIDA / nombre, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


def main():
    SALIDA.mkdir(exist_ok=True)
    # Productores: exactamente 71 % geolocalizados (se reparte por región con algo de variación)
    productores = []
    for i in range(1, 601):
        region = elegir(REGIONES)
        productores.append({"productor_id": f"P{i:04d}", "region": region, "cooperativa": rnd.choice(COOPERATIVAS),
                            "hectareas": round(rnd.uniform(1, 12), 1),
                            "certificacion": rnd.choices(["Ninguna", "Rainforest Alliance", "Fairtrade", "Orgánico"], [55, 20, 15, 10])[0],
                            "geolocalizado": "No"})
    for p in rnd.sample(productores, 426):  # 426 de 600 = 71 %
        p["geolocalizado"] = "Sí"
    escribir("productores.csv", productores)

    # Lotes: 5.000 lotes, 1.250.000 sacos. El 71 % de los lotes tiene geolocalización.
    n = 5000
    geo = set(rnd.sample(range(n), int(n * .71)))
    sacos = [rnd.randint(150, 350) for _ in range(n)]
    sacos[-1] += 1_250_000 - sum(sacos)
    # Mercados por volumen: se asignan lotes hasta llegar a cada porcentaje del total de sacos
    orden = list(range(n))
    rnd.shuffle(orden)
    mercado_de, acum, objetivo = {}, 0, []
    total = sum(sacos)
    limites, s = [], 0
    for m, pct in MERCADOS:
        s += pct
        limites.append((m, total * s / 100))
    k = 0
    for i in orden:
        acum += sacos[i]
        while acum > limites[k][1] and k < len(limites) - 1:
            k += 1
        mercado_de[i] = limites[k][0]
    lotes = []
    ultimo_mes = date(2026, 11, 1)
    rechazados_ultimo_mes = 0
    for i in range(n):
        dia = INICIO + timedelta(days=rnd.randint(0, 364))
        puntaje = round(min(90, max(78, rnd.gauss(83.5, 1.8))), 1)
        prod = rnd.choice(productores)
        estado = "Exportado"
        if puntaje < 80 and rnd.random() < .5:
            estado = "Rechazado por calidad"
        comprador = rnd.choice(COMPRADORES[mercado_de[i]])
        mes_idx = (dia.year - INICIO.year) * 12 + dia.month - INICIO.month
        diferencial = round(0.22 + (puntaje - 83) * 0.07 + PRIMA_COMPRADOR[comprador] + rnd.gauss(0, 0.03), 3)
        lotes.append({"lote_id": f"L{i + 1:05d}", "fecha_compra": dia.isoformat(), "mes": dia.strftime("%Y-%m"),
                      "mes_fecha": dia.replace(day=1).isoformat(), "productor_id": prod["productor_id"],
                      "region": prod["region"], "sacos_60kg": sacos[i], "puntaje_sca": puntaje,
                      "factor_rendimiento": round(rnd.gauss(92.8, 1.2), 1), "especial_prima": "Sí" if puntaje >= 85 else "No",
                      "geolocalizado": "Sí" if i in geo else "No", "destino_mercado": mercado_de[i],
                      "comprador": comprador, "estado": estado, "precio_c_usd_lb": PRECIO_C[mes_idx], "diferencial_usd_lb": diferencial})
    # Exactamente 23 lotes rechazados en el último mes (cifra del caso)
    for l in lotes:
        if l["fecha_compra"] >= ultimo_mes.isoformat() and l["estado"] == "Rechazado por calidad":
            l["estado"] = "Exportado"
    candidatos = [l for l in lotes if l["fecha_compra"] >= ultimo_mes.isoformat()]
    for l in rnd.sample(candidatos, 23):
        l["estado"] = "Rechazado por calidad"
    # Ventas: precio = contrato C + diferencial; se escala para que el total sea exactamente 520 millones de dólares.
    # Costos: compra al productor (según bolsa y calidad) y logística por libra; de ahí sale el margen de cada lote.
    brutos = [(l["precio_c_usd_lb"] + l["diferencial_usd_lb"]) * l["sacos_60kg"] * LIBRAS_POR_SACO for l in lotes]
    escala = 520_000_000 / sum(brutos)
    for l, b in zip(lotes, brutos):
        precio = (l["precio_c_usd_lb"] + l["diferencial_usd_lb"]) * escala
        l["precio_venta_usd_lb"] = round(precio, 3)
        l["ventas_usd"] = round(b * escala)
        # Al productor se le paga por bolsa y calidad, no según a quién se le vende: la prima del comprador va al margen
        costo_lb = (l["precio_c_usd_lb"] + 0.22 + (l["puntaje_sca"] - 83) * 0.06) * escala * rnd.uniform(0.835, 0.865)
        compra = costo_lb * l["sacos_60kg"] * LIBRAS_POR_SACO
        logistica = l["sacos_60kg"] * LIBRAS_POR_SACO * rnd.uniform(0.07, 0.11)
        l["margen_usd"] = round(l["ventas_usd"] - compra - logistica)
    lotes[-1]["ventas_usd"] += 520_000_000 - sum(l["ventas_usd"] for l in lotes)
    escribir("lotes.csv", lotes)

    # Embarques: días de documentos con promedio exacto de 6
    embarques = []
    for i in range(1, 1001):
        mercado = elegir([(m, p) for m, p in MERCADOS])
        dia = INICIO + timedelta(days=rnd.randint(0, 364))
        embarques.append({"embarque_id": f"E{i:04d}", "fecha": dia.isoformat(), "mes": dia.strftime("%Y-%m"), "puerto": elegir(PUERTOS),
                          "destino_mercado": mercado, "comprador": rnd.choice(COMPRADORES[mercado]), "contenedores": rnd.randint(2, 8),
                          "dias_documentos": rnd.randint(2, 10), "retraso_dias": max(0, int(rnd.gauss(-0.5, 2.5))),
                          "fecha_prometida": (dia + timedelta(days=rnd.randint(20, 45))).isoformat()})
    dif = 6 * len(embarques) - sum(e["dias_documentos"] for e in embarques)
    paso = 1 if dif > 0 else -1
    while dif:
        e = rnd.choice(embarques)
        if 1 <= e["dias_documentos"] + paso <= 14:
            e["dias_documentos"] += paso
            dif -= paso
    escribir("embarques.csv", embarques)

    # Reclamos: 57 que suman exactamente 3,1 millones de dólares
    motivos = [("Humedad fuera de rango", 25), ("Defectos físicos", 25), ("Taza distinta a la muestra", 30), ("Diferencia de peso", 10),
               ("Documentos incompletos", 10)]
    reclamos = []
    costos = [rnd.uniform(.4, 1.6) for _ in range(57)]
    escala = 3_100_000 / sum(costos)
    costos = [round(c * escala) for c in costos]
    costos[-1] += 3_100_000 - sum(costos)
    for i in range(57):
        e = rnd.choice(embarques)
        reclamos.append({"reclamo_id": f"R{i + 1:03d}", "fecha": e["fecha"], "mes": e["mes"], "embarque_id": e["embarque_id"],
                         "comprador": e["comprador"], "destino_mercado": e["destino_mercado"], "motivo": elegir(motivos), "costo_usd": costos[i]})
    escribir("reclamos.csv", reclamos)

    # Mercado diario: contrato C en USD por libra y TRM en pesos por dólar, días hábiles del año.
    # - TRM: la OFICIAL, de datos.gov.co (trm_oficial.csv, que trae python -m kit.mercado trm --csv ...). Sin ese archivo
    #   se simula una que baja como bajó en 2026.
    # - Contrato C: el camino día a día es simulado, pero termina en el cierre real del 25-nov-2026 (2,70 USD/lb), y el
    #   precio interno se calibra con el de la Federación ese día (COP 2.180.000 por carga de 125 kg).
    # Así el tablero y el asistente dicen lo mismo el día de la demo.
    oficial = {}
    ruta_trm = SALIDA / "trm_oficial.csv"
    if ruta_trm.exists():
        with open(ruta_trm, encoding="utf-8") as fh:
            oficial = {f["fecha"]: float(f["trm"]) for f in csv.DictReader(fh)}
    fechas_trm = sorted(oficial)
    mercado, c, trm, dia = [], 2.95, 3900.0, INICIO
    while dia <= date(2026, 11, 25):  # hasta el día antes del evento
        if dia.weekday() < 5:
            objetivo = PRECIO_C[(dia.year - INICIO.year) * 12 + dia.month - INICIO.month]
            c = max(2.2, c + (objetivo - c) * 0.08 + rnd.gauss(0, 0.045))
            avance = min(1.0, (dia - INICIO).days / (date(2026, 9, 15) - INICIO).days)
            trm_objetivo = 3900 + (3180 - 3900) * avance
            trm = max(2900, trm + (trm_objetivo - trm) * 0.05 + rnd.gauss(0, 18))
            publicadas = [f for f in fechas_trm if f <= dia.isoformat()]  # la vigente: la última publicada hasta ese día
            if publicadas:
                trm = oficial[publicadas[-1]]
            mercado.append({"fecha": dia.isoformat(), "contrato_c_usd_lb": c, "trm_cop_usd": round(trm, 2)})
        dia += timedelta(days=1)
    ajuste, dias_ajuste = 2.70 - mercado[-1]["contrato_c_usd_lb"], 40  # el último cierre es el real: se corrige en 40 días
    for k, fila in enumerate(mercado[-dias_ajuste:], 1):
        fila["contrato_c_usd_lb"] += ajuste * k / dias_ajuste
    ultimo = mercado[-1]
    escala = (2180000 / 125) / ((2.70 + 0.22) * ultimo["trm_cop_usd"] * 2.20462)  # precio interno real del último día
    for fila in mercado:
        fila["contrato_c_usd_lb"] = round(fila["contrato_c_usd_lb"], 4)
        fila["precio_ref_cop_kg"] = round((fila["contrato_c_usd_lb"] + 0.22) * fila["trm_cop_usd"] * 2.20462 * escala)
    escribir("mercado_diario.csv", mercado)

    escribir("presupuesto.csv", [
        {"rubro": "Compras de cosecha", "asignado_musd": 450, "ejecutado_musd": 380},
        {"rubro": "Logística", "asignado_musd": 38, "ejecutado_musd": 31},
        {"rubro": "Cumplimiento EUDR", "asignado_musd": 2.4, "ejecutado_musd": 0.9}])
    print(f"Datos en {SALIDA}: 600 productores, {n} lotes, 1.000 embarques, 57 reclamos, 3 rubros, {len(mercado)} días de mercado.")


if __name__ == "__main__":
    main()
