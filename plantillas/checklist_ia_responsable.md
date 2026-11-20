# Lista de verificación de IA responsable (para la solución del cliente)

Respondan sí o no, con la evidencia. Si una respuesta es "no", escriban qué falta. Al final, la compuerta
decide si la solución está lista para un piloto. Sirve como lámina de respaldo para la pregunta "¿y cómo
saben que es seguro?".

| # | Pregunta | Sí / No | Evidencia (archivo, prueba o demo) |
|---|---|---|---|
| **Datos** | | | |
| 1 | ¿Cada cifra que muestra la IA sale de una fuente del cliente, con la fuente visible? | | `kit/datos/cifras.csv`, sello "Cifra verificada" |
| 2 | ¿Los datos personales o confidenciales están fuera del repositorio y de la bitácora? | | `.gitignore`, bitácora solo con huellas |
| 3 | ¿Sabemos qué datos NO tenemos y la IA lo dice? | | Pregunta sin dato en la demo |
| **Entrada** | | | |
| 4 | ¿Los documentos externos se revisan antes de que la IA los lea? | | Escudo: firmas, Prompt Shields, juez |
| 5 | ¿Si un servicio de revisión falla, el documento no pasa? | | Prueba de falla cerrada |
| **Salida** | | | |
| 6 | ¿Una cifra inventada, escrita a mano o en palabras, no llega a la persona? | | `kit.medir`: cifras inventadas |
| 7 | ¿Se detecta si la IA intenta revelar sus instrucciones? | | Canario |
| **Acciones** | | | |
| 8 | ¿Está escrito qué puede hacer la IA sola y qué no (nivel de autonomía)? | | `kit/datos/politica.json` |
| 9 | ¿Las acciones sensibles esperan a una persona? | | Bandeja de aprobaciones |
| 10 | ¿Los destinos de pagos o envíos salen de datos maestros que la IA no puede cambiar? | | `kit/datos/maestros.json` |
| 11 | ¿Quien pide una acción no puede aprobarla? | | Prueba de segregación |
| 12 | ¿Una acción que el usuario no pidió se bloquea? | | Prueba de intención |
| **Trazabilidad** | | | |
| 13 | ¿Cada decisión queda registrada y se puede verificar que nadie la alteró? | | `python -m kit.bitacora verificar` |
| 14 | ¿Sabemos cuánto cuesta y cuánto tarda cada respuesta? | | Latencia, tokens y costo en la página |
| **Medición** | | | |
| 15 | ¿Medimos antes y después con casos del cliente? | | Tabla de `kit.medir` |
| 16 | ¿Algún ataque lo escribió alguien que no vio el kit? | | |
| 17 | ¿Reportamos los resultados malos y el intervalo de confianza? | | |
| **Personas** | | | |
| 18 | ¿Está claro quién usa la solución, quién aprueba y quién mantiene los datos maestros? | | Lienzo del problema |
| 19 | ¿La persona que aprueba tiene lo necesario para decidir (motivos, fuente, monto, destino)? | | Tarjeta de la acción |
| 20 | ¿Hay un plan si la IA no está disponible (proceso manual)? | | |

## Compuerta

| Resultado | Cuándo | Qué decir en el pitch |
|---|---|---|
| **Go** | Sí en 1, 4, 6, 8, 9, 10, 11 y 13, y al menos 16 de 20 en total | "Listo para un piloto de dos semanas con un área." |
| **Go condicionado** | Sí en 6, 9 y 13, pero falta alguno de los obligatorios | "Listo para piloto si antes resolvemos ___." |
| **No-go** | No en 6, 9 o 13 | "Todavía no: falta ___ para que la IA no invente ni actúe sola." |

La compuerta es una regla del equipo, no una certificación. Lo que vale es la evidencia de la última columna.
