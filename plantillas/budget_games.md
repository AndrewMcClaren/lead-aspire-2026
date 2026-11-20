# AI Budget Games: cómo prepararse sin conocer las reglas

## Lo que se sabe

Solo esta frase de la descripción oficial de Bogotá: *"Participa en los AI Budget Games, colabora en equipo,
resuelve retos del mundo real y desarrolla soluciones estratégicas."* Después vienen las *"Finales del Case
Championship"*. No encontramos nada público sobre las reglas (búsqueda del 20 de noviembre de 2026), y la edición
de Nueva York no tuvo nada con ese nombre.

## Qué podría ser (hipótesis, no hechos)

| Hipótesis | Cómo sería | Qué tan probable |
|---|---|---|
| **1. Repartir un presupuesto** | Les dan una plata ficticia y una lista de iniciativas o herramientas de IA con su costo. Deciden en qué invertir y lo defienden | La más probable por el nombre |
| **2. Un caso con tope de presupuesto** | El reto de un cliente, como en Nueva York, pero la solución tiene que caber en un monto | Probable |
| **3. Rondas con imprevistos** | Deciden, pasa algo ("se filtraron datos", "recortaron el 20 %") y reajustan | Posible |

Las tres piden lo mismo: **estimar costo y beneficio rápido, priorizar, decir a qué renuncian y por qué, y
defenderlo en pocos minutos.** Eso se puede practicar desde ya.

## El método en 5 pasos (20 minutos)

1. **Listar las opciones** en la tabla de abajo, con costo, beneficio, tiempo hasta ver resultados y riesgo.
   Si no dan un número, estímenlo y márquenlo como estimado.
2. **Ordenar por valor:** beneficio dividido por costo, y primero lo que da resultados en menos de 3 meses
   ("victorias rápidas"). Lo que tarda un año va después, aunque prometa más.
3. **Armar la cartera, sin poner todo en una sola apuesta.** Regla del equipo (no del evento): casi todo a
   victorias rápidas que se miden, a lo sumo una apuesta mediana, una partida fija para **gobierno y seguridad**
   (datos, control humano, medición) y una reserva para imprevistos.
4. **Decir qué NO financian y por qué.** Un jurado valora más una renuncia bien explicada que una lista larga.
5. **Poner la métrica y el punto de corte:** "a los 30 días miramos X; si no bajó, ese dinero pasa a Y".

**Frase para defenderlo:** "Con el mismo presupuesto, preferimos tres cosas pequeñas que se miden en 30 días a
una grande que se mide en un año. Y reservamos una parte para que la IA sea segura, porque eso es lo que permite
usarla en lo importante."

## Tabla para llenar

| Opción | Costo único | Costo mensual | Beneficio mensual (palanca) | Meses hasta ver resultados | Riesgo | ¿Financiamos? | Por qué |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| Gobierno y seguridad de la IA | | | Indirecto: habilita lo demás | | | Sí | |
| Reserva | | | | | | | |
| **Total** | | | | | | | **≤ presupuesto** |

## Lo que cuesta una iniciativa de IA (no olviden nada)

El error típico es contar solo la licencia. Una iniciativa de IA cuesta:

1. **Licencias por usuario** (por ejemplo, Copilot o Power Platform).
2. **Consumo:** tokens del modelo, llamadas a servicios. El kit mide el costo por respuesta.
3. **Integración:** horas de personas para conectarla a los sistemas del cliente.
4. **Datos:** limpiarlos, ordenarlos y mantenerlos (cifras, datos maestros).
5. **Capacitación y cambio:** que la gente la use de verdad.
6. **Gobierno y seguridad:** revisión de riesgos, monitoreo, control humano.
7. **Mantenimiento:** medir cada mes y ajustar.

### Tarea antes del 27: precios de lista verificados

Llenen esta tabla con las páginas oficiales de Microsoft (precio, fecha y enlace). Así, si el juego pide estimar,
no se inventan números. Los precios cambian: no usen precios de memoria.

| Producto | Unidad | Precio de lista (USD) | Fecha y enlace |
|---|---|---|---|
| Microsoft 365 Copilot | usuario/mes | | |
| Copilot Studio | paquete de mensajes o créditos/mes | | |
| Azure OpenAI (el modelo que usen) | millón de tokens de entrada / salida | | |
| Power Automate Premium | usuario/mes | | |
| Power BI Pro | usuario/mes | | |
| Azure AI Content Safety | por cada 1.000 registros (después del nivel gratis) | | |

Para pasar de costo a retorno: `plantillas/calculadora_roi.xlsx`.

## Práctica (20 minutos, cifras inventadas)

**Caso:** una cooperativa de ahorro y crédito tiene **50 millones de pesos** este año para IA. Elijan qué financiar.

| Opción | Costo al año (millones) | Beneficio al año (millones, estimado) | Meses hasta ver resultados | Riesgo principal |
|---|---|---|---|---|
| A. Asistente de preguntas frecuentes para asociados (Copilot Studio) | 12 | 30 | 2 | Que invente condiciones de crédito |
| B. Revisión de facturas de proveedores con aprobación en Teams | 15 | 25 + fraude evitado | 3 | Que pague sola o a una cuenta falsa |
| C. Copilot para las 40 personas administrativas | 30 | 20 (difícil de medir) | 1 | Que suban datos de asociados sin control |
| D. Modelo que predice la mora de los créditos | 25 | 40 | 9 | Sesgo y exigencias regulatorias |
| E. Tablero de indicadores en Power BI con preguntas en lenguaje natural | 6 | 8 | 1 | Cifras mal citadas |
| F. Gobierno y seguridad de la IA (política, capacitación, monitoreo, bitácora) | 6 | Indirecto | 1 | Ninguno: reduce el de las demás |

<details>
<summary>Una respuesta posible (hay otras)</summary>

Financiar F + A + B + E = 39 millones, y un piloto de C con 10 personas (unos 7,5 millones) para medir antes de
comprar para todos. Reserva: 3,5 millones. No financiar D este año: tarda 9 meses, tiene el mayor riesgo
regulatorio y el beneficio es una estimación. Se reconsidera cuando A y B muestren resultados. A y B llevan los
controles del kit (cifras verificadas, aprobación humana), que se pagan con F. Métricas a 30 días: consultas
resueltas sin una persona (A), minutos por factura y pagos a cuentas no registradas (B), horas ahorradas por
persona en el piloto (C).
</details>

## Preguntas para el networking del 24 o para la organización

1. ¿Qué son exactamente los AI Budget Games? ¿Se construye algo o es solo estrategia?
2. ¿El presupuesto es ficticio? ¿Hay un catálogo de opciones con precios?
3. ¿Los Budget Games y el Case Championship son el mismo reto o dos distintos?
4. ¿Todos los equipos presentan o solo los finalistas? ¿Cuánto dura cada presentación?
5. ¿Hay un cliente real, como Mastercard en Nueva York?
6. ¿Hay que llevar portátil? ¿Habrá acceso a Azure, Copilot o Power Platform?
7. ¿Cuáles son los criterios de evaluación?
