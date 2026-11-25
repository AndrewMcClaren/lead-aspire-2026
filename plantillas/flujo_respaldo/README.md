# Flujo de respaldo: solicitudes de despacho con aprobación en Teams

Para cuando el kit no aplica o no hay tiempo de conectarlo: el mismo principio ("lo delicado lo aprueba una persona y
las reglas del negocio deciden qué ni siquiera llega a aprobación") armado solo con Power Automate, en unos 30 minutos.
**Solo conectores estándar** (Microsoft Forms, Aprobaciones, Excel Online, Teams y Outlook): funciona con la licencia de
la universidad, como ya probamos con las aprobaciones.

El caso: alguien de logística pide despachar un lote. **Si va a Europa y no tiene la geolocalización de sus fincas, se
bloquea solo**, sin molestar a nadie (es la regla del reglamento europeo). Si no, le llega la aprobación al área de
Calidad en Teams. Todo queda en un Excel que Power BI puede leer.

```
Formulario (Forms) → ¿Europa sin geolocalización? ── sí → Bloqueado: aviso en Teams + fila en Excel
                                                  └─ no → Aprobación en Teams (Calidad) → fila en Excel + correo al solicitante
```

## 1. El formulario (5 minutos) — forms.office.com

Nuevo formulario: **"Solicitud de despacho de lote"**, con estas preguntas, todas obligatorias:

| Pregunta | Tipo | Opciones |
|---|---|---|
| Lote | Texto | |
| Destino | Opción | Unión Europea · Estados Unidos · Japón · Otro |
| ¿El lote tiene la geolocalización de sus fincas? | Opción | Sí · No |
| Sacos de 60 kg | Texto, con restricción **Número** | |

## 2. El Excel (2 minutos)

Suban `registro_despachos.xlsx` (esta carpeta) a su OneDrive, por ejemplo a `lead-aspire-decisiones`. Ya trae la tabla
**Registro** con las columnas que usa el flujo. Borren la fila de ejemplo cuando quieran.

## 3. El flujo (20 minutos) — make.powerautomate.com

1. **Create** → **Automated cloud flow** → nombre `despacho-lotes` → disparador **When a new response is submitted**
   (Microsoft Forms) → **Create**. En **Form Id**, elijan "Solicitud de despacho de lote".
2. **+** → **Get response details** (Microsoft Forms): mismo formulario; en **Response Id**, el contenido dinámico
   **Response Id**.
3. **+** → **Condition**. Dos filas, unidas con **And**:
    - **Destino** (contenido dinámico) · *is equal to* · `Unión Europea`
    - **¿El lote tiene la geolocalización de sus fincas?** · *is equal to* · `No`
4. **En "True" (bloqueado):**
    1. **Post message in a chat or channel** (Teams): Post as *Flow bot*, Post in *Chat with Flow bot*, Recipient: su
       correo. Mensaje: `Despacho BLOQUEADO: el lote [Lote] va a Europa sin geolocalización. Regla del reglamento
       europeo contra la deforestación. No se pidió aprobación.` (con el contenido dinámico **Lote** donde dice [Lote]).
    2. **Add a row into a table** (Excel Online (Business)): Location *OneDrive for Business*, el archivo
       `registro_despachos.xlsx`, Table *Registro*. Llenen: Fecha = expresión `formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm')`,
       Lote, Destino, Geolocalizacion y Sacos con el contenido dinámico, Solicitante = **Responders' Email**,
       Estado = `Bloqueado`, Decidido por = `Regla automática`, Comentario = `Europa sin geolocalización`.
5. **En "False" (va a aprobación):**
    1. **Start and wait for an approval**: *Aprobar o rechazar: primero en responder*. Title: `Despacho del lote [Lote]
       a [Destino]`. Assigned to: el correo de quien hace de Calidad (que no sea quien llena el formulario).
       Details: `Sacos: [Sacos]. Geolocalización: [¿El lote tiene…?]. Lo pidió: [Responders' Email].`
    2. **Add a row into a table**: igual que arriba, con Estado = expresión
       `if(equals(body('Start_and_wait_for_an_approval')?['outcome'], 'Approve'), 'Aprobado', 'Rechazado')`,
       Decidido por = `first(body('Start_and_wait_for_an_approval')?['responses'])?['responder']?['displayName']` y
       Comentario = `first(body('Start_and_wait_for_an_approval')?['responses'])?['comments']`.
    3. **Send an email (V2)** (Office 365 Outlook) a **Responders' Email**: asunto `Tu solicitud de despacho del lote
       [Lote]`, cuerpo con el Estado.
6. **Save**.

Si una expresión da "action not found", el bloque de aprobación tiene otro nombre: en `body('…')` pongan su nombre con
guiones bajos en vez de espacios.

## 4. Probarlo (3 minutos)

1. Llenen el formulario con **Destino: Unión Europea** y **Geolocalización: No** → en segundos llega el aviso de
   **bloqueado** a Teams, y en el Excel aparece la fila "Bloqueado · Regla automática". Nadie tuvo que aprobar nada.
2. Llénenlo con **Estados Unidos** y **Sí** → a Calidad le llega la aprobación en Teams; al aprobar, el Excel dice
   "Aprobado" con el nombre de quien aprobó y el solicitante recibe un correo.

## Cómo contarlo en el pitch

> "Las reglas del negocio deciden qué ni siquiera llega a aprobación: un lote sin trazabilidad no va a Europa, punto. Lo
> que sí puede ir, lo aprueba Calidad desde Teams, y todo queda registrado. Hoy está armado con Power Automate, sin una
> línea de código; mañana, la misma regla la aplica nuestro asistente con IA sobre sus datos de Snowflake."

Y el Excel `registro_despachos.xlsx` se puede conectar a Power BI (Obtener datos → Excel) para mostrar cuántas solicitudes
se bloquearon por la regla europea.

## Variantes para otros casos

El mismo esqueleto (formulario → regla → aprobación → registro) sirve para casi cualquier proceso:

| Caso | Regla automática (se bloquea sin preguntar) | Quién aprueba |
|---|---|---|
| Pagos a proveedores | La cuenta no es la registrada | Tesorería |
| Compras | El monto supera el saldo del rubro | Jefe del área |
| Ingreso de contratistas a obra | Un documento vencido | Seguridad y salud en el trabajo |
| Publicaciones en redes | Menciona precios o promociones no aprobadas | Mercadeo |
