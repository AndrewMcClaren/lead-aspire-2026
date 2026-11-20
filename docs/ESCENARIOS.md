# Escenarios probables y cómo atacarlos

En Nueva York el cliente fue Mastercard con un caso de compras hechas por agentes de IA. En Bogotá será una
empresa o aliado colombiano o regional que no conocemos. Este documento prepara al equipo para **cualquier**
caso, incluidos los que no tienen nada que ver con el kit.

## Primero: las cuatro palancas

Todo empresario quiere mover una de estas cuatro cosas. Son las mismas cuatro líneas de las conferencias de
negocio del ecosistema Microsoft (ingresos, productividad, gastos, seguridad). **La solución del 27 tiene que
mover al menos un número de una de ellas, y el pitch tiene que decir cuál.**

| Palanca | Pregunta que se hace el cliente | Número típico |
|---|---|---|
| Ingresos | ¿Vendo más o pierdo menos clientes? | Conversión, ventas, clientes que se van |
| Productividad | ¿Mi gente hace lo mismo en menos tiempo? | Horas por tarea, tiempo de respuesta |
| Gastos | ¿Gasto menos para hacer lo mismo? | Costo por caso, reprocesos, devoluciones |
| Seguridad y confianza | ¿Evito fraudes, errores y multas? | Fraudes evitados, errores, quejas |

## Segundo: qué demo armar según el problema

Después de la entrevista, ubiquen el problema en esta tabla. La columna de la derecha dice qué construir en
las ~3,5 horas de construcción.

| Si el problema es… | Demo | Herramientas | ¿Usa el kit? |
|---|---|---|---|
| Responder preguntas con datos del cliente (cifras, indicadores) | Asistente con cifras verificadas, con voz | Azure OpenAI, Azure AI Speech | **Sí, tal cual** (`plantillas/adaptar_el_kit.md`) |
| Una IA que hace cosas (pagar, enviar, cambiar datos) | Asistente + guardián de acciones + aprobación en Teams | Azure OpenAI, Power Automate | **Sí**: guardián, política y datos maestros |
| Leer documentos largos (manuales, normas, contratos) y responder | Asistente con documentos y citas | Copilot Studio con fuentes de conocimiento, o Azure AI Search + Azure OpenAI | **En parte**: el escudo para documentos externos y la idea de "si no está, no lo digas" |
| Facturas, formularios o documentos que hay que digitar | Extracción automática + revisión de reglas + aprobación | Azure AI Document Intelligence, Power Automate | **En parte**: el guardián y las reglas de datos maestros |
| Procesos manuales con correos y aprobaciones | Flujo automatizado con aprobación | Power Automate, Teams, SharePoint | **En parte**: la política de qué se aprueba solo y qué no |
| Entender qué pasa en el negocio (tendencias, segmentos) | Dashboard con preguntas en lenguaje natural | Power BI, Excel con Copilot | **No**: solo la regla de mostrar la fuente de cada número |
| Crear contenido o atender en redes | Asistente de contenido con revisión humana | Microsoft 365 Copilot, Copilot Studio | **No**: solo la aprobación humana antes de publicar |

## Tercero: los casos probables

Los ocho tipos de cliente más probables en un hackatón en Bogotá. Las cifras y problemas son **típicos del
sector, no de una empresa real**: el día del evento manda lo que diga el cliente.

### 1. Banco, cooperativa o fintech
- **Problemas típicos:** fraude por cambio de cuenta o suplantación, atención al cliente saturada, solicitudes
  de crédito lentas, quejas.
- **Preguntas clave:** ¿Cuántos casos de fraude o reclamos tienen al mes y cuánto cuestan? ¿Qué decisiones
  nunca puede tomar una IA sola? ¿Qué usan hoy para atender (WhatsApp, call center, app)?
- **Palanca:** seguridad (fraude) o productividad (tiempo de atención).
- **Demo:** el kit tal cual. Asistente que responde saldos o condiciones con cifras verificadas y guardián
  que bloquea pagos a cuentas no registradas.
- **Cuidado:** datos financieros personales (habeas data financiero, Ley 1266 de 2008, y datos personales,
  Ley 1581 de 2012). En la demo, solo datos ficticios.

### 2. Retail o comercio electrónico
- **Problemas típicos:** devoluciones, inventario agotado, compras hechas por asistentes de IA que no son lo
  que el cliente quería (el caso de Nueva York), atención en temporada alta.
- **Preguntas clave:** ¿Cuánto les cuestan las devoluciones? ¿Qué porcentaje de ventas es digital? ¿Ya venden
  por WhatsApp o por asistentes?
- **Palanca:** gastos (devoluciones) o ingresos (conversión).
- **Demo:** el kit con los datos del cliente: el caso de ejemplo ya es una cadena de tiendas. Si el problema es
  "el agente compra lo que no es", el guardián revisa cada compra contra las preferencias del cliente antes de
  pagar (agreguen las preferencias como datos maestros).

### 3. Entidad pública o servicio al ciudadano
- **Problemas típicos:** ciudadanos que no encuentran información, trámites con errores, cifras oficiales mal
  citadas.
- **Preguntas clave:** ¿Qué preguntas se repiten más? ¿Qué información es oficial y quién la mantiene? ¿Qué
  pasa si la IA da un dato equivocado?
- **Palanca:** productividad y confianza.
- **Demo:** el kit con cifras oficiales; la demo de respaldo del DANE (`KIT_DATOS=respaldo/dane`) ya está lista.
- **Cuidado:** lenguaje claro, nada de datos por persona y reserva estadística si son datos censales.

### 4. Salud (clínicas, IPS, aseguradoras)
- **Problemas típicos:** pacientes que no llegan a sus citas, filas en atención, autorizaciones lentas.
- **Preguntas clave:** ¿Cuántas citas se pierden al mes y cuánto cuesta cada una? ¿Por qué canal se comunican
  con los pacientes? ¿Qué puede decir un sistema y qué solo un profesional de salud?
- **Palanca:** gastos (citas perdidas) o productividad.
- **Demo:** asistente de agendamiento y recordatorios con aprobación humana para cambios; cifras verificadas
  de disponibilidad. **Nunca** consejos médicos: el asistente remite a un profesional.
- **Cuidado:** datos de salud son sensibles (Ley 1581 de 2012). Solo datos ficticios.

### 5. Logística y transporte
- **Problemas típicos:** clientes preguntando "¿dónde está mi pedido?", rutas, novedades de entrega, facturas de
  transportadores.
- **Preguntas clave:** ¿Cuántas consultas de seguimiento reciben al día? ¿De dónde sale el estado del pedido?
  ¿Qué novedades requieren a una persona?
- **Palanca:** productividad.
- **Demo:** asistente que responde el estado con datos del sistema del cliente (claves verificadas), y flujo de
  Power Automate para novedades que requieren aprobación.

### 6. Manufactura o agroindustria
- **Problemas típicos:** reportes manuales, mantenimiento, calidad, compras a proveedores.
- **Preguntas clave:** ¿Qué reporte les toma más tiempo? ¿Dónde están los datos (Excel, ERP)? ¿Qué decisiones se
  toman con esos datos?
- **Palanca:** productividad o gastos.
- **Demo:** dashboard en Power BI con preguntas en lenguaje natural, o el kit sobre los indicadores de planta.
  Si hay órdenes de compra, el guardián con datos maestros de proveedores.

### 7. Universidad o educación
- **Problemas típicos:** estudiantes con las mismas preguntas (matrículas, pagos, fechas), deserción, carga
  administrativa.
- **Preguntas clave:** ¿Cuáles son las 10 preguntas más repetidas? ¿Dónde está la información oficial? ¿Qué
  trámites necesitan a una persona?
- **Palanca:** productividad.
- **Demo:** asistente con documentos oficiales (reglamento, calendario) en Copilot Studio o con Azure AI Search,
  con citas; escudo para correos externos; "no tengo ese dato" cuando no está.

### 8. Mercadeo, marca o estrategia comercial
- **Problemas típicos:** vender más en redes, entender clientes, crear contenido.
- **Preguntas clave:** ¿Qué canal vende más hoy? ¿Qué datos de clientes tienen? ¿Cómo miden una campaña?
- **Palanca:** ingresos.
- **Demo:** **aquí el kit no es la demo.** Un dashboard en Power BI con segmentos y una propuesta de contenido
  generada con Copilot, con revisión humana antes de publicar y una forma de medir (A/B o antes y después).
- **Lo que sí se lleva:** mostrar la fuente de cada número y que una persona apruebe lo que se publica.

## Cuarto: si nada encaja

1. Vuelvan a la entrevista: ¿qué le cuesta más tiempo o dinero al cliente? Ese es el problema.
2. Escojan la palanca y el número.
3. Armen la demo más pequeña que mueva ese número, aunque sea una hoja de Excel con Copilot o un flujo de
   Power Automate de tres pasos.
4. Usen la lista de IA responsable para responder "¿y si la IA se equivoca?".

Una demo pequeña que funciona y mide un número le gana a una plataforma grande sin evidencia.

## Herramientas de Microsoft mencionadas

Revisen en `docs/MICROSOFT_PARA_ESTUDIANTES.md` cuáles tienen activas con el correo institucional. Algunas
(Copilot Studio, Document Intelligence, Azure AI Search) no están probadas en este repositorio: si el caso las
pide, prueben un ejemplo pequeño antes del evento o elijan la alternativa que ya funciona.
