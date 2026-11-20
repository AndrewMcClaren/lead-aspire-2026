# Desplegar el kit en Azure (para que Copilot Studio o Power Automate lo usen)

**Esto no se ha probado desde este repositorio.** Háganlo el 22 o 23 de noviembre, no el día del evento. Si no
funciona en una hora, quédense con la opción A.

## ¿Hace falta desplegar?

| Opción | Cuándo | Riesgo |
|---|---|---|
| **A. Demo local** (`python -m kit.servidor`) + video de respaldo | Siempre como base. Es lo que ya funciona | Ninguno nuevo |
| **B. Azure App Service** con dirección pública `https` | Si la demo del día pone a Copilot Studio o Power Automate al frente y el kit detrás, como "motor de confianza" | Cuenta, región y cuota de estudiante; servicio gratis con límites |
| **C. Túnel desde el portátil** (Dev Tunnels de Microsoft) | Para una prueba rápida, sin desplegar | La red de invitados del evento puede bloquearlo |

La arquitectura que más le habla a un jurado de Microsoft: **Copilot Studio (o Teams o Power Apps) al frente →
conector personalizado (`kit/conector/swagger.json`) → el kit en Azure, que verifica cifras y acciones → Power
Automate para la aprobación humana.** Para eso hace falta la opción B o C.

## Opción B: Azure App Service

Necesitan Azure for Students activo y la CLI de Azure (desde PowerShell: `winget install Microsoft.AzureCLI`, y
reabrir la terminal).

```bash
az login
```

Desde la carpeta del repositorio. El nombre tiene que ser único en todo Azure (por ejemplo `kit-lead-<iniciales>`),
y la región, una de las permitidas para su cuenta de estudiante:

```bash
az webapp up --name kit-lead-ap --runtime "PYTHON:3.12" --sku F1 --location eastus
```

`F1` es el nivel gratis (con límites de uso diario y arranque lento después de un rato sin uso). El comando crea
el grupo de recursos y sube el código; anoten el grupo de recursos que muestra.

Indiquen cómo arrancar el kit (el puerto 8000 es el que suele esperar App Service en Linux; si no responde,
revisen los registros con `az webapp log tail`):

```bash
az webapp config set --name kit-lead-ap --resource-group GRUPO --startup-file "python -m kit.servidor --host 0.0.0.0 --puerto 8000"
```

Las claves van como configuración de la aplicación, **nunca** en el repositorio. Inventen una clave larga para
`KIT_API_KEY` y guárdenla para el conector:

```bash
az webapp config appsettings set --name kit-lead-ap --resource-group GRUPO --settings KIT_API_KEY=UNA_CLAVE_LARGA KIT_BITACORA_PRIVADA=1 KIT_BITACORA=/home/bitacora.jsonl AZURE_OPENAI_ENDPOINT=... AZURE_OPENAI_API_KEY=... OPENAI_API_VERSION=...
```

Para usar el modelo real en el servidor desplegado, cambien `--startup-file` agregando `--modelo azure:DEPLOYMENT`.

Prueben: `https://kit-lead-ap.azurewebsites.net` debe abrir la página y pedir la clave.

**En el conector** (Power Automate o Copilot Studio): importen `kit/conector/swagger.json`, cambien el host por
`kit-lead-ap.azurewebsites.net`, el esquema a `https` y la autenticación a clave de API con el encabezado
`X-API-Key`.

**Después del evento**, borren todo para no gastar crédito:

```bash
az group delete --name GRUPO
```

## Opción C: túnel desde el portátil

Microsoft tiene Dev Tunnels para exponer un puerto local con una dirección `https`. Revisen su documentación para
los comandos actuales. Con el túnel abierto, definan siempre `KIT_API_KEY` antes de levantar el servidor, porque
cualquiera con la dirección podría usarlo.

## Cuidados

- Con una dirección pública, **siempre** `KIT_API_KEY`. El servidor avisa si se abre a la red sin clave.
- `KIT_BITACORA_PRIVADA=1` guarda huellas en vez del texto de preguntas, cuentas y peticiones.
- El nivel gratis tiene límites; para la demo alcanza, para producción no.
- Los datos del cliente solo en la configuración del servicio o en el `.env`, nunca en GitHub.
