# LEAD ASPIRE Bogotá · 27 de noviembre de 2026

Preparación del equipo para LEAD Aspire Day Colombia 2026 en Microsoft Bogotá, a partir de la descripción
oficial de Bogotá y de lo que se sabe de la edición de Nueva York.

> **Confirmado en el hospitality (24 de noviembre):** el formato es como el de Nueva York. El viernes, las
> empresas invitadas presentan sus necesidades y su contexto, los equipos construyen y le presentan la solución a
> esos mismos clientes. **Las empresas: una de las cafeteras más grandes de Colombia (exportadora o importadora,
> por confirmar), Snowflake y Microsoft.** Por eso vale el **plan A** (caso con construcción). Preparación del caso:
> [`ESCENARIOS.md`](ESCENARIOS.md), sección "El caso confirmado", y el caso del kit `casos/cafe`.

## Qué sabemos y de dónde

**Nueva York (12 de octubre de 2026), fuentes públicas** (página del evento en Luma y dos notas de RIT):

- Equipos de 4 a 6, una postulación por equipo. Más de 1.000 postulaciones y 17 equipos finalistas.
- **No hay reto al llegar.** El equipo conoce al cliente, le hace preguntas, descubre qué problema vale la
  pena resolver y lo resuelve. El flujo que publica Luma es *Discover → Strategize → Build → Pitch*.
- El rol es "especialista de Microsoft Cloud & AI por un día". La solución se construye con "tecnologías de
  IA de Microsoft". No hace falta ser programador, pero sí se espera una solución que funcione.
- El cliente fue **Mastercard**, que pidió pensar cómo generar **confianza del consumidor en el comercio
  agéntico**: compras hechas por agentes de IA.
- Ganó **AlignBuddy** (Los Tigres de RIT): antes de pagar, revisa que la compra que propone el agente
  coincida con las preferencias del cliente según su historial (por ejemplo, marca un itinerario con
  escalas si el cliente siempre vuela directo). Se presentó como complemento de lo que Mastercard ya
  tiene (Agent Pay y Verifiable Intent).
- Lo que el equipo dice que lo hizo destacar: un gerente de producto les dijo que las mejores ideas son
  las que **se implementan fácil o encajan con lo que la empresa ya tiene**.
- No se publicaron los criterios de evaluación ni la duración del pitch.

**Bogotá, descripción oficial (la que compartió el equipo):** "LEAD Aspire Day | Colombia 2026", una
*experiencia estudiantil* para aprender, explorar y prepararse profesionalmente, con cuatro pilares: **Connect**
(red de contactos), **Explore** (ideas y perspectivas), **Compete** ("participa en los **AI Budget Games**,
colabora en equipo, resuelve retos del mundo real y desarrolla soluciones estratégicas") y **Deliver** (presentar
y celebrar). Lo destacado: networking, charlas de liderazgo y carrera, reto AI Budget Games, Innovation Hub,
estrategia de equipo y preparación de pitch, **finales del Case Championship** y premiación. El equipo también
supo de una jornada de 10:00 a 17:00 y un networking previo el 24 de noviembre (sin verificar).

### Nueva York frente a Bogotá

| | Nueva York (12 de octubre) | Bogotá (27 de noviembre) |
|---|---|---|
| Cómo se presenta | Hackatón: "especialista de Microsoft Cloud & AI por un día" | Experiencia estudiantil de liderazgo y preparación profesional |
| Fases | Discover → Strategize → Build → Pitch | Connect → Explore → Compete → Deliver |
| La competencia | Un caso de un cliente (Mastercard) resuelto con IA de Microsoft | "AI Budget Games" y finales de un "Case Championship" |
| ¿Hay que construir? | Sí: se esperaba una solución que funcione | No lo dice: habla de "soluciones estratégicas" |
| Además | — | Networking, charlas de carrera, Innovation Hub, premiación |

**Lo que eso cambia:**

1. **Probablemente hay menos tiempo para construir**, porque la jornada tiene charlas y networking. El peso puede
   estar en la estrategia, el presupuesto y el caso de negocio. El kit deja de ser el protagonista y pasa a ser la
   **prueba de que la estrategia se puede implementar**: 60 segundos de demo o una lámina de respaldo.
2. **El presupuesto pasa al centro:** costos, retorno, priorización y a qué se renuncia. Lo practicamos en
   [`plantillas/budget_games.md`](../plantillas/budget_games.md), junto con la calculadora de ROI.
3. **"Finales" sugiere rondas:** quizás todos presentan corto y solo algunos llegan a la final. Tengan una versión
   del pitch de 2 minutos además de la de 4 o 5.
4. **El networking cuenta (Connect):** cada integrante debe tener una presentación personal de 30 segundos
   (quién soy, qué estudio, qué construí) y su LinkedIn al día.
5. **El caso de presupuesto del kit ya está listo** (`KIT_DATOS=casos/presupuesto`): un asistente que responde
   cuánto se asignó, ejecutó y queda por rubro, con cifras verificadas, y un guardián que bloquea un gasto que
   supere el saldo del rubro, incluso partido en varias solicitudes. Si el reto trata de presupuestos, es la demo.
6. **Lleven el kit desplegado desde antes.** Si hay poco tiempo para construir, no configuren integraciones ese
   día. El plan del 22 y 23 ya incluye desplegarlo en Azure (con una hora de tope; si no sale, demo local).
7. **Nadie sabe aún las reglas.** El 24 pregunten lo de la lista de `budget_games.md`. Si el día del evento resulta
   ser un caso con construcción como el de Nueva York, el resto de esta guía aplica tal cual.

## Experiencia previa del equipo

Antes de este evento ganamos la Datatón del DANE (octubre de 2026) con un dashboard y un agente de voz
sobre cifras oficiales ([DATATON-DANE-2026](https://github.com/AndrewMcClaren/DATATON-DANE-2026)), y
construimos un sistema de controles contra la manipulación de agentes de IA que leen documentos
([guardian-defacc](https://github.com/AndrewMcClaren/guardian-defacc)). Sirve para una lámina de respaldo
si preguntan "¿quiénes son?". No es la solución del 27: el reto se descubre ese día.

## El patrón que llevamos listo

AlignBuddy ganó en Nueva York con una idea que se repite en muchos casos de IA: **el agente propone, y un
control por fuera del agente revisa con datos del cliente antes de que algo pase.** Eso es lo que hace el kit
de este repositorio (`kit/`):

| AlignBuddy (Mastercard) | Kit de este repo | El patrón |
|---|---|---|
| Compra propuesta por el agente | Respuesta o acción propuesta por el asistente | El agente propone |
| Historial y preferencias del cliente | Tabla de cifras verificadas (`kit/datos/cifras.csv`) | Datos del cliente que la IA no puede cambiar |
| "Este vuelo no es como los que usted compra" | "No tengo ese dato verificado" o "este pago espera aprobación" | Verificación en código, explicable |
| Menos devoluciones, más satisfacción | Ninguna cifra inventada; nada delicado sin una persona | Confianza medible |

Un cliente lo entiende en una frase: **"la IA puede equivocarse o ser engañada; lo que llega a la persona
sale de sus propios datos, y lo delicado lo aprueba alguien"**.

### Lo que funciona en un pitch corto

| Qué hacer | Por qué |
|---|---|
| La primera lámina repite el problema del cliente con sus palabras y la respuesta en una frase | El jurado decide en el primer minuto |
| Cada número del pitch dice de dónde salió (datos del cliente o una medición de antes y después) | Un número sin fuente se cuestiona; uno con fuente convence |
| Apenas den los criterios de evaluación, armar el guion con una columna "criterio" | Así ningún criterio queda sin cubrir |
| Preparar las preguntas obvias: costo, privacidad, "¿y si el modelo se equivoca?", cómo se integra | Las respuestas preparadas suenan seguras |
| Demo con plan B: video grabado y versión que corre sin internet | La red del evento falla |
| Mostrar en vivo que la IA dice "no sé" en vez de inventar | Genera más confianza que una respuesta perfecta |

> **Si el caso del cliente no se parece a Nueva York:** `docs/ESCENARIOS.md` dice qué demo armar según el tipo
> de problema, incluidos los casos donde el kit no aplica.

### Lo que es hecho y lo que es deducción

Una IA externa revisó el texto oficial y propuso ajustes. Los aplicamos, pero ojo con lo que presentó como hecho:

| Afirmación | ¿Lo dice el texto oficial? |
|---|---|
| Hay un reto AI Budget Games y unas finales del Case Championship | **Sí** |
| Hay charlas de liderazgo y carrera, Innovation Hub y networking | **Sí** |
| Todos compiten en una ronda y solo los mejores pasan a la final | No: es una deducción razonable por la palabra "finales" |
| El evento busca talento para *prácticas profesionales* | **No.** El texto dice "habilidades **prácticas** de liderazgo y preparación profesional", no habla de pasantías |
| Los jurados evalúan cómo trabajan en equipo | No lo dice. Igual conviene comportarse como si los vieran: escuchar, no atropellar, recibir bien la retroalimentación |
| Habrá 2,5 a 3 horas para construir | No lo dice: es una estimación |
| Hay que construir un prototipo para los Budget Games | No lo dice: habla de "soluciones estratégicas" |

## Plan del día (10:00 a 17:00)

**Plan A, si es un caso con construcción como el de Nueva York.** Si son los Budget Games o un caso sin
construcción, usen el plan B que sigue a esta tabla.

| Hora | Fase | Qué hacer | Entregable |
|---|---|---|---|
| 10:00–11:00 | **Descubrir** | Entrevista al cliente con las preguntas de abajo. Uno pregunta, uno anota, uno escucha números. | Tres problemas candidatos con su costo |
| 11:00–11:45 | **Estrategia** | Escoger UNO. Criterios: duele, se puede medir, encaja con lo que el cliente ya usa, se demuestra en 6 horas. | Una frase de problema y una métrica |
| 11:45–12:00 | Validar | Mostrarle al cliente la frase y la métrica. "¿Si movemos este número, le sirve?" | Visto bueno |
| 12:00–15:30 | **Construir** | Un flujo pequeño que funcione de punta a punta con datos de ejemplo. Nada de plataformas. | Demo que corre |
| 15:30–16:15 | Medir | Escribir 10 a 20 casos del cliente en `casos.json` y correr `python -m kit.medir --modelo azure:<deployment>`. Aunque sea poco, es un número con su intervalo de confianza. | Una tabla de antes y después |
| 16:15–17:00 | **Pitch** | Ensayar dos veces con reloj. | Pitch y demo |

**Plan B, si es estrategia y presupuesto (AI Budget Games):**

| Momento | Qué hacer |
|---|---|
| Al recibir las reglas (5 min) | Leer los criterios en voz alta y anotarlos. Repartir roles: alguien lleva los números (calculadora), alguien la historia y alguien el riesgo |
| Primeros 20 min | El método de 5 pasos de `budget_games.md`: opciones, valor, cartera, renuncias, métrica |
| Siguiente bloque | Pitch con la estructura de siempre: el problema y su costo, la cartera elegida, qué se mide a 30 días, riesgos y control humano, siguiente paso |
| Si hay tiempo y portátil | 60 segundos del kit como prueba de que la opción principal ya funciona (cifras verificadas y aprobación) |
| Antes de presentar | Ensayar la versión de 2 minutos y la de 4 |

### Preguntas para el cliente

1. ¿Qué proceso le cuesta más tiempo o dinero hoy? ¿Cuánto, aproximadamente?
2. ¿Dónde ya usan IA o automatización? ¿Qué les preocupa de dejar que la IA tome decisiones?
3. ¿Qué sistemas tienen hoy (CRM, ERP, Microsoft 365, Dynamics, Power Platform)? *La solución debe encajar ahí.*
4. ¿Cómo sabrían que funcionó? ¿Qué número le mostrarían a su jefe?
5. ¿Qué no puede pasar nunca? (fraude, datos personales expuestos, una decisión sin revisar)
6. ¿Quién usaría la solución el lunes siguiente?

La pregunta 3 sale directo de lo que hizo ganar a AlignBuddy. La 5 abre la puerta a hablar de riesgos y
controles: pocos equipos la van a hacer.

## Cómo armar el pitch

1. **El problema del cliente, en sus palabras y con su número.** "Ustedes nos dijeron que…"
2. **El hueco medido.** Antes de la solución: "de 20 casos, hoy pasan 14". Un número así es lo que más
   recuerda un jurado.
3. **La demo**, un solo flujo y en vivo, o un video de respaldo por si falla la red.
4. **Cómo encaja con lo que ya tienen** (Microsoft 365, Dynamics, Power Platform, sus sistemas).
5. **Riesgos y límites**, dichos por ustedes antes de que se los pregunten: qué no resuelve, qué falta
   para producción, cómo se evita que la IA decida sola lo delicado.
6. **Siguiente paso concreto**: un piloto de dos semanas con un área.

## Roles para un equipo de 4 a 6

| Rol | En la mañana | En la tarde |
|---|---|---|
| Líder del cliente | Dirige la entrevista y valida el problema | Arma y da el pitch |
| Datos | Pide y entiende los datos de ejemplo | Construye la medición de antes y después |
| Construcción (1 o 2) | Escucha qué sistemas existen | Construye la demo |
| Riesgo y seguridad | Pregunta qué no puede pasar | Agrega los controles y la sección de límites |
| Historia (si son 6) | Toma notas textuales del cliente | Hace las láminas y el video de respaldo |

**Reparto sugerido si son 5 (2 + 2 + 1).** Es un consejo, no lo que hizo el equipo ganador: las fuentes no dicen
cómo se repartieron.

| Grupo | Personas | Roles de la tabla de arriba |
|---|---|---|
| Estrategia, negocio y pitch | 2 | Líder del cliente + Riesgo y seguridad (entrevista, ROI, historia, preguntas del jurado) |
| Prototipo | 2 | Construcción (el kit, Copilot Studio o Power Automate según `docs/ESCENARIOS.md`) |
| Datos y diseño | 1 | Datos (datos de prueba realistas, medición de antes y después, láminas limpias) |

Nadie trabaja solo en lo suyo todo el día: a las 12:00 y a las 15:30 los cinco revisan juntos la demo y el pitch.

## Arquitectura que le habla a un jurado de Microsoft

El kit en Python es un riesgo si se muestra como el producto y una ventaja si es el **motor de confianza** detrás
de herramientas de Microsoft:

> **Copilot Studio, Teams o Power Apps** (lo que ve el usuario) → **conector personalizado** → **el kit en Azure**
> (verifica cifras, documentos y acciones) → **Power Automate** (aprobación humana en Teams).

Para eso hace falta que el kit esté en una dirección pública (`docs/DESPLIEGUE_AZURE.md`) y que dos integrantes
practiquen antes: un agente simple en Copilot Studio con un documento, un flujo de aprobación en Teams con Power
Automate y un tablero de tres gráficas en Power BI desde un CSV. Si el caso no necesita el kit, esas tres
habilidades son la demo.

En el pitch, la parte técnica es una sola lámina; el resto, problema, impacto y demo. Traductor de jerga a lenguaje
de negocio: `plantillas/preguntas_jurado.md`.

## Cómo describir la solución en una frase

Sea cual sea el caso, usen este flujo de tres pasos para explicarla (es lo que hacía AlignBuddy y lo que hace el kit):

> **Entrada** (el dato, el documento o la solicitud) → **validación** (la IA propone y el código revisa con los
> datos del cliente) → **acción aprobada** (lo delicado lo confirma una persona).

Y digan que se conecta a lo que el cliente ya tiene, sin reemplazarlo.

## Prompt de auditoría

Para que una IA haga de jurado exigente con cada avance: `plantillas/prompt_auditoria.md`. No peguen datos
confidenciales del cliente en herramientas personales.

## Antes del 27 de noviembre

Las herramientas, cómo activarlas con el correo institucional, sus límites y la lista de chequeo por
integrante están en **[MICROSOFT_PARA_ESTUDIANTES.md](MICROSOFT_PARA_ESTUDIANTES.md)**.

| Día | Qué hacer | Listo cuando |
|---|---|---|
| **Jue 20 y vie 21** | Cada integrante activa Azure for Students, Power Apps Developer Plan y GitHub Student Developer Pack, y revisa Copilot Chat. Pedir Copilot Studio a TI de cada universidad. | La tabla de chequeo por integrante está llena |
| **Sáb 22** | En la cuenta con cuota: Azure OpenAI, Speech F0 y Content Safety F0. Correr `python -m kit.verificar --modelo azure:<deployment> --escudo --voz`. Si Azure OpenAI no despliega, pedir cuota y probar otra región o la cuenta de otro integrante. | Las tres pruebas en OK |
| **Sáb 22 y dom 23 (prototipado)** | Los dos de prototipo practican en Power Platform: agente en Copilot Studio con un documento, aprobación en Teams con Power Automate, tablero de 3 gráficas en Power BI. Probar el despliegue del kit en Azure (`docs/DESPLIEGUE_AZURE.md`); si en una hora no funciona, quedarse con la demo local. | Las tres prácticas hechas y el kit con dirección pública (o descartado) |
| **Dom 23** | Conectar el **kit de demo** (`kit/`) a Azure: modelo, voz y Prompt Shields. Ensayar el recorrido de 60 segundos de `docs/INFRAESTRUCTURA.md`. Correr `python -m kit.medir --modelo azure:<deployment>` para tener la primera tabla con modelo real. Probar el conector en Power Automate o el MCP en VS Code. Practicar `plantillas/adaptar_el_kit.md` con otros datos (por ejemplo `respaldo/dane`). | La demo corre con Azure, hay una tabla de medición y el kit se adapta a otros datos en 30 minutos |
| **Dom 23 (prueba de fuego)** | Alguien que no construyó el kit sigue `RUNBOOK.md` solo, con cronómetro. Lo que no entienda, se corrige en el RUNBOOK. | Lo levanta solo en menos de 20 minutos |
| **Vie 21 a lun 24** | Llenar la tabla de precios de lista verificados de `plantillas/budget_games.md` y hacer la práctica de la cooperativa (20 minutos). Cada integrante prepara su presentación personal de 30 segundos. | Tabla de precios con enlaces y una cartera defendida en 2 minutos |
| **Lun 24** | Networking de LEAD y Microsoft. Hacer las 7 preguntas de `plantillas/budget_games.md` (qué son los AI Budget Games, si se construye, si hay cliente, criterios, duración del pitch). | Las respuestas anotadas, y el plan A o el B elegido |
| **Mar 25** | **Simulacro completo** de 7 horas con un caso de `plantillas/simulacro.md` (o el plan B con la práctica de `budget_games.md` si el 24 confirman que es estrategia y presupuesto). Alguien de afuera hace de cliente con el guion. Cronometrar cada fase. Uno de los ensayos tiene que ser el caso 3, donde el kit no sirve. Repasar `docs/ESCENARIOS.md`. | Pitch grabado en video y la tabla de calificación del simulacro llena |
| **Mié 26** | Corregir lo que falló en el simulacro. Dejar listas las plantillas de láminas, el guion por criterio y el video de respaldo de la demo. Cargar portátiles y probar el micrófono. | Plantillas en una carpeta compartida |
| **Jue 27** | Evento | |

### Qué llevar listo

- [ ] El kit de demo funcionando en dos portátiles, con las claves en variables de entorno.
- [ ] Una versión que corra sin internet (`python -m kit.servidor` en modo simulado, o Ollama) por si falla la red.
- [ ] La demo de respaldo con los datos del DANE (`KIT_DATOS=respaldo/dane`) por si el cliente no da datos a tiempo.
- [ ] La lista de verificación de IA responsable (`plantillas/checklist_ia_responsable.md`) como lámina de respaldo.
- [ ] La calculadora de ROI (`plantillas/calculadora_roi.xlsx`) abierta en un portátil, lista para los números del cliente.
- [ ] `plantillas/budget_games.md` con la tabla de precios de lista llena y verificada.
- [ ] La presentación personal de 30 segundos de cada integrante.
- [ ] La hoja de una página (`plantillas/una_pagina.docx`) lista para llenar hacia las 16:15 y exportar a PDF.
- [ ] `RUNBOOK.md` impreso o en el celular de cada integrante.
- [ ] Plantilla de pitch de 7 láminas (`plantillas/pitch.md`), con la lámina de presupuesto y la versión de 2 minutos.
- [ ] Las preguntas para el cliente impresas o en el celular.
- [ ] La experiencia previa del equipo en una lámina de respaldo, por si preguntan "¿quiénes son?".
- [ ] Cargadores, adaptador HDMI o USB-C y el video de la demo en una memoria.

## Errores comunes que no hay que repetir

- **Problema demasiado grande.** "Mejorar la experiencia del cliente" no se resuelve en 6 horas; "que el
  agente no compre vuelos con escalas a quien siempre vuela directo" sí.
- **Mucha arquitectura y poca evidencia.** Una plataforma enorme sin un solo número de antes y después
  pierde contra un flujo pequeño que funciona y se mide.
- **Lo que dice la presentación no está en la demo.** Si la lámina dice "120 casos", la demo tiene que
  tener 120 casos.
- **No comparar con lo obvio.** "¿Y si solo le escriben mejor el prompt?" Tengan la respuesta lista.
