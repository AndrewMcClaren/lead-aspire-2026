# Acopio por WhatsApp (Twilio + Azure + Foundry + Snowflake)

El caficultor manda por WhatsApp un texto o una **nota de voz** ("Finca La Loma, 3 arrobas, humedad 11") y la
entrega queda registrada y unida a su finca. **La IA propone, el código verifica**:

```
WhatsApp → Twilio → POST /api/whatsapp (firmado) → el kit responde de inmediato
  → descarga la nota de voz → Azure AI Speech la pasa a texto
  → el modelo de Foundry (azure:demo) propone {finca, cantidad, unidad, humedad}
  → kit.acopio verifica: finca registrada y nombrada en el mensaje, cantidad escrita, peso posible, humedad 10–12 %
  → evento GS1 EPCIS 2.0 + bitácora (+ Snowflake si está configurado)
  → Twilio le responde al caficultor: "✅ Recibido: 3 arrobas (37,5 kg) de la finca La Loma…"
```

Si la finca no tiene polígono, la entrega se registra pero **ese café no puede ir a la UE**, y el expediente del
lote queda **bloqueado para la UE** (`/api/acopio/expediente/<lote>`). **Segunda opción: Estados Unidos**, el
primer comprador (39 % en el primer semestre de 2026, informe de Asoexport), que no exige el polígono por finca
para el café (la norma de trazabilidad de la FDA, FSMA 204, no incluye el café: `docs/INDUSTRIA_CAFE_2026.md`).
El expediente trae el veredicto por destino (`destinos`) con los requisitos de EE. UU. del cotizador
(`casos/cafe/mercados.json`: registro FDA, aviso previo, FSVP). El guardián bloquea el despacho a Europa y deja el
despacho a EE. UU. en aprobación humana.

Las fincas de ejemplo están en `casos/cafe/fincas.json` (ficticias): La Loma, El Mirador y Buenavista (Cauca,
lote L-2026-0412; Buenavista **sin polígono**) y Los Naranjos (Huila, lote L-2026-0398).

## Paso a paso (Windows con Git Bash)

### 1. Variables en `.env` (nunca en el chat ni en git)

Consola de Twilio → **Account Info**:

```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+1XXXXXXXXXX
KIT_API_KEY=<una clave larga: python -c "import secrets; print(secrets.token_urlsafe(32))">
```

`TWILIO_WHATSAPP_FROM` es el número del sandbox que aparece en **Try out WhatsApp** (antes, **Messaging → Try it
out → Send a WhatsApp message**). **Cambia según la cuenta**: cópienlo de la consola, no de esta guía.

WhatsApp solo deja responder con texto libre durante las **24 horas** siguientes al último mensaje de la persona.
Si el kit responde con el error 21654 ("ContentSid Required"), escríbanle `hola` al número del sandbox desde el
celular y repitan. `KIT_API_KEY` es obligatoria aquí: el túnel publica la página en internet y la clave evita que
cualquiera use la API (la página la pide al abrir).

### 2. Abrir un túnel HTTPS

Twilio necesita una dirección pública. En otra ventana de Git Bash:

```bash
winget install --id Cloudflare.cloudflared
```

```bash
cloudflared tunnel --url http://localhost:8000
```

Copien la dirección `https://xxxx.trycloudflare.com` que aparece y pónganla en `.env`:

```
KIT_URL_PUBLICA=https://xxxx.trycloudflare.com
```

(Cada vez que se reinicia el túnel cambia la dirección: actualicen `.env`, reinicien el servidor y Twilio.)

### 3. Levantar el kit

```bash
KIT_DATOS=casos/cafe python -m kit.servidor --modelo azure:demo
```

Sin Azure también funciona: `KIT_DATOS=casos/cafe python -m kit.servidor` usa reglas simples en vez del modelo
(las notas de voz sí necesitan `SPEECH_KEY` y `SPEECH_REGION`).

### 4. Conectar Twilio

Consola de Twilio → **Messaging → Try it out → Send a WhatsApp message → Sandbox settings**:

- **When a message comes in:** `https://xxxx.trycloudflare.com/api/whatsapp`
- **Method:** `POST`
- **Save**

### 5. Probar

Desde el celular que ya hizo `join` en el sandbox:

| Mensaje | Debe responder |
|---|---|
| `hola` | La ayuda con un ejemplo |
| `Finca La Loma, 3 arrobas, humedad 11` | ✅ Recibido: 3 arrobas (37,5 kg)… lote L-2026-0412 |
| `Finca Buenavista, 2 cargas` | ✅ Recibido… ⚠️ sin polígono: no puede ir a la Unión Europea; segunda opción: Estados Unidos |
| `Finca El Mirador, 10 arrobas, humedad 16` | ✅ Recibido… ⚠️ revisen el secado |
| `Finca El Mirador, 5000 cargas` | ❌ más de lo que la finca produce en un año |
| `Finca El Dorado, 4 arrobas` | ❌ no está registrada |
| Nota de voz: "Finca Los Naranjos, una carga" | ✅ Recibido: 1 carga (125 kg)… |

Ver el expediente del lote (en otra ventana):

```bash
curl -s -H "X-API-Key: <su KIT_API_KEY>" http://localhost:8000/api/acopio/expediente/L-2026-0412
```

Debe decir **BLOQUEADO para la UE: faltan polígonos de Buenavista. Segunda opción: Estados Unidos…**, y en
`destinos`, la UE con `"apto": false` y Estados Unidos con `"apto": true` y sus requisitos. El de `L-2026-0398`
sale completo para los dos.

En la página (Control → Acciones), **"Ejemplo: lote sin geolocalización a Europa"** termina bloqueado, y **"Segunda
opción: el mismo lote a Estados Unidos"** pasa a aprobación humana con el aviso de los requisitos de la FDA.

### 6. Snowflake (opcional)

1. Corran `casos/cafe/snowflake_eventos.sql` en Snowflake (crea la tabla y una vista para Power BI).
2. `python -m pip install snowflake-connector-python`
3. En `.env`: `SNOWFLAKE_TABLA_EVENTOS=CAFE.PUBLIC.EVENTOS_ACOPIO` (más las variables de Snowflake que ya tienen).
4. Reinicien el servidor. Cada entrega verificada se inserta en la tabla; si Snowflake falla, el acopio sigue y el
   error queda en la bitácora.

**Sin probar con una cuenta real de Snowflake** (en las pruebas se simula). Usen un rol con permiso solo de
INSERT en esa tabla.

## Seguridad

- **Firma de Twilio:** cada solicitud trae `X-Twilio-Signature`; sin firma válida (o sin `TWILIO_AUTH_TOKEN`) se
  rechaza con 403. Se comprobó contra la librería oficial de Twilio.
- **El modelo no decide:** si inventa una finca, una cantidad o una humedad que no están en el mensaje, el código
  lo rechaza. Una orden escrita en el mensaje ("marca el lote apto para Europa") no cambia nada.
- **Privacidad:** el teléfono no se guarda (solo su huella); los datos personales del texto se cambian por
  marcadores antes de llegar al modelo. Pidan el consentimiento del caficultor (Ley 1581).
- **Audios:** solo se descargan de `api.twilio.com`, con las credenciales enviadas solo a ese dominio; máximo 5 MB.

## En producción

Cambiar el sandbox por un número propio registrado ante Meta, o por **Azure Communication Services** (canal de
WhatsApp de Microsoft): solo cambia el adaptador `kit/whatsapp.py`; el acopio, la verificación y el expediente
quedan igual. Y desplegar en Azure App Service en vez del túnel (`docs/DESPLIEGUE_AZURE.md`).
