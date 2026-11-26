# Guía de entrevista ejecutiva: exportadora de café

**Contexto:** exportadora de café colombiana (genérica del sector) · entrevistado: gerente general o director de operaciones ·
objetivo: encontrar en 45 minutos el problema que vale la pena resolver con IA el mismo día, con su número de antes.

**Cómo usarla:** no lean todo. Hagan el mapa de la sección 1 (10 minutos), escojan 4 o 5 preguntas de la sección 2 según lo
que salga, cierren con 2 de la sección 3, y anoten las señales de la sección 5. Uno pregunta, uno anota **textual**, uno
escucha números. Pidan siempre un número aproximado: "¿más o menos cuánto? un rango me sirve".

## 1. Mapa de punta a punta (6 preguntas)

| # | Pregunta | Qué pieza del negocio mapea |
|---|---|---|
| 1 | "Cuéntenos el recorrido de un saco: ¿a quién le compran, cuántos productores o cooperativas son y cómo fijan el precio que les pagan (precio interno, diferencial, primas)?" | Abastecimiento, base de proveedores y exposición al precio |
| 2 | "Desde que llega el pergamino hasta que sale el excelso, ¿dónde se mide la calidad (factor de rendimiento, humedad, catación) y quién decide si un lote se rechaza o se baja de categoría?" | Transformación, control de calidad y mermas |
| 3 | "¿Cómo se cierra una venta: contratos a precio fijo o a diferencial sobre el contrato C? ¿Cuántos compradores pesan el 80 % del volumen?" | Canales de venta, concentración de clientes y riesgo de precio |
| 4 | "Desde que cierran un contrato hasta que el contenedor sale de Buenaventura o Cartagena, ¿cuántos días pasan y qué documentos hay que reunir? ¿Dónde se atasca?" | Logística, puertos y ciclo de documentos |
| 5 | "Cuando un comprador recibe el café, ¿qué pasa si la taza no coincide con la muestra? ¿Cuántos reclamos tienen al año y cómo se resuelven?" | Postventa, calidad percibida y costo de reclamos |
| 6 | "¿Cuántos de sus compradores vuelven a comprarles la siguiente cosecha, y qué les piden hoy que antes no pedían (trazabilidad, certificaciones, sostenibilidad)?" | Recurrencia, retención y nuevos requisitos del mercado |

## 2. Preguntas por rol para encontrar los puntos débiles (12)

**Strategy Manager (riesgos ocultos y dependencia)**
1. "Si mañana el reglamento europeo contra la deforestación (EUDR) se aplicara en serio a todos sus lotes, ¿qué porcentaje de lo que venden a Europa podría salir sin problema?" — revela el tamaño del riesgo regulatorio y si ya lo midieron (verifiquen la fecha de aplicación vigente: se ha aplazado).
2. "¿Qué pasaría si su comprador más grande se fuera con otra exportadora? ¿Qué los hace difíciles de reemplazar hoy?" — revela concentración de clientes y si su ventaja es real o solo precio.
3. "¿Qué parte de la operación depende de una sola persona, un solo sistema o un solo puerto?" — revela puntos únicos de falla.

**Business Analyst y Finanzas (ineficiencias y fugas de margen)**
4. "¿Qué reporte o tarea se hace a mano cada mes, cuántas personas participan y cuántos días toma?" — revela horas recuperables (la base del ROI).
5. "¿Cuánto les costaron el año pasado los reclamos, los descuentos por calidad y las demoras en puerto, sumados?" — revela la fuga de margen en pesos o dólares.
6. "Entre que pagan la cosecha y cobran al comprador, ¿cuántos días pasan? ¿Cuánto capital tienen inmovilizado en inventario?" — revela el costo del ciclo de caja.

**CMO (oportunidades comerciales y cliente final)**
7. "Cuando un comprador pide una cotización o un perfil de taza específico, ¿cuánto tardan en responderle con disponibilidad, calidad y precio?" — revela fricción comercial y ventas perdidas por lentitud.
8. "¿Qué saben de lo que hace el comprador con su café (marca, tostión, cliente final) y lo usan para venderle más?" — revela falta de visibilidad del cliente final.
9. "¿Cuánto más pagan por un lote especial o certificado y qué tan fácil es demostrarle al comprador de dónde viene?" — revela primas que se pierden por no poder probar origen y calidad.

**CPO (datos, silos y escalabilidad)**
10. "Si les pido ahora el porcentaje de lotes con geolocalización completa, ¿cuánto tardan en dármelo y de cuántos sistemas o archivos sale?" — revela silos y madurez de datos en una sola pregunta.
11. "¿Qué guardan en Snowflake hoy y quién lo consulta? ¿El área comercial o de calidad puede sacar una cifra sin pedírsela a un analista?" — revela si los datos existen pero no se usan.
12. "¿Ya usan IA o automatización en algo? ¿Sus empleados usan ChatGPT por su cuenta, y con qué datos?" — revela madurez, IA en la sombra y el riesgo que ya existe.

## 3. Presupuesto y capacidad de inversión (5 preguntas diplomáticas)

1. "De lo que invierten en tecnología al año, ¿qué parte se va en mantener lo que ya tienen y qué parte en proyectos nuevos?" — revela la proporción Run / Grow; si casi todo es Run, el piloto debe ser barato y rápido.
2. "Cuando aprobaron su último proyecto de tecnología, ¿qué número convenció al comité: ahorro de horas, menos pérdidas, más ventas o cumplir una norma?" — revela qué métrica usar en el pitch.
3. "¿En cuántos meses esperan que una inversión así se pague sola?" — revela el periodo de recuperación exigido; pongan ese número en la calculadora de ROI.
4. "¿Quién tendría que decir que sí a un piloto de dos semanas, y quién firma si después se vuelve un proyecto?" — revela el dueño del presupuesto y el ciclo de aprobación.
5. "¿Cuándo se definen los presupuestos del próximo año? ¿Hay algún rubro de cumplimiento, sostenibilidad o transformación digital que ya esté aprobado?" — revela la ventana de compra y si hay plata etiquetada (por ejemplo, para cumplir con Europa).

## 4. Hipótesis de soluciones con IA (para validar con el cliente, no para vender a ciegas)

Los impactos usan las cifras del caso ficticio `casos/cafe` como ejemplo; el viernes se calculan con los números que dé el cliente.

| Dolor que puede salir | Solución con IA | Impacto financiero esperado | Complejidad |
|---|---|---|---|
| Lotes que van a Europa sin trazabilidad completa | **Agente con reglas**: responde qué lotes están completos con datos verificados de Snowflake y no deja despachar a Europa un lote sin geolocalización (aprobación en Teams) | Protege el acceso a Europa (42 % del volumen en el ejemplo); evita devoluciones o rechazos en destino | **Media**: el kit ya lo hace (`casos/cafe`) |
| Reclamos de calidad costosos | **Predictiva**: alerta de riesgo de reclamo por lote con humedad, factor, catación y comprador | Si los reclamos bajan 20 %: 0,6 millones de dólares al año (sobre 3,1 millones del ejemplo) | **Media-alta**: requiere historial de reclamos por lote |
| Documentos de embarque lentos | **GenAI + extracción**: lee certificados y facturas (Document Intelligence), arma el paquete y marca lo que falta | De 6 a 2 días por embarque; menos demoras y multas en puerto | **Media** |
| Cifras que tardan días en llegar al comercial | **Asistente sobre Snowflake** con cifras verificadas y su fuente, en Teams | Horas de analista liberadas y cotizaciones más rápidas | **Baja-media**: el kit ya lo hace |
| Capital inmovilizado entre cosechas | **Predictiva**: pronóstico de compras por región y semana para planear caja | Menos costo financiero del inventario | **Alta**: datos históricos limpios y validación con la mesa de coberturas |

Regla: el viernes escojan **una** fila, la que tenga número del cliente, encaje con lo que ya usa y se pueda demostrar en
unas horas. No prometan predecir el precio del café.

## 5. Señales de compra y bloqueadores

**Señales verdes (hay urgencia y plata)**

| Lo que dicen | Por qué importa |
|---|---|
| "Esto nos costó X el año pasado" (con un número) | El dolor está medido: el ROI se calcula solo |
| "La auditoría o el comprador europeo nos lo están pidiendo para la próxima cosecha" | Hay fecha límite externa: urgencia real |
| "Ya tenemos los datos en Snowflake, pero nadie los aprovecha" | La base técnica existe: el piloto es rápido |
| "Si funciona, lo llevo al comité el próximo mes" | Hay patrocinador y ruta de aprobación |

**Señales rojas (estancamiento) y cómo destrabarlas**

| Lo que dicen | Qué significa | Repregunta |
|---|---|---|
| "Todo está en Excel de cada área" | Datos dispersos, sin fuente única | "¿Cuál de esos archivos usan para decidir? Empecemos solo con ese." |
| "Eso lo decide TI / casa matriz" | No hay patrocinio en la sala | "¿Qué tendría que ver TI para decir que sí a un piloto de dos semanas que solo lee datos?" |
| "No sabemos cuánto nos cuesta" | Dolor sin medir | "Si tuviera que adivinar: ¿más o menos de 100 millones al año? ¿Más o menos de 500?" |
| "La IA se equivoca, no confiamos" | Miedo legítimo, no un no | "¿Qué tendría que pasar para confiar? ¿Que cada cifra muestre su fuente y que nada se apruebe sin una persona?" (ahí entra el kit) |

## 6. Las cinco preguntas de comercio exterior (con respuesta honesta)

Las planteó un experto en relaciones económicas internacionales. Son las que un gerente comercial o financiero de una
exportadora se hace todos los días. Para cada una: qué puede hacer la IA de verdad, qué no, y qué pieza del kit o del
tablero lo muestra. **Regla de oro: nadie predice el precio de la bolsa de forma consistente; quien prometa eso pierde
credibilidad ante un jurado que conoce el negocio.**

| Pregunta | Qué sí se puede hacer | Qué no | Cómo lo mostramos |
|---|---|---|---|
| 1. ¿Cómo tener los mejores precios del mercado? | El precio de exportación = contrato C de Nueva York + **diferencial**. El C no lo controla nadie; el diferencial sí: calidad (puntaje de taza), trazabilidad para Europa y cumplimiento de entregas suben la prima. La IA muestra qué lotes y regiones ganan más diferencial | Garantizar vender "al precio más alto" | Power BI página 5: `Diferencial promedio (USD/lb)` por comprador y puntaje |
| 2. ¿Cómo sacar ventaja de las bolsas internacionales? | Ver el mercado **a diario** con reglas fijadas de antemano: alerta cuando el C cruza el precio objetivo o se mueve más de 3 % en una semana, y la mesa de coberturas decide si fija precio. Medir la exposición: cuánto vale cada centavo de movimiento | Que la IA opere o "adivine" la bolsa | Power BI página 7 (mercado del día) + alerta de Power Automate con aprobación humana |
| 3. ¿Cuál es el mejor comprador para tener más rentabilidad? | Comparar compradores por **margen por saco**, no por precio: uno que paga parecido puede dejar 3 puntos más de margen porque premia la calidad, reclama menos y paga a tiempo | Elegir comprador solo con datos de un año | Página 5: dispersión precio contra margen; en el ejemplo, 14,9 % frente a 11,6 % |
| 4. ¿Se puede predecir la venta con históricos para dimensionar la producción? | Una proyección de tendencia con banda de incertidumbre (pronóstico de Power BI). Con 2 o 3 años de historia capta la cosecha principal y la mitaca | Predecir la cosecha sin datos de clima y floración; dar un número sin su margen de error | Página 6: pronóstico a 3 meses con intervalo de 95 % |
| 5. ¿Cómo llegar a tiempo con lo que el cliente necesita? | Medir `% embarques a tiempo` por cliente contra la fecha prometida, ver dónde se pierde el tiempo (documentos: 6 días por embarque) y bloquear antes lo que no va a pasar en destino (lote sin geolocalización a Europa) | Controlar navieras o puertos | Página 6 + flujo de despacho con regla automática y aprobación en Teams |

**Si preguntan "¿y el precio de todos los días?"** El valor del saco cambia cada día (en los datos de práctica, 1,2 % en
promedio y hasta 6 % en un día). Sirve para cuatro cosas concretas, ninguna es adivinar:
1. **Exposición:** cuántos sacos están comprados o vendidos sin precio fijado, y cuánto se gana o pierde por centavo
   (1,3 millones de dólares por cada millón de sacos).
2. **Alertas con decisión humana:** un flujo programado lee el precio cada mañana y avisa a la mesa de coberturas en Teams.
3. **Precio justo al productor:** comparar lo que se paga en cada región con el precio de referencia del día.
4. **Respuestas con fuente y fecha:** el asistente contesta "el contrato C cerró en 2,70 USD/lb el 25 de noviembre de 2026"
   con la Federación Nacional de Cafeteros como fuente (dato real, ya está en el caso), nunca un precio inventado.

Fuentes reales (para decirlo, no para usarlas el viernes sin permiso): el contrato C se publica en ICE Futures (redistribuir
sus datos exige licencia; también hay proveedores en Snowflake Marketplace), la Federación Nacional de Cafeteros publica el
precio interno de referencia y el Banco de la República la TRM.

## Si quien presenta es Snowflake o Microsoft

Probablemente vengan como aliados, no como el cliente. Tres preguntas que valen oro:
- "¿Qué ven que más le cuesta a una empresa como esta para sacarle valor a sus datos?"
- "¿Qué combinación de Snowflake y Microsoft recomendarían para un piloto de dos semanas?"
- "¿Qué haría que un jurado de ustedes diga 'esto se puede implementar el lunes'?"

## 7. Banco de preguntas para el viernes y análisis del sector

- **Preguntas para la cafetera, por bloque** (negocio, compras, precio y riesgo, compradores, reglamento europeo,
  calidad, documentos, datos, seguridad y decisión), cada una con qué buscar y qué pieza nuestra responde: documento
  del equipo `plantillas/preguntas_cafetera_viernes.md` (copia del documento "Preguntas para la cafetera del viernes" en Claude Docs).
- **Análisis completo de la industria** con fuentes (FNC, DANE, MinCIT, SIC, Banco de la República, boletines
  Central Cafetera 2026): `docs/INDUSTRIA_CAFE_2026.md`. Notas de cada investigación: `docs/investigacion_cafe/`.
