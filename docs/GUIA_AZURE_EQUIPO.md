# Guía Azure y Foundry para el equipo

25 de noviembre de 2026 · Copia de la guía compartida del equipo

Cada integrante puede montar en unos 45 minutos el mismo Azure que nos funcionó el 24 de noviembre: modelo gpt-4.1-mini, Prompt Shields y voz en español. Si el viernes falla la cuenta de Andrés, basta cambiar seis líneas del archivo .env por las de otra persona y todo sigue igual.

## Antes de empezar

Cada persona lo hace con su propio correo institucional: a cada cuenta Microsoft le da crédito y cuota distintos, así que si una falla, otra puede funcionar.

Qué necesita cada uno:

- Correo institucional activo (el de la universidad).
- Un computador con Python 3.10 o superior y Git (en Windows, Git Bash).
- Acceso al repositorio privado `lead-aspire-2026`: Andrés los invita en GitHub (Settings → Collaborators). Si no les llega la invitación, Andrés les pasa el archivo `lead-aspire-2026.bundle`.
- 45 minutos sin afanes.

**Usen exactamente estos nombres.** Así los comandos son iguales para todos y cambiar de cuenta el viernes es solo cambiar el `.env`:

| Qué | Nombre |
| --- | --- |
| Grupo de recursos | `lead-aspire` |
| Región | France Central (si la cuenta la permite) |
| Recurso de Foundry | `lead-aspire-ia-<su nombre>` |
| Proyecto de Foundry | `lead-aspire-proj` |
| Implementación del modelo | `demo` (siempre este) |
| Content Safety | `lead-aspire-cs-<su nombre>` |
| Speech | `lead-aspire-voz-<su nombre>` |

Hay dos portales distintos y se confunden fácil: **portal.azure.com** (el azul: suscripción, presupuesto, grupos, Content Safety, Speech) y **ai.azure.com** (Foundry: modelos). Cada paso dice en cuál se hace.

## Paso 1: Azure for Students y la alerta de presupuesto (10 minutos)

Azure for Students da 100 USD de crédito, no pide tarjeta y se detiene sola cuando se acaba el crédito.

1. Entren a [azure.microsoft.com/free/students](https://azure.microsoft.com/free/students) y den **Empezar gratis**.
2. Inicien sesión con el **correo institucional** y sigan la verificación de estudiante.
3. Al terminar, en **portal.azure.com** deben ver los 100 USD de crédito.
4. En el inicio del portal, bajo **Navegar**, clic en **Suscripciones** (la llave amarilla) → **Azure for Students**. Debe decir **Estado: Activo**.
5. En el menú izquierdo de la suscripción: **Administración de costos → Presupuestos → + Agregar**.
6. Primera pantalla:
    - Nombre: `alerta-lead`
    - Período de restablecimiento: **Mensual**
    - Las fechas, como vienen
    - Importe: **20**
7. **Siguiente** → Condiciones de alerta:
    - Fila 1: **Coste real**, **80** %
    - Fila 2: **Coste real**, **100** %
    - Grupo de acciones: Ninguno
8. Destinatarios: su correo institucional (y uno personal si quieren). Idioma: **español**.
9. **Crear**.
10. Agreguen **azure-noreply@microsoft.com** a sus contactos para que la alerta no se vaya a spam.

El presupuesto no bloquea nada: solo avisa por correo. Si llega un aviso, revisen qué recurso está gastando.

## Paso 2: regiones permitidas y grupo de recursos (5 minutos)

Las cuentas de estudiante solo dejan crear recursos en unas pocas regiones. En la cuenta de Andrés eran `norwayeast`, `francecentral`, `northcentralus`, `belgiumcentral` y `denmarkeast`; en la suya pueden ser otras.

**Ver las regiones** (portal.azure.com):

1. En la barra de búsqueda de arriba escriban **Directiva** y entren al servicio **Directiva**.
2. En el menú izquierdo, bajo **Creación**, clic en **Tareas**. (Azure en español traduce "Asignaciones" como "Tareas".)
3. Abran **Allowed resource deployment regions**.
4. En la pestaña **Parámetros**, el valor de `listOfAllowedLocations` es la lista. Usen el botón de copiar para verla completa.
5. **No toquen** "Editar asignación" ni "Eliminar asignación": la regla la pone Microsoft para las cuentas de estudiante.

Si `francecentral` está en su lista, úsenla para todo. Si no, escojan una de su lista y úsenla en todos los pasos.

**Crear el grupo de recursos** (la carpeta donde queda todo lo del evento):

1. Busquen **Grupos de recursos** → **+ Crear**.
2. Suscripción: **Azure for Students**. Nombre: `lead-aspire`. Región: **(Europe) France Central**.
3. **Revisar y crear** → **Crear**.

Si ven grupos como `<usuario>-rg` o `DefaultResourceGroup-eastus2`, los creó Azure solo: están vacíos y no cuestan nada.

## Paso 3: Foundry y el modelo gpt-4.1-mini (15 minutos)

**Crear el recurso de Foundry** (portal.azure.com):

1. En el inicio del portal, clic en **Foundry** (ícono morado) → **+ Crear**.
2. Datos básicos:
    - Suscripción: **Azure for Students**
    - Grupo de recursos: `lead-aspire`
    - Nombre: `lead-aspire-ia-<su nombre>` (si dice que ya existe, agréguenle un número)
    - Región: **(Europe) France Central**
3. Más abajo: **Application insights: None** (cobra aparte; no lo necesitamos). Nombre del proyecto: `lead-aspire-proj`.
4. La "Directiva de revisión de contenido" es informativa: Microsoft guarda lo que se envía al modelo para detectar abusos. Por eso nunca se le mandan datos personales reales de un cliente.
5. **Revisar y crear** → **Crear**. Esperen 1 o 2 minutos hasta **"Se completó la implementación"** y den **Ir al recurso**.

**Desplegar el modelo** (ai.azure.com):

1. En la página del recurso, clic en **Ir al portal de Foundry**.
2. Menú izquierdo: **Catálogo** → pestaña **Modelos**. En **Buscar** escriban `mini` y dejen marcado **Disponible en mi proyecto**.
3. Clic en **gpt-4.1-mini** → **Implementar** → **Configuración personalizada**.
4. Configuración:
    - Nombre de la implementación: **`demo`** (borren el que viene)
    - Tipo de implementación: **Estándar global** (se paga solo por uso; la demo gasta centavos)
    - Tokens por minuto: **100.000** (no cuesta más tener el límite alto)
    - Límites de protección: **DefaultV2**
5. **Implementar**.

Qué modelos evitar:

- **gpt-5.4-mini**: en la cuenta de Andrés dio "Cuota insuficiente". Pueden probarlo primero; si sale ese aviso, vuelvan a gpt-4.1-mini.
- **gpt-4o-mini, o3-mini, o4-mini**: dicen "En desuso".
- **realtime, transcribe, codex**: son para audio o código, no para chat.
- **Phi-4**: no dice "Hospedado en Azure".
- Nunca elijan **Provisioned** ni **PTU**: se cobran por hora y se acaban el crédito.

**Probar y copiar las claves:**

1. En la pestaña **Área de juegos** escriban "hola". La primera vez puede salir **ERR_BAD_RESPONSE**: es el despliegue recién creado, esperen 2 a 5 minutos y prueben otra vez.
2. El aviso naranja "No tiene permiso para crear agentes" no nos afecta: el kit llama al modelo directo.
3. Pestaña **Detalles**: copien el **punto de conexión** solo hasta `.com/` (por ejemplo `https://lead-aspire-ia-andres.openai.azure.com/` o `https://lead-aspire-ia-andres.cognitiveservices.azure.com/`) y la **clave**. La clave no se manda a nadie.

## Paso 4: Content Safety y Speech, los dos gratis (10 minutos)

Los dos se crean en **portal.azure.com**, no en Foundry: en Foundry, Content Safety sale "coming soon". Content Safety es el filtro de seguridad de Microsoft (Prompt Shields) y es más importante que Speech. Speech es la voz; sin él, la demo usa la voz del navegador.

**Content Safety:**

1. Busquen **Content Safety** → **+ Crear**.
2. Grupo de recursos `lead-aspire`, región **France Central**, nombre `lead-aspire-cs-<su nombre>`, plan de tarifa **Free F0** (no S0: ese cobra). Si aparece una casilla de IA responsable, márquenla.
3. **Revisar y crear** → **Crear** → **Ir al recurso**.
4. En **Información general**, confirmen que el plan diga **F0**.
5. Menú izquierdo: **Claves y punto de conexión**. Copien el **punto de conexión** completo (empieza por `https://` y termina en `.com/`) y la **CLAVE 1**.

**Speech:**

1. Busquen **Speech** → **Servicios de voz** (o "Speech services") → **+ Crear**.
2. Grupo `lead-aspire`, región **France Central**, nombre `lead-aspire-voz-<su nombre>`, plan **Free F0**.
3. **Crear** → **Ir al recurso** → **Claves y punto de conexión**. Copien la **CLAVE 1**. La región va en minúsculas y sin espacios: `francecentral`.

Cada suscripción solo puede tener un recurso F0 de cada servicio. Si dice que ya tienen uno, usen ese.

## Paso 5: traer el repo y llenar el .env (10 minutos)

En Windows, abran **Git Bash**. Todos los comandos se escriben **dentro de la carpeta del repo**: si sale "not a git repository", es que están en otra carpeta.

**Traer el repo**, con una de estas dos formas:

- Con la invitación de GitHub: `git clone https://github.com/AndrewMcClaren/lead-aspire-2026.git`
- Con el archivo que les pasa Andrés: `git clone lead-aspire-2026.bundle lead-aspire-2026`. Si la ruta tiene espacios, va entre comillas: `git clone "/c/Users/<usuario>/Datos e IA/lead-aspire-2026.bundle" lead-aspire-2026`. Truco: escriban `git clone` y un espacio, arrastren el archivo a la ventana y la ruta se pega sola.

Después:

1. `cd lead-aspire-2026`
2. `pip install -r requirements.txt`
3. `cp .env.ejemplo .env`
4. `notepad .env`

En el Bloc de notas llenen estas líneas, sin espacios alrededor del `=` y sin comillas:

```
AZURE_OPENAI_ENDPOINT=https://lead-aspire-ia-<su nombre>.openai.azure.com/
AZURE_OPENAI_API_KEY=<clave del modelo>
OPENAI_API_VERSION=2024-10-21
CONTENT_SAFETY_ENDPOINT=https://lead-aspire-cs-<su nombre>.cognitiveservices.azure.com/
CONTENT_SAFETY_KEY=<clave 1 de Content Safety>
SPEECH_KEY=<clave 1 de Speech>
SPEECH_REGION=francecentral
SPEECH_VOZ=es-CO-SalomeNeural
```

Guarden (Ctrl + S) y cierren. El `.env` nunca se sube a GitHub: git ya lo ignora.

Para actualizar el repo cuando Andrés mande cambios: con GitHub, `git pull`; con un bundle nuevo, `git fetch ../lead-aspire-2026.bundle main` y después `git merge --ff-only FETCH_HEAD`.

## Paso 6: verificar, medir y abrir la demo (10 minutos)

**1. Verificar todo** (una llamada a cada servicio, centavos):

```
python -m kit.verificar --modelo azure:demo --escudo --voz
```

Deben salir en `[OK]` estas líneas (los `[--]` son opcionales):

- `Pregunta real a azure:demo · La cadena vendió un total de 4.820 millones de pesos…`
- `Pregunta sin dato a azure:demo · No tengo ese dato verificado.`
- `Prompt Shields · ataque por documento: [True, False]`
- `Azure Speech ida y vuelta · oyó: La cadena tiene 38 tiendas.`
- Al final: `Todo lo obligatorio está listo.`

**2. Medir** (unas 60 preguntas, centavos):

```
python -m kit.medir --modelo azure:demo
```

Lo que nos dio el 24 de noviembre: sin controles, 7 de 8 respuestas correctas y 1 de 6 ataques exitosos; con el kit, 8 de 8 y 0 de 6.

**3. Prueba de penetración** (1 o 2 minutos, centavos):

```
pip install pip-audit
python -m seguridad.pentest --modelo azure:demo
```

Lo que nos dio: 118 pruebas, 103 resisten, 0 vulnerables, 15 límites conocidos. Si pip-audit se demora por la red, córranlo aparte con `pip-audit -r requirements.txt -s osv --timeout 60`; debe decir `No known vulnerabilities found`.

**4. Abrir la demo:**

```
python -m kit.servidor --modelo azure:demo
```

Abran http://localhost:8000 en Chrome o Edge y **no cierren la terminal** (si la cierran, la página dice "conexión rechazada"). Arriba deben ver en verde **Modelo: azure-demo**, **Prompt Shields: activo** y **Voz: Azure Speech**.

Recorrido de prueba:

1. "¿Cuánto vendió la cadena el último año?" → 4.820 millones, sello "Cifra verificada", con voz.
2. "¿Cuánto vendió la tienda de Medellín?" → "No tengo ese dato verificado".
3. **Pegar un ejemplo con trampa** y repetir la pregunta 1 → "Documento saneado" o "bloqueado", y la cifra sigue siendo 4.820.
4. **Ejemplo: cuenta cambiada** → **Proponer acción** → bloqueada, con el motivo.

Para el caso del café: `KIT_DATOS=casos/cafe python -m kit.servidor --modelo azure:demo` (en PowerShell: `$env:KIT_DATOS="casos/cafe"` y luego el comando).

## Paso 7 (opcional): aprobaciones en Teams, de ida y vuelta (20 minutos)

Con esto, cada acción que el guardián deja "pendiente" le llega a Tesorería en Teams o por correo, y cuando la aprueban allá, la página del kit cambia sola a **"Aprobada por … · desde Teams"**. Solo usa conectores estándar (sin licencia Premium): el disparador de Teams, Aprobaciones y OneDrive.

Cómo funciona:

1. El kit envía la acción pendiente al flujo, con un **código de un solo uso** (token).
2. El flujo pide la aprobación en Teams o por correo.
3. Al decidir, el flujo guarda un archivo pequeño en una carpeta de OneDrive.
4. OneDrive lo sincroniza al computador y el kit lo aplica, con las mismas reglas de siempre: el token debe coincidir, quien pidió no puede aprobar y todo queda en la bitácora. Un archivo viejo o inventado se aparta en la subcarpeta `rechazadas`.

**A. La carpeta de OneDrive** (en el computador que corre la demo):

1. Abran el Explorador de archivos → **OneDrive - <su universidad>** y creen las carpetas `lead-aspire` y, dentro, `decisiones`.
2. Clic derecho en `decisiones` → **Mantener siempre en este dispositivo**, para que sincronice rápido.
3. Copien la ruta (clic derecho → **Copiar como ruta**). Será algo como `C:\Users\<usuario>\OneDrive - Universidad Santo Tomás\lead-aspire\decisiones`.

**B. El flujo en Power Automate** (make.powerautomate.com):

1. **Create** → **Instant cloud flow** → disparador **When a Teams webhook request is received** → **Create**. En **Who can trigger the flow?**: **Anyone**.
2. **+** → **Start and wait for an approval**: tipo *Aprobar o rechazar: primero en responder*, **Assigned to** el correo de quien aprueba, y en **Title** y **Details** estas expresiones (ícono **fx**):
    - Title: `concat('Acción #', string(triggerBody()?['id']), ': ', triggerBody()?['tipo'], ' a ', triggerBody()?['destino'])`
    - Details: `concat('Monto: ', string(triggerBody()?['monto']), '. Lo pidió: ', triggerBody()?['solicitante'], '. Motivo del guardián: ', triggerBody()?['motivo'])`
3. **+** → busquen **Create file** de **OneDrive for Business**:
    - **Folder Path**: `/lead-aspire/decisiones` (o búsquenla con el ícono de carpeta)
    - **File Name** (fx): `concat('accion-', string(triggerBody()?['id']), '-', utcNow('yyyyMMddHHmmss'), '.json')`
    - **File Content** (fx): `string(addProperty(addProperty(addProperty(addProperty(addProperty(json('{}'), 'id', triggerBody()?['id']), 'token', triggerBody()?['token']), 'resultado', body('Start_and_wait_for_an_approval')?['outcome']), 'aprobador', first(body('Start_and_wait_for_an_approval')?['responses'])?['responder']?['displayName']), 'comentario', coalesce(first(body('Start_and_wait_for_an_approval')?['responses'])?['comments'], '')))`
4. **Save** y copien la **HTTP URL** del disparador. Es secreta: no la compartan.

Si la expresión del contenido da error "action not found", es porque el bloque de aprobación tiene otro nombre: en `body('…')` pongan el nombre del bloque con guiones bajos en vez de espacios.

**C. El kit** (`notepad .env`):

```
NOTIFICAR_URL=<la HTTP URL del disparador>
KIT_DECISIONES=C:\Users\<usuario>\OneDrive - Universidad Santo Tomás\lead-aspire\decisiones
```

Sin comillas. Reinicien `python -m kit.servidor --modelo azure:demo`. Arriba debe salir el chip **Teams · ida y vuelta**.

**Probarlo:** en Acciones, propongan el pago de ejemplo → sale **pendiente** con "Enviada a Teams · esperando la decisión" → aprueben en Teams o en el correo → en 10 a 60 segundos (lo que tarde OneDrive en sincronizar) la tarjeta cambia a **"Aprobada por <nombre> · desde Teams"**, sin recargar. Si en el ensayo tarda más de 15 segundos, el viernes muestren la llegada a Teams y aprueben en la página.

## Problemas que ya nos pasaron

Todos estos salieron el 24 de noviembre y tienen solución conocida.

| Qué aparece | Qué significa | Qué hacer |
| --- | --- | --- |
| `fatal: not a git repository` | Están en otra carpeta | `ls`, luego `cd lead-aspire-2026` |
| "Cuota insuficiente" al desplegar | Esa cuenta no tiene cuota para ese modelo | Usar gpt-4.1-mini, o la cuenta de otro integrante |
| `RequestDisallowedByAzure` | Región no permitida | Revisar la lista del Paso 2 y crear en una región de ella |
| ERR_BAD_RESPONSE en el Área de juegos | Despliegue recién creado | Esperar 2 a 5 minutos |
| "No tiene permiso para crear agentes" | Falta un rol de Foundry que no usamos | Ignorarlo |
| Content Safety dice "coming soon" | Lo buscaron en ai.azure.com | Crearlo en portal.azure.com |
| La configuración predeterminada se ve gris | Está deshabilitada en esa cuenta | Usar **Configuración personalizada** |
| Error de versión de la API | La versión del `.env` no sirve para ese modelo | Cambiar a `OPENAI_API_VERSION=2025-04-01-preview` |
| La página dice "conexión rechazada" | Cerraron la terminal del servidor | Volver a correr `python -m kit.servidor` y dejarla abierta |
| `TimeoutError` en pip-audit | La red no alcanza pypi.org | `pip-audit -r requirements.txt -s osv --timeout 60`, o mirar la pestaña Actions de GitHub |
| `ConnectionAbortedError` en la prueba de penetración | Versión vieja del repo | Actualizar el repo (Paso 5) |
| `Address already in use` | Otro servidor usa el puerto 8000 | `python -m kit.servidor --puerto 8001` y abrir localhost:8001 |
| "Datos: alterada" en la página | Cambiaron un archivo de datos sin sellar | Si fue a propósito: `python -m kit.integridad sellar` |

## Plan B: si la cuenta de Andrés falla el viernes

Como todos usan los mismos nombres, cambiar de cuenta toma 2 minutos y los comandos no cambian.

1. Quien tenga su cuenta lista le pasa a quien maneja la demo sus valores del `.env` **en persona o por un canal privado**, nunca en el chat del grupo ni en capturas.
2. Se reemplazan las líneas de Azure en el `.env` (modelo, Content Safety y Speech).
3. `python -m kit.verificar --modelo azure:demo --escudo --voz` hasta ver `Todo lo obligatorio está listo`.
4. `python -m kit.servidor --modelo azure:demo` y seguir.

Si ninguna cuenta funciona, la demo corre igual sin internet: `python -m kit.servidor` (modo simulado). En el pitch se dice tal cual: "esta es la versión sin conexión; con Azure, el modelo es gpt-4.1-mini y lo medimos así", y se muestra la tabla de la medición.

Quién tiene qué (llénenlo hoy):

| Integrante | Azure for Students | Modelo `demo` | Content Safety | Speech | `kit.verificar` en OK |
| --- | --- | --- | --- | --- | --- |
| Andrés | Sí | Sí (gpt-4.1-mini) | Sí | Sí | Sí |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

## Cuidados y después del evento

- **Las claves no se comparten** en chats de grupo, capturas, correos ni en GitHub. Si una se filtra, en el recurso → **Claves y punto de conexión** → **Regenerar** y actualicen el `.env`.
- **Nunca acepten "Actualizar a pago por uso"**, aunque Azure lo ofrezca: se acaba el crédito de estudiante.
- **Nada de datos personales reales** de un cliente en el modelo. La demo usa datos inventados y el kit cambia cédulas y correos por etiquetas.
- **Solo planes gratis** (F0) para Content Safety y Speech, y **Estándar global** para el modelo. Nada de Provisioned ni PTU.
- **Después del 27**, si ya no lo van a usar: portal.azure.com → **Grupos de recursos** → `lead-aspire` → **Eliminar grupo de recursos**. Borra todo lo del evento de una vez y deja de consumir crédito.

Más detalle en el repo: `RUNBOOK.md` (levantar la demo), `docs/MICROSOFT_PARA_ESTUDIANTES.md` (herramientas y límites) y `docs/SEGURIDAD.md` (prueba de penetración).
