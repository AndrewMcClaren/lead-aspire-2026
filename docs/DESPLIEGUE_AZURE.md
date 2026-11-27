# Desplegar el kit en Azure: dirección pública fija, base de datos SQL y Teams de ida y vuelta

**Probado de punta a punta el 27 de noviembre de 2026** con la cuenta Azure for Students de Andrés:
https://lead-aspire-kit.azurewebsites.net. Con esto el kit funciona **con el portátil apagado**: WhatsApp, la página,
la base de datos y las aprobaciones de Teams llegan directo a Azure.

```
Caficultor (WhatsApp) ─► Twilio ─► kit en Azure App Service ─► Azure SQL (dbo.EventosAcopio)
                                        │  la IA propone, el código verifica
Exportadora (página, pestaña Acopio) ◄──┤
                                        └─► guardián ─► Power Automate ─► Teams ─► HTTP ─► kit: aprobada
```

## ¿Hace falta desplegar?

| Opción | Cuándo | Riesgo |
|---|---|---|
| **A. Demo local** (`python -m kit.servidor`) + video de respaldo | Siempre como plan B | Depende del portátil |
| **B. Azure App Service** (esta guía) | La demo pública: dirección fija, sin túnel, con base de datos | Región y cuota de la cuenta de estudiante (ver abajo) |
| **C. Túnel** (`cloudflared tunnel --url http://localhost:8000`) | Prueba rápida de WhatsApp desde el portátil | La dirección cambia cada vez; hay que actualizar Twilio |

## Lo que está desplegado

| Recurso | Nombre | Región | Costo |
|---|---|---|---|
| Plan de App Service | `lead-aspire-plan` (B1, Linux) | norwayeast | ≈ USD 13/mes, del crédito de estudiante |
| Aplicación web | `lead-aspire-kit` (Python 3.12, identidad administrada) | norwayeast | incluida en el plan |
| Servidor SQL | `lead-aspire-sql-france` (solo Microsoft Entra ID, sin contraseñas) | francecentral | gratis |
| Base de datos | `acopio` (oferta gratis de Azure SQL, serverless, se pausa sola) | francecentral | gratis |

Todo está en el grupo `lead-aspire`, **el mismo de Azure OpenAI, Content Safety y Speech**.

## Paso a paso (lo que funcionó)

Desde PowerShell, en la carpeta del repositorio. Instalen la CLI de Azure con `winget install Microsoft.AzureCLI`
y abran una terminal nueva.

### 1. Iniciar sesión

```powershell
az login --use-device-code
```

Abran https://login.microsoft.com/device, escriban el código y entren con la cuenta de estudiante.

### 2. Regiones permitidas (lo primero que falla)

La cuenta de estudiante tiene una política que solo deja crear recursos en algunas regiones. Para verlas:

```powershell
az policy assignment list --query "[].parameters.listOfAllowedLocations.value" -o json
```

En la cuenta de Andrés: `norwayeast`, `francecentral`, `northcentralus`, `belgiumcentral`, `denmarkeast`. Además,
cada región tiene cuota distinta: **B1 no tenía cuota en francecentral ni en northcentralus; sí en norwayeast**. Y
**Azure SQL no acepta servidores nuevos en norwayeast**; sí en francecentral.

### 3. Plan y aplicación web

```powershell
az appservice plan create --name lead-aspire-plan --resource-group lead-aspire --location norwayeast --sku B1 --is-linux
az webapp create --name lead-aspire-kit --resource-group lead-aspire --plan lead-aspire-plan --runtime "PYTHON:3.12" --assign-identity "[system]" --https-only true
az webapp config set -g lead-aspire -n lead-aspire-kit --startup-file "python -m kit.servidor --host 0.0.0.0 --puerto 8000 --modelo azure:demo" --always-on true --min-tls-version 1.2 --ftps-state Disabled
```

Usen **B1, no F1**: F1 se duerme a los 20 minutos sin uso y tarda en despertar, y Twilio solo espera 15 segundos.
B1 con `--always-on` responde siempre.

### 4. Base de datos Azure SQL, sin contraseñas

```powershell
az provider register --namespace Microsoft.Sql --wait
$u = az ad signed-in-user show --query "{upn:userPrincipalName, id:id}" -o json | ConvertFrom-Json
az sql server create --name lead-aspire-sql-france --resource-group lead-aspire --location francecentral --enable-ad-only-auth --external-admin-principal-type User --external-admin-name $u.upn --external-admin-sid $u.id
az sql db create -g lead-aspire -s lead-aspire-sql-france -n acopio --edition GeneralPurpose --family Gen5 --capacity 2 --compute-model Serverless --use-free-limit --free-limit-exhaustion-behavior AutoPause --backup-storage-redundancy Local
az sql server firewall-rule create -g lead-aspire -s lead-aspire-sql-france -n AzureServices --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0
```

Si un intento de `az sql server create` falla en una región, el nombre queda "apartado" en esa región: usen otro
nombre para la siguiente.

Para darle permiso a la aplicación (con `winget install Microsoft.Sqlcmd`; si dice que su IP no está permitida,
agréguenla con `az sql server firewall-rule create ... --start-ip-address <IP> --end-ip-address <IP>`, usando la IP
exacta que muestra el error):

```powershell
sqlcmd -S tcp:lead-aspire-sql-france.database.windows.net,1433 -d acopio --authentication-method ActiveDirectoryAzCli -Q "CREATE USER [lead-aspire-kit] FROM EXTERNAL PROVIDER; ALTER ROLE db_datareader ADD MEMBER [lead-aspire-kit]; ALTER ROLE db_datawriter ADD MEMBER [lead-aspire-kit]; ALTER ROLE db_ddladmin ADD MEMBER [lead-aspire-kit];"
```

La tabla `dbo.EventosAcopio` y la vista `dbo.AcopioPorLote` las crea el kit al arrancar (`kit/sqlazure.py`).

### 5. Configuración (las claves nunca van en el repositorio)

Las variables del `.env` pasan a la configuración de la aplicación, **leídas con el lector del kit** (`kit.cargar_env`):
el `.env` tiene comentarios al final de algunas líneas (`KIT_LIMITE_MINUTO=60   # ...`) y, si se copian tal cual, el
servidor no arranca (`ValueError: invalid literal for int()`). No copien `KIT_DECISIONES` (es una carpeta del
portátil) ni las de Snowflake. Agreguen estas:

```
KIT_DATOS=casos/cafe
KIT_URL_PUBLICA=https://lead-aspire-kit.azurewebsites.net
KIT_EVENTOS=/home/datos/eventos_acopio.jsonl
KIT_BITACORA=/home/datos/bitacora.jsonl
AZURE_SQL_SERVER=lead-aspire-sql-france.database.windows.net
AZURE_SQL_DATABASE=acopio
SCM_DO_BUILD_DURING_DEPLOYMENT=true
WEBSITES_PORT=8000
```

`KIT_EVENTOS` y `KIT_BITACORA` van en `/home`, que persiste: la carpeta del código se borra en cada despliegue.

```powershell
az webapp config appsettings set -g lead-aspire -n lead-aspire-kit --settings "@ajustes.json"
```

(`ajustes.json` es una lista `[{"name": "...", "value": "...", "slotSetting": false}, ...]`; bórrenlo después.)

### 6. Subir el código

Un zip con los archivos del repositorio, **sin `.env` ni `resultados/`** (en Git Bash):

```bash
git ls-files -co --exclude-standard | grep -v '^resultados/' | zip -@ ../kit.zip
```

```powershell
az webapp deploy -g lead-aspire -n lead-aspire-kit --src-path ..\kit.zip --type zip
```

Tarda unos 5 minutos (instala `requirements.txt`). Si la página responde 503, lean el error de arranque:

```powershell
az webapp log download -g lead-aspire -n lead-aspire-kit --log-file logs.zip
```

y busquen `Traceback` en `LogFiles/StartupLogs/*_failure.log`. Cuando arranca bien, ese registro dice
`Azure SQL: tabla dbo.EventosAcopio lista en acopio` y `Demo lista`.

### 7. Twilio

Consola de Twilio → Messaging → Try it out → Send a WhatsApp message → **Sandbox settings** → **When a message
comes in**: `https://lead-aspire-kit.azurewebsites.net/api/whatsapp`, POST, **Save**.

**Twilio puede tardar 5 minutos o más en usar la dirección nueva.** Mientras tanto sigue mandando a la anterior: si
era un túnel apagado, en Twilio aparece el error 11200 y el caficultor no recibe respuesta. Esperen y vuelvan a
probar; no cambien nada más.

### 8. Teams de ida y vuelta (Power Automate)

En el portátil, la decisión vuelve por un archivo en OneDrive (`KIT_DECISIONES`). Azure no ve esa carpeta, así que
el flujo `aviso-kit-teams` tiene además una **rama en paralelo** junto a *Create file*, con la acción **HTTP**:

| Campo | Valor |
|---|---|
| Method | `POST` |
| URI | `https://lead-aspire-kit.azurewebsites.net/api/decisiones` |
| Headers | `Content-Type: application/json` y `X-API-Key: <KIT_API_KEY>` |
| Body (expresión **fx**) | la misma de *File Content* de *Create file* |

El kit aplica la decisión con las mismas reglas que la carpeta: token de un solo uso, solo acciones pendientes,
quien pidió no aprueba y todo queda en la bitácora. **La acción HTTP es Premium** (diamante en el ícono): revisen
que el flujo siga funcionando el día del evento. Si deja de funcionar, la acción queda pendiente y se aprueba en la
página.

## Probar en la dirección pública

1. https://lead-aspire-kit.azurewebsites.net → pide la clave (`KIT_API_KEY`) → arriba, todo en verde.
2. Pregunta: "¿Cuántos sacos exportamos el último año?" → 1.250.000, cifra verificada.
3. WhatsApp, **un mensaje por entrega**: `Finca La Loma, 3 arrobas, humedad 11` y luego `Finca Buenavista, 2 cargas`
   → ✅ en el celular y aparecen en la pestaña **Acopio**.
4. Base de datos: portal.azure.com → base `acopio` → **Editor de consultas** (entrar con la cuenta de la
   universidad) → `SELECT * FROM dbo.EventosAcopio` y `SELECT * FROM dbo.AcopioPorLote`. Desde el portátil:
   `python -m kit.sqlazure ver` (con `AZURE_SQL_SERVER` y `AZURE_SQL_DATABASE` en el `.env` y `az login`).
5. Acciones → "Segunda opción: el mismo lote a Estados Unidos" → pendiente → aprobar en Teams → en unos segundos,
   **aprobada · canal Teams**.

Resultado del 27 de noviembre: las dos entregas en `dbo.EventosAcopio` (287,5 kg en L-2026-0412, 37,5 kg aptos para
la UE) y el despacho a Estados Unidos aprobado desde Teams 37 segundos después de proponerlo.

## Conector para Copilot Studio o Power Automate

Importen `kit/conector/swagger.json`, cambien el host por `lead-aspire-kit.azurewebsites.net`, el esquema a `https`
y la autenticación a clave de API con el encabezado `X-API-Key`.

## Después del evento

**No borren el grupo `lead-aspire`**: ahí también están Azure OpenAI, Content Safety y Speech. Borren solo lo de este
despliegue:

```powershell
az webapp delete -g lead-aspire -n lead-aspire-kit
az appservice plan delete -g lead-aspire -n lead-aspire-plan --yes
az sql server delete -g lead-aspire -n lead-aspire-sql-france --yes
```

(El servidor SQL borra también la base `acopio`; exporten antes lo que quieran guardar.) Y devuelvan el webhook del
sandbox de Twilio a donde lo necesiten.

## Cuidados

- Con una dirección pública, **siempre** `KIT_API_KEY`. El servidor avisa si se abre a la red sin clave.
- `KIT_BITACORA_PRIVADA=1` guarda huellas en vez del texto de preguntas, cuentas y peticiones.
- SQL sin contraseñas: la aplicación entra con su identidad administrada y las personas con su cuenta de Entra ID.
  El teléfono del caficultor no llega a la base: solo su huella.
- Las acciones pendientes viven en la memoria del servidor: si la aplicación se reinicia, se vuelven a proponer.
- Los datos del cliente solo en la configuración del servicio o en el `.env`, nunca en GitHub.
