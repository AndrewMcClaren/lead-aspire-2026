# Plantilla de Power BI: exportadora de café

Un tablero de siete páginas sobre una exportadora de café **ficticia**, listo para armar en unos 30 minutos y para cambiar
por los datos del cliente el viernes. Sus números coinciden con el caso del kit (`casos/cafe`): **el tablero y el
asistente dicen lo mismo** (1.250.000 sacos, 520 millones de dólares en ventas, 71 % de lotes con geolocalización, 42 % a
Europa, 57 reclamos por 3,1 millones de dólares, 6 días de documentos por embarque). Los precios son una serie ficticia del
contrato C más un diferencial por calidad y comprador: sirven para practicar, no son precios reales.

| Archivo | Qué es |
|---|---|
| `datos/*.csv` | Productores, lotes, embarques, reclamos y presupuesto (inventados, con semilla fija) |
| `tema_cafe.json` | Los colores beige y café, iguales a la página del kit |
| `datos/trm_oficial.csv` | La TRM **oficial** de cada día (Superintendencia Financiera, API abierta de datos.gov.co), traída con `python -m kit.mercado trm` |
| `datos/mercado_diario.csv` | El mercado de cada día hábil del año: TRM oficial; contrato C simulado que termina en el cierre real del 25-nov-2026 (contrato C 2,70 USD/lb; precio interno COP 2.180.000 por carga) |
| `medidas.dax` | Las 33 medidas para copiar y pegar (incluye precio, margen por comprador y entregas a tiempo) |
| `snowflake.sql` | Las mismas tablas en Snowflake, para conectar Power BI a Snowflake |
| `generar_datos.py` | Regenera los CSV (`python plantillas/powerbi/generar_datos.py`) |

Power BI Desktop es gratis (Microsoft Store). Para armar y presentar el tablero en el computador no hace falta licencia;
publicarlo y compartirlo en línea sí pide Power BI Pro.

## 1. Cargar los datos (5 minutos)

**Antes de importar, un paso que evita el error más común:** Archivo → Opciones y configuración → Opciones →
**Configuración regional** (en "Archivo actual") → Configuración regional para la importación: **Inglés (Estados Unidos)**.
Los CSV usan punto decimal (83.5); con la configuración de Colombia, Power BI leería 835.

1. Inicio → **Obtener datos** → **Texto/CSV** → `datos/lotes.csv` → **Cargar**.
2. Repitan con `productores.csv`, `embarques.csv`, `reclamos.csv`, `presupuesto.csv` y `mercado_diario.csv`.
3. Vista de **modelo** (ícono de las tres cajas, a la izquierda): arrastren
    - `lotes[productor_id]` sobre `productores[productor_id]`
    - `reclamos[embarque_id]` sobre `embarques[embarque_id]`
4. Vista → **Temas** → **Examinar temas** → `tema_cafe.json`.

**Desde Snowflake** (si el cliente o el jurado preguntan "¿y con nuestros datos?"): corran `snowflake.sql` en su cuenta de
prueba, carguen los CSV, y en Power BI: Obtener datos → **Snowflake** → servidor `<cuenta>.snowflakecomputing.com`,
almacén `COMPUTE_WH` → base `CAFE` → esquema `PUBLIC` → las seis tablas → **Importar**.

## 2. Las medidas (5 minutos)

Inicio → **Nueva medida**, peguen una medida de `medidas.dax` y Enter. Repitan con cada una. Después, en la pestaña de
la medida, pongan el formato: **Porcentaje** para las que empiezan con %, **Número entero con separador** para sacos y
lotes, **Moneda** para las de USD.

## 3. Las páginas (20 a 30 minutos)

Regla de diseño: **una pregunta por página**, como mucho 5 objetos, títulos que dicen la conclusión ("619 lotes que van a
Europa no tienen geolocalización"), no el nombre del gráfico.

**Página 1 · Resumen** ("¿Cómo vamos este año?")
- 4 tarjetas: `Sacos`, `% lotes con geolocalización`, `Costo reclamos (USD)`, `Días promedio de documentos`.
- Gráfico de columnas: eje `lotes[mes]`, valor `Sacos`.
- Barras: eje `lotes[destino_mercado]`, valor `Sacos` (ordenadas de mayor a menor).

**Página 2 · Riesgo Europa** ("¿Qué no puede entrar a Europa?") — la página que más le importa al cliente
- Tarjetas: `Lotes a Europa sin geolocalización` y `Sacos en riesgo para Europa`.
- Barras: eje `lotes[region]`, valor `% lotes con geolocalización` (de menor a mayor: dónde trabajar primero).
- Tabla: `lote_id`, `region`, `comprador`, `sacos_60kg`, con filtro de página `destino_mercado = Unión Europea` y
  `geolocalizado = No`. Es la lista de trabajo para el área de sostenibilidad.

**Página 3 · Calidad y reclamos** ("¿Dónde perdemos plata por calidad?")
- Tarjetas: `Reclamos`, `Costo reclamos (USD)`, `Costo por reclamo (USD)`.
- Barras: eje `reclamos[motivo]`, valor `Costo reclamos (USD)`.
- Columnas: eje `lotes[mes]`, valor `Lotes rechazados`.

**Página 4 · Presupuesto** ("¿Cuánto nos queda y dónde?")
- Barras agrupadas: eje `presupuesto[rubro]`, valores `Presupuesto ejecutado (M USD)` y `Saldo disponible (M USD)`.
- Tarjeta: `% ejecución del presupuesto`.

**Página 5 · Precio y compradores** ("¿A quién nos conviene venderle?")
- Tarjetas: `Precio promedio (USD/lb)`, `Contrato C promedio (USD/lb)`, `Diferencial promedio (USD/lb)`, `% margen`.
- Gráfico de dispersión: eje X `Precio promedio (USD/lb)`, eje Y `% margen`, tamaño `Sacos`, leyenda `lotes[comprador]`. Arriba
  a la derecha quedan los compradores que pagan mejor y dejan más margen.
- Barras: eje `lotes[comprador]`, valor `Margen por saco (USD)`, de mayor a menor. En el ejemplo, el mejor comprador deja
  14,9 % de margen y el peor 11,6 %, con precios parecidos: la diferencia está en el diferencial que pagan por la calidad.

**Página 6 · Pronóstico y entregas** ("¿Cuánto vamos a vender y llegamos a tiempo?")
- Gráfico de líneas: eje `lotes[mes_fecha]` (en el panel de formato, eje X de tipo **Continuo**), valor `Sacos`. Luego, en el
  panel **Análisis** (ícono de lupa) → **Pronóstico** → Agregar: longitud **3 meses**, intervalo de confianza **95 %**. Power BI
  dibuja la proyección con su banda de incertidumbre.
- Tarjetas: `% embarques a tiempo` y `Retraso promedio (días)`.
- Barras: eje `embarques[comprador]`, valor `% embarques a tiempo`: a qué clientes les estamos fallando.

**Página 7 · Mercado del día** ("¿Cómo se movió hoy y qué nos cuesta?")
- Tarjetas: `Contrato C último (USD/lb)`, `Cambio semanal del contrato C`, `TRM última`.
- Gráfico de líneas: eje `mercado_diario[fecha]`, valor `contrato_c_usd_lb`; agreguen en Análisis una **línea constante** con el
  precio objetivo que defina la mesa de coberturas.
- Texto para contarlo: "cada centavo que sube o baja la bolsa mueve 1,3 millones de dólares por cada millón de sacos sin
  precio fijado". Por eso importa ver el dato a diario y decidir con reglas, no adivinar.

Del pronóstico, digan lo que es: con un año de datos es una proyección de tendencia. El café tiene cosecha principal y mitaca;
para capturar esa temporada hacen falta dos o tres años de historia, y la producción depende del clima, que estos datos no
tienen.

## 4. Cómo usarlo en la demo (30 segundos)

1. Página 2: "619 lotes que van a Europa, 155.094 sacos, no tienen la geolocalización de sus fincas: no podrían entrar".
2. Clic en la región con menor porcentaje: la tabla muestra exactamente qué lotes y de qué comprador.
3. Cambien al kit y pregunten: "¿Qué porcentaje de los lotes tiene geolocalización?" → **71 %, la misma cifra, con su
   fuente**. "El tablero muestra; el asistente responde con la misma verdad y no deja despachar a Europa sin ella."

## Para el caso del cliente

Si el viernes el cliente da otros datos, reemplacen los CSV por los suyos con columnas parecidas (o conecten su Snowflake)
y ajusten las medidas. Si sus datos tienen otra forma, armen solo la página que responde su pregunta principal: una
página bien hecha vale más que cuatro a medias.

No usen el pronóstico ni Copilot de Power BI sin probarlos antes: Copilot en Power BI pide una capacidad de pago que la
cuenta de estudiante no tiene.
