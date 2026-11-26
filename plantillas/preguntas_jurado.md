# Preguntas difíciles del jurado y cómo responderlas

Respuestas cortas, de una o dos frases, y **solo con cosas ciertas**. Los corchetes se llenan con los datos del
cliente el día del evento. Si no tienen el dato, digan "no lo medimos todavía; en el piloto lo medimos así: …".

**Regla de oro:** nunca prometan algo que la demo no muestra. Un jurado de Microsoft o de una consultora lo nota.

## Las cinco más probables

**1. "Ya tenemos sistemas complejos (un ERP, sistemas propios) y políticas de TI estrictas. ¿Cuánto cuesta y
cuánto tarda llevar esto a producción?"**
> "No reemplazamos nada: es una capa que se conecta por API o por conectores de Power Platform, y empieza solo
> leyendo datos. Proponemos un piloto con un área y [un proceso]; el costo y el tiempo los estimamos en la
> calculadora con sus números: [resultado]. Lo primero que necesitaríamos es [acceso de solo lectura a X]."

No den semanas ni montos que no salgan de la calculadora con datos del cliente.

**2. "¿Por qué hicieron una parte en código propio en vez de usar solo lo que ya trae Microsoft?"**
> "Usamos [Copilot Studio / Power Automate / Azure AI Content Safety] para lo que ya resuelven bien. Agregamos una
> capa pequeña en Azure que hace algo que el modelo no garantiza: que cada cifra salga de sus datos y que ninguna
> acción delicada se ejecute sin una persona. La IA conversa; el código verifica."

No digan que es "de menos de 200 líneas": el kit completo tiene más de 1.500 y el jurado puede pedir verlo.

**3. "¿Cómo protegen los datos personales (Ley 1581 de 2012) si mandan información a un modelo en la nube?"**
> "La IA nunca ve la cédula ni el correo: antes de llamarla, cambiamos cédulas, correos, teléfonos, cuentas y
> tarjetas por etiquetas, y la respuesta vuelve con los datos solo para quien preguntó. Tampoco ve los valores de
> sus cifras, solo sus nombres. Con Azure OpenAI, según Microsoft, los datos no se usan para entrenar los modelos,
> y el registro guarda la pregunta con etiquetas, no con los datos."

Lo que **no** pueden decir: que detecta *todos* los datos personales (no ve nombres sueltos, direcciones ni datos
de salud escritos en texto libre; para eso está la detección de datos personales de Azure AI Language), ni que
hay una región de Azure OpenAI en Colombia (verifiquen antes). Muéstrenlo en vivo: una pregunta con una cédula y
la línea "La IA recibió: …".

**4. "¿Cuál es el retorno y qué pasa si la gente no lo usa?"**
> "Hoy [el proceso] les cuesta [X horas o pesos] al mes. Con una adopción conservadora de [la mitad de la base],
> el beneficio neto es [resultado de la calculadora] y el piloto se recupera en [meses]. Para que lo usen, va
> donde ya trabajan: [Teams / el sistema que nombró el cliente]."

Muestren el escenario conservador, no el optimista. No mencionen WhatsApp si la demo no lo tiene.

**5. "Si solo pudieran mostrar una métrica a la junta en 30 días, ¿cuál sería?"**
> "[La métrica de la palanca que eligieron], medida antes y después con los mismos casos. Por ejemplo: horas al
> mes en [el proceso] y cero cifras inventadas o pagos sin aprobación en el piloto."

No prometan "100 % de precisión": el kit garantiza que las cifras salen de la tabla, no que el modelo siempre
escoja la correcta. Por eso cada respuesta muestra su fuente.

## Otras que conviene tener listas

| Pregunta | Respuesta |
|---|---|
| ¿Y si el modelo se equivoca? | "No puede escribir cifras: solo cita datos verificados y muestra la fuente. Si no tiene el dato, lo dice. Lo delicado lo aprueba una persona." |
| ¿Y si alguien le esconde instrucciones en un documento? | "Revisamos los documentos antes de que el modelo los lea, y aunque algo pasara, una cifra escrita a mano no sale. Lo mostramos en la demo." |
| ¿Por qué no basta con escribir mejor el prompt? | "Un prompt se puede saltar; una regla en código no. En nuestra medición, sin controles pasaron [X] de [Y] ataques y con el kit [0]." |
| ¿Cuánto cuesta cada respuesta? | "[ms] y [USD] por respuesta con el modelo que usamos; lo mide el propio kit." |
| ¿Le hicieron pruebas de seguridad? | "Sí: una prueba de penetración propia de 147 ataques en 9 frentes, 25 de ellos contra el modelo real de Azure, incluidos documentos con trampas (Word con letra blanca, correos con instrucciones invisibles, cuentas cambiadas). La primera corrida encontró 6 problemas, entre ellos uno de phishing y uno de CSRF; los corregimos y quedaron como pruebas automáticas. Hoy: 0 vulnerables y 13 límites que conocemos y explicamos. No reemplaza una auditoría de terceros." (`docs/SEGURIDAD.md`) |
| ¿Y si secuestran al modelo? | "Lo probamos: hicimos que el modelo escribiera lo que quiere el atacante, cifras falsas en 9 formas, enlaces de phishing, su configuración. Nada de eso llega a la persona, porque el control está en el código, no en el modelo." |
| ¿Siguen algún estándar? | "Nos guiamos por OWASP, NIST y la guía de controles críticos de IA de SANS. Tenemos la tabla control por control, incluidos los que no cubrimos." (`docs/SANS.md`). Nunca "cumplimos". |
| ¿Y si alguien cambia los datos o las cuentas registradas? | "Los datos quedan sellados: si alguien cambia una cifra o una cuenta, el sistema avisa antes de responder." |
| ¿Y si alguien insiste en engañar a la IA? | "Al tercer intento la conversación se detiene sola: sigue respondiendo, pero no puede hacer nada hasta que una persona la revise." (Muéstrenlo: tres veces el documento con trampa y luego un pago.) |
| ¿Cómo saben que va a seguir funcionando en seis meses? | "Corremos la misma prueba cada semana y el sistema la compara con la anterior: si algo empeora, nos avisa y dice qué cambió." |
| ¿Y si alguien abusa de la API o agota el presupuesto? | "Hay un tope de consultas por minuto y cada respuesta muestra su costo." |
| ¿Qué falta para producción? | "[Conectarlo a sus datos reales, pruebas con usuarios, revisión de seguridad de su TI y medir el piloto]." |

## Traductor: de jerga técnica a lenguaje de negocio

En el pitch, usen la columna de la derecha. La de la izquierda es solo para cuando pregunten "¿cómo funciona?".

| No digan | Digan |
|---|---|
| Inyección de instrucciones (prompt injection) | "Alguien esconde una orden en un correo o un documento para engañar a la IA" |
| Firmas locales, saneado | "Un filtro que tacha las frases tramposas antes de que la IA las lea" |
| Prompt Shields | "El filtro de seguridad de Microsoft para IA" |
| Grounding, claves verificadas | "La IA solo puede usar los números de ustedes, con su fuente" |
| Canario | "Una alarma si la IA intenta revelar su configuración" |
| Guardián de acciones, política en JSON | "Las reglas del negocio deciden qué puede hacer la IA sola y qué no" |
| Human-in-the-loop, segregación de funciones | "Lo delicado lo aprueba una persona, y nunca la misma que lo pidió" |
| Bitácora encadenada por hashes, HMAC | "Un registro de todo lo que pasó, que nadie puede borrar ni editar sin que se note" |
| Servidor MCP, conector Swagger | "Se conecta a Copilot y a Power Automate, que ya usan" |
| Intervalo de Wilson | "Con pocos casos, el resultado está entre X y Y" |
| Seudonimización, tokenización de PII | "La IA nunca ve la cédula ni el correo: ve una etiqueta" |
| Envenenamiento de datos, huella SHA-256 | "Un sello que avisa si alguien cambió los datos" |
| Rate limiting | "Un tope de consultas por minuto para que nadie abuse ni agote el presupuesto" |
| Circuit breaker, cuarentena | "Como la tarjeta que se bloquea al tercer intento con la clave equivocada" |
| Monitoreo de deriva | "Como el chequeo médico: cada medición se compara con la anterior" |

Ojo: no digan "lista para la Superintendencia" ni "cumple la norma X". Digan "deja la evidencia que pediría una
auditoría".
