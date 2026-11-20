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
> "Con Azure OpenAI los datos quedan bajo el contrato empresarial de Microsoft con el cliente; según Microsoft, no
> se usan para entrenar los modelos. El piloto se configura en una región que cumpla la política del cliente. Nuestra
> bitácora puede guardar solo huellas, no los textos, y solo enviamos al modelo lo necesario para responder."

Lo que **no** pueden decir: que el kit "enmascara datos sensibles" (no lo hace) ni que hay una región de Azure
OpenAI en Colombia (verifiquen antes). Si el caso tiene datos personales, digan qué datos quitarían del flujo.

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

Ojo: no digan "lista para la Superintendencia" ni "cumple la norma X". Digan "deja la evidencia que pediría una
auditoría".
