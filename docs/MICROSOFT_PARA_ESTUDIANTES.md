# Herramientas de Microsoft para estudiantes · qué activar ya

Revisado el 20 de noviembre de 2026, para preparar el hackatón Microsoft LEAD ASPIRE en Bogotá
(27 de noviembre) con un correo institucional. Las ofertas para estudiantes cambian seguido: cada fila
trae su fuente, y donde las fuentes no coinciden lo decimos. **Antes de contar con algo, verifíquenlo
con su cuenta**, que es lo que hace la lista de chequeo del final.

## Resumen: qué hacer hoy

1. **Cada integrante** activa Azure for Students con su correo institucional (USD 100, sin tarjeta).
   Si son 5, el equipo tiene USD 500 en créditos.
2. En una de esas cuentas, crear tres recursos y probarlos con `python -m kit.verificar`: Azure OpenAI
   (modelos), Azure AI Speech (voz) y Azure AI Content Safety (Prompt Shields).
3. Revisar que Copilot Chat funciona con la cuenta institucional y pedir a TI de la universidad una
   licencia de Copilot Studio.
4. Activar el Power Apps Developer Plan (Power Apps, Power Automate y Dataverse gratis para practicar).
5. Hacer un simulacro del día completo antes del 27 (ver `LEAD_ASPIRE_Bogota.md`).

> **No activen la prueba gratuita normal de Azure con el correo de la universidad.** Según la
> documentación de preguntas de Microsoft, si la activan, después no pueden activar Azure for Students.

## Las herramientas, una por una

### Lo que casi seguro ya tienen con el correo institucional

| Herramienta | Qué da | Ojo | Para qué la usamos |
|---|---|---|---|
| **Microsoft 365 Copilot Chat** | Chat con IA (GPT-5) sin costo al entrar con la cuenta del colegio o la universidad, si la institución tiene licencias A1, A3 o A5 | Microsoft está activando entre mediados de noviembre y mediados de diciembre de 2026 un modo "Study and Learn" que el administrador puede imponer a estudiantes con licencias Starter Education: si su universidad lo prende, el chat queda limitado a ese agente | Ordenar las notas de la entrevista con el cliente, resumir documentos, primeros borradores del pitch |
| **Word, Excel, PowerPoint y Teams** | Las apps de Microsoft 365 de la institución | Revisen que pueden compartir archivos con personas de otras universidades del equipo | Pitch (PowerPoint), datos de ejemplo (Excel), coordinación (Teams) |
| **Power BI Desktop** | Gratis para Windows | Publicar en el servicio de Power BI o usar Fabric suele estar bloqueado en cuentas institucionales; la prueba de Fabric funciona con un correo personal | Dashboard rápido si el cliente ya usa Power BI |

### Lo que hay que activar

| Herramienta | Qué da | Cómo se activa | Límites que importan |
|---|---|---|---|
| **Azure for Students** | USD 100 de crédito por 12 meses en casi todos los servicios de Azure, sin tarjeta, renovable cada año mientras sean estudiantes | azure.microsoft.com/free/students con el correo institucional | Una cuenta por persona; el crédito no sirve en Azure Marketplace; solo para estudiantes de educación superior |
| **Azure OpenAI en Azure AI Foundry** (dentro de Azure for Students) | Modelos de lenguaje como servicio | Crear un recurso de Foundry y desplegar un modelo | **Ver la sección de abajo: con cuentas de estudiante suele haber poca cuota y regiones restringidas** |
| **Azure AI Speech, nivel gratis (F0)** | Voz a texto: 5 horas al mes. Texto a voz con voces neurales: 500.000 caracteres al mes | Crear un recurso de Speech y escoger el nivel F0 | Voice Live (agente de voz en tiempo real) se cobra por tokens según el modelo; los límites de F0 para Voice Live están en la página de cuotas de Speech |
| **Azure AI Content Safety, nivel gratis (F0)** | Prompt Shields (detecta inyección de instrucciones en lo que escribe el usuario y en documentos), groundedness y material protegido: 5.000 registros de texto al mes | Crear un recurso de Content Safety con nivel F0 | Cada registro son 1.000 caracteres; al llegar al tope el servicio se detiene, no cobra. Máximo 10.000 caracteres por solicitud a Prompt Shields |
| **Power Apps Developer Plan** | Entorno de desarrollo gratis con Power Apps, flujos de nube de Power Automate y Dataverse | Con cualquier correo de trabajo o institucional que use Microsoft Entra ID | Solo para desarrollo y pruebas, no producción; 750 ejecuciones de flujos al mes y 2 GB de base de datos; sin RPA ni dataflows; el entorno se deshabilita si no se usa |
| **GitHub Student Developer Pack** | GitHub Pro gratis y otras herramientas | education.github.com/pack con el correo institucional y comprobante de estudiante | Desde el 12 de marzo de 2026, Copilot para estudiantes pasó a un plan "Copilot Student", con más que Copilot Free pero sin todo lo de Copilot Pro. Un blog dice que las inscripciones se pausaron en abril; no lo confirmamos en GitHub |
| **Microsoft Learn Student Hub** | Applied Skills (evaluaciones prácticas con credencial) sin costo para estudiantes; descuento en exámenes de certificación | learn.microsoft.com, sección de estudiantes | El voucher gratis de examen depende de cada evento o reto; no es automático |

### Lo que depende de la universidad

| Herramienta | Situación |
|---|---|
| **Copilot Studio** (agentes sin código) | No encontramos una oferta gratuita oficial para estudiantes. Algunas universidades la habilitan a pedido de TI; hay reportes no oficiales de una prueba de 60 días. **Pidan hoy a TI de su universidad una licencia o la prueba**: si se habilita, es la forma más rápida de mostrar un agente en un hackatón de Microsoft. |
| **Microsoft Fabric** | Suele estar deshabilitado para cuentas de estudiantes; la prueba funciona con correo personal. |
| **Microsoft 365 Developer Program** (inquilino de prueba con E5) | Un foro lo recomienda para estudiantes, pero en los últimos años Microsoft lo restringió (por ejemplo, a quienes tienen ciertas suscripciones de Visual Studio). Revisen si califican; no cuenten con él. |

### Para después del 27

**Imagine Cup 2027**: desde esta edición es una competencia de startups. Hay una categoría Student
Startup con equipos de hasta 4 estudiantes, pero exige una **empresa constituida desde el 2 de noviembre
de 2024** y tener 18 años o más. Los equipos registrados reciben hasta USD 5.000 en créditos de Azure. La
fecha límite aparece como 8 de enero o 28 de febrero de 2027 según la fuente: confírmenla en
imaginecup.microsoft.com y en las reglas oficiales.

## Azure OpenAI con una cuenta de estudiante: lo que suele fallar

Las respuestas de Microsoft Q&A de estudiantes coinciden en esto (no es documentación oficial, pero se
repite mucho):

- **Cuota baja o en cero.** Se reporta 1.000 tokens por minuto para la mayoría de los modelos y 0 para
  algunos (por ejemplo, la serie o y GPT-4.1). Con cuota 0, el despliegue no funciona.
- **Regiones restringidas.** La suscripción de estudiante solo permite desplegar en unas cinco regiones
  definidas por una política. Si aparece `RequestDisallowedByAzure`, revisen en el portal **Policy →
  Assignments → Allowed resource deployment regions** cuáles les tocaron. Usuarios reportan que East US 2
  y Sweden Central les funcionaron, pero varía.
- **Más cuota**: se pide con un ticket de soporte (tipo "Service and subscription limits (quotas)").
- **Pasar a pago por uso** no da cuota de OpenAI automáticamente y termina el crédito de estudiante.
- Los modelos de Anthropic en Foundry no se pueden desplegar con suscripciones de estudiante, de prueba o
  solo con créditos.

**Por eso hay que probarlo ya, no el 27.** Si el despliegue falla, todavía hay días para pedir cuota,
probar otra región o usar la cuenta de otro integrante.

## Cómo conectar lo que ya tenemos

| Pieza del kit | Sin Azure (funciona hoy) | Con Microsoft | Comando para probar |
|---|---|---|---|
| Modelo (`kit/modelos.py`) | Simulado u Ollama | Azure OpenAI | `python -m kit.verificar --modelo azure:<deployment>` |
| Escudo (`kit/escudo.py`) | Apagado | Prompt Shields | `python -m kit.verificar --escudo` |
| Voz (`kit/voz.py` y la página) | Voz y micrófono del navegador | Azure AI Speech (voz colombiana) | `python -m kit.verificar --voz` |
| Aprobación humana (`kit/aprobacion.py`) | Bandeja en la página | Aviso a Teams con Power Automate (`NOTIFICAR_URL`) | Flujo de prueba en el Developer Plan |
| Dashboard | HTML de un solo archivo | Power BI Desktop si el cliente usa Power BI | — |

Variables de entorno (copien `.env.ejemplo` a `.env` y llénenlo; `.env` está en `.gitignore` y nunca se sube):

```bash
export AZURE_OPENAI_ENDPOINT="https://<recurso>.openai.azure.com/"
export AZURE_OPENAI_API_KEY="..."
export OPENAI_API_VERSION="2024-10-21"
export CONTENT_SAFETY_ENDPOINT="https://<recurso>.cognitiveservices.azure.com"
export CONTENT_SAFETY_KEY="..."
export SPEECH_KEY="..."
export SPEECH_REGION="eastus"   # la región del recurso de Speech
```

La versión de la API de Azure OpenAI cambia; usen la que muestre el portal de Foundry para su despliegue.

### La demo armada con herramientas de Microsoft

Un asistente que responde con datos del cliente, por voz, sin inventar y sin ejecutar solo lo delicado:

1. **Datos verificados** en un CSV (`kit/datos/cifras.csv`, hoy con un caso ficticio de ejemplo).
2. **Azure OpenAI** responde, pero solo puede citar claves de esa tabla; el código pone el número. Así una
   cifra vieja o inventada en un prompt no llega a la persona.
3. **Azure AI Speech** convierte la pregunta hablada en texto y la respuesta en voz.
4. **Prompt Shields** revisa los documentos antes de que el modelo los lea.
5. Si la acción es delicada (un pago, un envío de datos), **Power Automate** pide la aprobación de una
   persona en Teams.

**Esa demo ya está en este repositorio (`kit/`)** y corre hoy sin claves: `python -m kit.servidor`. Cuando
tengan Azure, se conecta cambiando el modelo y llenando el `.env`. El día del evento solo cambian
`kit/datos/cifras.csv` y `kit/datos/contexto.md` (ver `plantillas/adaptar_el_kit.md`).

## Cuidados

- **Crédito finito.** Configuren una alerta de presupuesto en Azure (Cost Management → Budgets) por debajo
  de USD 100 y borren los recursos que no usen.
- **Claves fuera del código.** Usen variables de entorno o los Secretos de Colab. Si una clave se sube por
  error a GitHub, regenérenla en el portal de inmediato.
- **Agentes públicos.** Un agente publicado en una plataforma de voz o de chat lo puede usar cualquiera y
  gasta sus minutos. Restrinjan dominios o despublíquenlo al terminar.
- **Datos.** Usen solo datos públicos o sintéticos. Nada de datos personales
  ni documentos reales de una empresa sin permiso.
- **El día del evento** no sabemos si la organización da cuentas o recursos. Lleven todo funcionando en sus
  propias cuentas y una versión que corra en el portátil (HTML de un solo archivo, Ollama) por si falla la
  red o el inquilino de la universidad bloquea algo.

## Lista de chequeo por integrante

| | Integrante 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Copilot Chat abre con la cuenta institucional | | | | | | |
| Azure for Students activo (USD 100) | | | | | | |
| Alerta de presupuesto creada | | | | | | |
| Power Apps Developer Plan activo | | | | | | |
| GitHub Student Developer Pack aprobado | | | | | | |
| Pidió Copilot Studio a TI de su universidad | | | | | | |

**Una sola cuenta del equipo (la que tenga cuota):**

- [ ] Recurso de Azure AI Foundry creado en una región permitida y un modelo pequeño desplegado.
- [ ] `python -m kit.verificar --modelo azure:<deployment>` en OK (responde la cifra y dice "no sé" con la tienda de Medellín).
- [ ] Recurso de Content Safety F0 y `python -m kit.verificar --escudo` en OK.
- [ ] Recurso de Speech F0 y `python -m kit.verificar --voz` en OK (la transcripción se parece a la frase).
- [ ] `python -m kit.servidor --modelo azure:<deployment>` y una ronda de preguntas en la página, con voz y escudo.

## Fuentes

- Azure for Students: [azure.microsoft.com/free/students](https://azure.microsoft.com/en-us/free/students); prueba gratuita normal y correo universitario: [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5773916/how-to-sing-in-azure-portal-without-credit-card), [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5850498/creating-free-account-in-azure)
- Azure OpenAI con cuentas de estudiante: [Q&A sobre cuota](https://learn.microsoft.com/en-ie/answers/questions/2224916/azure-ai-foundry-quota-insufficient-issues-student), [Q&A sobre Azure for Students](https://learn.microsoft.com/en-us/answers/questions/2183197/azure-openai-with-azure-for-students), [Q&A sobre regiones](https://learn.microsoft.com/answers/a/12822623), [Q&A sobre Claude](https://learn.microsoft.com/en-us/answers/questions/5817540/unable-to-deploy-anthropic-claude-models-in-azure), [cuotas de Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/quotas-limits)
- Azure AI Speech: [precios](https://azure.microsoft.com/en-us/pricing/details/speech/), [cuotas y límites](https://learn.microsoft.com/en-gb/azure/ai-services/speech-service/speech-services-quotas-and-limits)
- Azure AI Content Safety: [precios](https://azure.microsoft.com/en-us/pricing/details/content-safety/), [documentación](https://learn.microsoft.com/azure/ai-services/content-safety/overview)
- Copilot Chat en educación: [Microsoft Education](https://www.microsoft.com/en/education/products/copilot-in-education), [módulo de Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/implement-microsoft-copilot-school-partner-success-series/understand-copilot-options-education), [aviso MC1548047](https://mc.merill.net/message/MC1548047)
- Copilot Studio en universidades (ejemplo de una institución): [Minnesota State Mankato](https://services.mnsu.edu/TDClient/30/Portal/KB/ArticleDet?ID=1176)
- Power Apps Developer Plan: [Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/developer/plan), [crear el entorno](https://learn.microsoft.com/power-platform/developer/create-developer-environment)
- Power BI y Fabric con cuentas de estudiante: [foro de Fabric](https://community.fabric.microsoft.com/t5/Fabric-platform/Fabric-Trial-blocked-on-school-account-any-workaround/td-p/4705962), [foro de Fabric](https://community.fabric.microsoft.com/t5/Developer/Free-ways-for-students-to-try-AI-MCP-Power-BI-development/m-p/5180276)
- GitHub para estudiantes: [anuncio de Copilot Student](https://github.com/orgs/community/discussions/189268), [preguntas frecuentes](https://github.com/orgs/community/discussions/111352)
- Microsoft Learn para estudiantes: [certificaciones y Applied Skills](https://learn.microsoft.com/en-us/training/student-hub/certifications), [Student Ambassadors](https://learn.microsoft.com/training/student-hub/become-a-student-ambassador)
- Imagine Cup 2027: [preguntas frecuentes](https://imaginecup.microsoft.com/Support/faq), [categoría 2027](https://imaginecup.microsoft.com/en-us/category/34), [GeekWire](https://geekwire.com/2026/microsoft-opens-imagine-cup-to-startups-and-the-new-rules-show-how-its-ai-strategy-has-changed/)
