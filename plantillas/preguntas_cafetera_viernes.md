# Preguntas para la cafetera del viernes

26 de noviembre de 2026. Copia en el repo del documento del equipo (Claude Docs). Análisis completo y fuentes:
`docs/INDUSTRIA_CAFE_2026.md`.

## Cómo usar esta guía el viernes

No hay tiempo para todas las preguntas: lleven las **6 imprescindibles** (marcadas ★) y escojan 4 o 5 más según lo que
la empresa cuente en su presentación. El objetivo es salir con **un problema, su número y su dueño**, no con una lista
de ideas.

| Rol | Quién | Qué hace |
|---|---|---|
| Pregunta | Quien mejor conversa | Hace las preguntas, repregunta "¿cuánto?" y "¿quién decide?" |
| Anota | Uno del equipo | Escribe cifras y frases textuales; marca en la columna "Lo que tenemos" qué pieza encaja |
| Arma la demo | Quien maneja el kit | Mientras escucha, prepara la pieza del kit o la página de Power BI que responde al dolor que oyó |

Reglas:

1. Escuchen el 70 % del tiempo. Empiecen por su negocio, nunca por la IA.
2. Toda respuesta vaga se repregunta con un número: "¿más o menos cuántos al mes?", "¿cuánto les costó la última vez?".
3. Muestren que hicieron la tarea con una cifra del sector (sección siguiente) antes de preguntar, no después.
4. No prometan nada de la sección final. Si preguntan por precio, respondan con riesgo y margen.
5. Los datos del kit y del tablero son inventados. Si la empresa da cifras propias, esas mandan.

## El sector en 10 cifras verificadas

El año récord quedó atrás: hay menos café, menos pesos por dólar y un mes para cumplir el reglamento europeo. Usen una de
estas cifras para abrir cada bloque de preguntas.

| # | Cifra | Fuente |
|---|---|---|
| 1 | Año cafetero 2024/25: 14,87 millones de sacos (mejor en ~33 años); 2025/26: 12,65 millones (−15 %) | [FNC](https://federaciondecafeteros.org/wp-content/uploads/2026/09/Precios-area-y-produccion-de-cafe-Noviembre-2026.xlsx) |
| 2 | Precio interno: récord de COP 3.380.000 por carga (feb-2025); COP 2.180.000 el 25-nov-2026, con el contrato C en 2,70 USD/lb | [FNC](https://federaciondecafeteros.org/wp-content/uploads/2026/03/precio_cafe.pdf) |
| 3 | En septiembre de 2026 el precio en pesos cayó 30 % aunque en dólares solo 12 %: la tasa de cambio bajó 18,9 % | [FNC, septiembre 2026](https://federaciondecafeteros.org/wp-content/uploads/2026/10/9.-Informe-mensual-Septiembre-2026-p.pdf) |
| 4 | Diferencial colombiano: de 3,6 centavos/lb (feb-2025, mínimo desde 2008) a ~72 centavos/lb (sep–oct 2026) | Ídem |
| 5 | Café sin tostar exportado, ene–ago 2026: USD 3.289 millones (−11,5 %); extractos +18,8 % | [DANE](https://www.dane.gov.co/files/operaciones/EXPORTACIONES/bol-EXPORTACIONES-ago2026.pdf) |
| 6 | Central Cafetera, segundo trimestre de 2026: café verde −29,3 % y productores reteniendo inventarios a la espera de mejores precios | [Banco de la República](https://doi.org/rnmt) |
| 7 | Ene–oct 2026: los 10 mayores exportadores mueven el 73,6 % del volumen; la FNC el 22,8 %; EE. UU. recibe el 40,9 % | [FNC, exportaciones](https://federaciondecafeteros.org/wp-content/uploads/2026/10/Exportaciones-Octubre-2026.xlsx) |
| 8 | Reglamento europeo contra la deforestación: aplica desde el 30-dic-2026 a empresas grandes y medianas; la carga de probar cumplimiento es del exportador | [EUR-Lex 2025/2650](https://eur-lex.europa.eu/eli/reg/2025/2650/oj/eng) |
| 9 | Café verde y tostado excluidos del recargo de 12,5 % de EE. UU. vigente desde julio de 2026 | [El Colombiano](https://www.elcolombiano.com/negocios/eeuu-eleva-arancel-productos-colombianos-trabajo-forzoso-2026-AO39150808) |
| 10 | Fraude por suplantación de correo: ~USD 3.000 millones en pérdidas reportadas en 2025 (FBI); en exportación, el falso "cambiamos de cuenta" | [ABA Banking Journal](https://bankingjournal.aba.com/2026/04/fbi-cybercrime-losses-increased-26-in-2025/) |

Más contexto: 561.766 productores, 97 % con 5 hectáreas o menos; costo de producción de COP 1,68 millones por carga,
69 % mano de obra.

## Las preguntas, por bloque

Cada pregunta trae qué señal buscar y qué pieza nuestra responde. Las ★ son las seis que no pueden faltar.

### A. Negocio y prioridades

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ★ Si este año tuvieran que mejorar un solo número, ¿cuál sería: volumen, margen por saco, días de caja o cumplimiento europeo? | Su prioridad real y el indicador del piloto | Calculadora de ROI; Power BI página 1 (resumen) |
| ¿Cuántos sacos exportaron en 2025 y cómo va 2026 frente a la caída nacional de 11,8 %? | Su tamaño (un top 10 mueve entre ~650.000 y 1,1 millones de sacos) | Reemplazar los datos inventados del tablero por los suyos |
| ¿Qué mezcla venden (verde estándar, especiales, liofilizado o extractos) y hacia dónde quieren crecer? | Diversificación: los extractos crecen 18,8 % mientras cae el verde | Power BI página 5 (margen por comprador y producto) |
| ¿Qué parte de su volumen va a EE. UU., Europa y Asia? | Cuánto pesa el reglamento europeo frente a los aranceles | Power BI página 2 (riesgo Europa) |

### B. Compras y origen

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ¿A cuántos proveedores le compran y por qué canal: cooperativas, intermediarios, directo a finca, la Federación? | Qué tan difícil es la trazabilidad | Maestro de proveedores del guardián (`maestros.json`) |
| En el segundo trimestre el Banco de la República vio productores reteniendo café a la espera de precio. ¿Cómo los afectó y cómo saben cuánto podrán comprar el próximo mes? | Necesidad de pronóstico de volumen comprable | Power BI página 6 (pronóstico con banda de incertidumbre, sin prometer exactitud) |
| ¿Cómo fijan el precio que pagan al productor y cómo comprueban que es el correcto ese día? | Control de precio justo y de errores | Tabla de mercado diario y alerta en Power Automate |
| ¿Cuánto esperan que los afecte El Niño declarado en octubre? | Riesgo de oferta para 2027 | Escenarios en Power BI |

### C. Precio, cobertura y riesgo

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ★ ¿Cuánto café tienen hoy comprado o vendido sin precio fijado, y cada cuánto lo ven consolidado? | Si dicen "en Excel, cada semana": oportunidad del panel de riesgo | Power BI página 7 (mercado del día): cada centavo vale USD 1,3 millones por millón de sacos |
| La tasa de cambio explicó buena parte de la caída del precio interno. ¿Cómo cubren el riesgo del peso? | Si gestionan los tres componentes: bolsa, diferencial y tasa de cambio | Medidas de TRM y diferencial en el tablero |
| ¿Qué pasó con sus garantías en las subidas de 2024–2025? ¿Tuvieron que buscar crédito? | Dolor de liquidez (el sector puso ~USD 7.000 millones en garantías en nov-2024) | Panel de riesgo con alertas |
| ¿Quién decide fijar precio o cubrirse, y con qué reglas escritas? | Si hay reglas, el código las puede vigilar | Guardián con `politica.json` y aprobación humana en Teams |

### D. Compradores y margen

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ¿Cuál es su cliente más rentable y cómo lo saben: por precio, por margen por saco o por reclamos? | Si miden margen o solo precio | Power BI página 5 (dispersión precio contra margen) |
| El diferencial colombiano pasó de 3,6 a ~72 centavos por libra. ¿Cuánto de eso capturaron y qué lo explica: calidad, origen, cumplimiento? | Dónde está su ventaja real | Medida de diferencial promedio por comprador |
| ¿Cuántos reclamos de calidad tuvieron este año y cuánto costaron? | El costo medido de la calidad | Power BI página 3; asistente que responde con la cifra y su fuente |
| ¿Sus compradores les piden datos nuevos: huella de carbono, trazabilidad, trabajo infantil? | Exigencias que vienen | Cifras verificadas con fuente en el kit |

### E. Reglamento europeo contra la deforestación

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ★ Falta un mes para el 30 de diciembre. ¿Qué porcentaje de su café con destino a Europa ya tiene el expediente completo, incluida la legalidad? | La oportunidad número 1: la carga es del exportador | Regla del kit que bloquea el lote sin geolocalización; flujo de despacho; Power BI página 2 |
| ¿Usan el SICA de la Federación para la geolocalización? ¿Qué les falta: tenencia de la tierra, trabajo? | La brecha difícil es la legalidad, no el mapa | El asistente puede listar los faltantes por lote |
| ¿Cuánto tiempo toma armar un expediente por embarque y quién lo hace? | La línea base en horas | Bitácora con tiempos de cada paso |
| ¿Algún importador europeo les ha retenido o rechazado un lote por esto? | Dolor con número | Aprobación de Calidad en Teams antes del despacho |

### F. Calidad

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ¿Cómo registran la catación y el análisis físico por lote, y está conectado al precio de venta y a los reclamos? | Si existe historia etiquetada (sin ella no hay modelo posible) | Snowflake + Power BI página 3 |
| ¿Cuántas muestras catan al día y con cuántos catadores? | Cuello de botella de calidad | Asistente que consulta resultados por lote |
| ¿Han probado equipos de calidad con IA, como espectroscopía o visión? | Madurez; en Brasil la IA apoya a los catadores, no los reemplaza | Fase 2, con aliados (por ejemplo, la línea NIRS de Cenicafé) |

### G. Logística y documentos

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ★ ¿Cuántos documentos mueve un embarque (contrato, instrucción, conocimiento de embarque, factura, certificados de origen, OIC y Almacafé, carta de crédito) y cuánto tardan en conciliarlos? | El piloto más rápido de montar | El kit lee documentos con el escudo, marca discrepancias y deja la acción pendiente de aprobación |
| ¿Qué porcentaje de embarques sale en la fecha prometida? ¿Dónde se pierde el tiempo? | Cumplimiento al cliente | Power BI página 6 (% a tiempo, retraso por cliente) |
| ¿Les han rechazado documentos en el banco o en destino? ¿Cuánto costó? | Dolor con número | Bitácora de cada revisión |
| En 2023 la caída de IFX Networks tumbó la plataforma del ICA y retrasó exportaciones. ¿Los afectó? ¿Qué plan tienen si cae un proveedor? | Dependencia de terceros | Flujo de respaldo en Power Automate; la demo funciona sin red |

### H. Datos y tecnología

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ★ ¿Dónde viven hoy los datos de compras, inventario, contratos y calidad: ERP, Snowflake o Excel por área? | Si ya están en Snowflake, el piloto es de días | `kit.snowflake traer`: consulta de solo lectura, cifras selladas y registradas |
| ¿Qué usan de Microsoft: Teams, Power BI, Power Automate, Copilot, Azure? | Encaje con lo que ya pagan | Aprobaciones en Teams, tablero en Power BI, modelo en Azure |
| ¿Han probado IA generativa? ¿Qué salió bien y qué no? | Miedos y aprendizajes | Cifras con su fuente y juez que revisa |
| ¿Quién en TI tendría que aprobar un piloto de dos semanas que solo lee datos? | Ruta de aprobación | Informe de pruebas de seguridad (118 ataques, 0 pasaron) |

### I. Seguridad y fraude

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ¿Les han intentado cambiar la cuenta bancaria por correo, a ustedes o a sus compradores? ¿Les ha llegado la estafa que suplanta a la Federación? | El fraude más común en exportación | Guardián: solo la cuenta registrada; el pago lo aprueba una persona |
| Si un asistente lee correos de compradores y PDF de proveedores, ¿qué les preocuparía que saliera mal? | Su miedo concreto; ya pasó con EchoLeak (2025) | 16 firmas en español + Prompt Shields + juez; el escudo de documentos de Microsoft viene apagado por defecto y el kit lo cubre |
| ¿Quién puede aprobar hoy un pago o un despacho, y queda registro de quién lo aprobó? | Segregación de funciones | Bitácora encadenada y firmada; parada automática tras 3 incidentes |
| ¿Cómo manejan los datos personales de los productores (cédula, finca) frente a la Ley 1581 y la circular de IA de la SIC? | Riesgo legal (multas de hasta ~COP 3.500 millones) | Marcadores de datos personales: el modelo no ve cédulas ni nombres |

### J. Presupuesto y decisión

| Pregunta | Qué buscamos | Lo que tenemos |
|---|---|---|
| ★ Si en dos semanas les mostramos [el problema que nombraron] resuelto con sus datos, ¿quién tendría que verlo para decir que sí y qué número tendría que moverse? | Patrocinador y criterio de éxito | Piloto de dos semanas con la medición antes y después |
| ¿Esto entraría en el presupuesto de este año o en el plan de 2027? | Urgencia real | Costo bajo: servicios gratuitos o de pago por uso en Azure |
| ¿Han hecho pilotos con Microsoft o Snowflake? ¿Cómo los midieron? | Cómo evalúan | Medición automática antes y después (`kit.medir`) |

## Si dicen X, mostramos Y

El dolor que nombren decide la demo. Las cuatro primeras filas son las de mayor valor según la investigación; nuestro kit
encaja mejor en las que leen documentos, muestran cifras y proponen acciones.

| Si dicen… | Oportunidad | Qué mostramos (45 segundos) | Cómo medir el piloto |
|---|---|---|---|
| "No sabemos si llegamos al 30 de diciembre con Europa" | Expediente del reglamento europeo y legalidad por lote | Pedir el despacho de un lote a Europa sin geolocalización: se bloquea solo. Uno completo va a aprobación de Calidad en Teams | % del volumen a Europa con expediente completo; horas por expediente |
| "La posición la consolidamos en Excel" o "nos agarraron las garantías" | Panel de riesgo: posición, diferencial, tasa de cambio y liquidez | Power BI página 7 y la alerta diaria; el asistente da el precio del día con fuente y fecha, sin pronosticar | Horas para cerrar la posición diaria; alertas a tiempo |
| "Los documentos de exportación nos quitan días" | Mesa documental de exportación | Un correo de un "comprador" con instrucción escondida para cambiar la cuenta: el escudo la bloquea y la acción queda pendiente en Teams | Minutos por embarque; rechazos bancarios; días de cobro |
| "Nos estafaron" o "nos intentaron cambiar la cuenta" | Control de pagos | El guardián rechaza la cuenta no registrada aunque el modelo la proponga; queda en la bitácora | Intentos bloqueados; tiempo de aprobación |
| "No sabemos qué cliente nos deja más" | Analítica de margen por cliente | Power BI página 5 y la pregunta al asistente con la cifra verificada | Margen por saco por segmento |
| "Los reclamos de calidad nos cuestan" | Copiloto de contratos y reclamos | El asistente responde el costo de reclamos con su fuente; Power BI página 3 | Tiempo de respuesta a reclamos |
| "No sabemos cuánto café vamos a poder comprar" | Pronóstico de volumen comprable | Power BI página 6, contando con honestidad qué datos faltan (2–3 años de historia y clima) | Error del pronóstico frente a las compras reales |
| "Tenemos todo en Snowflake y nadie lo usa" | Asistente sobre Snowflake | Traer las cifras de Snowflake, sellarlas y preguntar: la respuesta trae su fuente y la huella | Preguntas respondidas sin analista |

Cierre sugerido: "No les vendemos una IA que adivina el precio. Les mostramos una que trabaja con sus datos, no se deja
engañar por un correo y no mueve un peso sin que una persona lo apruebe."

## Lo que no prometer y las cifras que no usar

Un jurado que conoce el café descuenta puntos por cualquier promesa de esta tabla.

| No prometer | Qué decir en su lugar |
|---|---|
| Predecir el precio o "ganarle al mercado" | Los estudios del Banco de la República, el FMI y el NBER no encuentran ventaja sistemática. Medimos el riesgo cada día y decidimos con reglas |
| Un retorno de inversión "de la industria" | Ninguna exportadora colombiana ha publicado uno medido. El piloto mide la línea base |
| Cumplimiento europeo automático | La IA arma el expediente y señala faltantes; la legalidad la decide una persona |
| Detección perfecta de ataques | Defensa en capas: firmas, Prompt Shields, juez, guardián y aprobación humana |
| Que la aprobación humana basta | Quien aprueba ve los datos crudos, no solo el resumen del asistente |
| Reemplazar catadores o extensionistas | En los casos reales la IA los apoya |
| IA en finca lista (roya o madurez por foto) | En campo la precisión baja a ~81,5 % y no hay despliegue en Colombia |
| Funciones de Snowflake Cortex o Microsoft Fabric | No las hemos probado |

Cifras que circulan y **no** deben usar: "99 % de fincas geolocalizadas", "280.000 familias en riesgo", "960.000 empleos
directos", un porcentaje nacional de cafés especiales, la edad promedio de 55 años del caficultor (dato de ~2013) y los
nombres de ministros actuales (sin verificar en fuente oficial). Para el peso del café en el PIB digan "≈1,5–1,8 %,
estimación de la Federación".
