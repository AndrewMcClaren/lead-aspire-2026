# LEAD ASPIRE 2026 · Bogotá

Preparación y kit de demo del equipo para **LEAD Aspire Day Colombia**, el 27 de noviembre de 2026 en
Microsoft Bogotá. En Nueva York fue un caso con cliente y construcción; en Bogotá la competencia se anuncia como
**AI Budget Games** y un **Case Championship**, con reglas aún sin publicar. Preparamos los dos formatos.

## Qué hay aquí

| Carpeta | Para qué |
|---|---|
| [`docs/LEAD_ASPIRE_Bogota.md`](docs/LEAD_ASPIRE_Bogota.md) | Qué se sabe del evento, plan del día, preguntas al cliente, pitch, roles y **plan día por día hasta el 27** |
| [`docs/MICROSOFT_PARA_ESTUDIANTES.md`](docs/MICROSOFT_PARA_ESTUDIANTES.md) | Herramientas de Microsoft con correo institucional, límites, cómo probarlas y **lista de chequeo por integrante** |
| [`RUNBOOK.md`](RUNBOOK.md) | **Una página para levantar la demo sin ayuda** y qué hacer si algo falla |
| [`docs/ESCENARIOS.md`](docs/ESCENARIOS.md) | **Doce tipos de cliente probables** y qué demo armar en cada uno, incluidos los casos donde el kit no aplica |
| [`docs/DESPLIEGUE_AZURE.md`](docs/DESPLIEGUE_AZURE.md) | Cómo poner el kit en Azure con dirección pública para Copilot Studio o Power Automate (no probado) |
| [`docs/SEGURIDAD.md`](docs/SEGURIDAD.md) | **Prueba de penetración** (98 pruebas en 7 frentes), qué se corrigió, cifrado, red y **cumplimiento normativo en Colombia** |
| [`docs/SANS.md`](docs/SANS.md) | La guía de controles críticos de seguridad en IA de SANS **control por control** frente al kit, qué del cuaderno de NotebookLM no citar y cómo usarlo en la entrevista y el pitch |
| [`docs/INFRAESTRUCTURA.md`](docs/INFRAESTRUCTURA.md) | Las capas del kit área por área, cómo mostrarlas en 60 segundos, su relación con OWASP, NIST e ISO, y sus límites |
| [`plantillas/budget_games.md`](plantillas/budget_games.md) | **AI Budget Games**: hipótesis, método de 5 pasos para repartir un presupuesto, costos de una iniciativa de IA, práctica y preguntas para la organización |
| [`plantillas/`](plantillas) | Para el día: entrevista, lienzo del problema, pitch, preguntas del jurado, lista de IA responsable, cómo adaptar el kit, **tres casos de simulacro** y un **prompt de auditoría** para que una IA haga de jurado una **calculadora de ROI** en Excel y una **hoja de una página** para el jurado (Word y ejemplo en PDF) |
| [`kit/`](kit) | La demo lista para adaptar (abajo) |
| [`respaldo/`](respaldo) | Material de referencia: los datos del DANE (demo de respaldo) y el análisis de los 18 proyectos de DefAcc |

## El kit de demo

Un asistente que responde con los datos del cliente, por voz, **sin inventar cifras**, **sin obedecer
instrucciones escondidas** y **sin ejecutar solo lo delicado**. Cada área tiene su capa:

| Área | Qué hace |
|---|---|
| Datos personales | Cédulas, correos, teléfonos, cuentas y tarjetas se cambian por marcadores antes de llamar al modelo; la respuesta vuelve con los datos. El modelo ve el nombre de cada cifra, nunca su valor. |
| Entrada | Firmas locales en español retiran las oraciones con instrucciones para la IA; luego Prompt Shields y, opcional, un juez LLM con canario. Si un servicio falla, el documento no pasa. |
| Salida | El modelo cita claves; el código pone cada cifra con su unidad y su fuente. Cifras escritas a mano (en dígitos o palabras) o claves inventadas: "No tengo ese dato verificado". Un canario detecta si intenta revelar sus instrucciones. |
| Sesión | Al tercer documento con trampa la conversación se detiene: ninguna acción pasa hasta que una persona la revise y la reinicie. |
| Acciones | Política en archivo (`politica.json`) y datos maestros (`maestros.json`): intención, destino registrado, cuenta, monto pedido, saldo disponible por rubro, sesión sospechosa, niveles de autonomía y segregación de funciones. |
| Auditoría | Bitácora encadenada por hashes (con firma HMAC opcional) de cada pregunta, acción y decisión. |
| Integridad | Los datos del caso se sellan con su huella; si alguien cambia una cifra o una cuenta, el servidor y `kit.verificar` avisan. Límite de solicitudes por minuto. |
| Medición | `kit.medir`: antes y después con el mismo modelo, con intervalos de confianza, latencia, tokens y costo. |
| Integración | Azure OpenAI, Prompt Shields, Azure Speech, conector para Power Automate y Copilot Studio, servidor MCP para agentes. |

Detalle de cada capa, cómo probarla y cómo mostrarla: [`docs/INFRAESTRUCTURA.md`](docs/INFRAESTRUCTURA.md).

Los datos de ejemplo son de una **cadena de tiendas ficticia**. El día del evento se cambian por los del
cliente siguiendo [`plantillas/adaptar_el_kit.md`](plantillas/adaptar_el_kit.md).

### Probarlo ya (sin claves ni internet)

Requisitos: Python 3.10 o superior.

```bash
pip install -r requirements.txt
```

```bash
python -m kit.servidor
```

Abran http://localhost:8000 en Chrome o Edge. El modelo `simulado` busca por palabras: sirve para ensayar el
recorrido, no es inteligencia real y puede escoger mal una cifra.

### Comandos

| Comando | Para qué |
|---|---|
| `python -m kit.verificar` | Revisa todo: datos, escudo, guardián, bitácora y variables de Azure |
| `python -m kit.verificar --modelo azure:<deployment> --escudo --voz` | Prueba los servicios reales de Azure (una llamada cada uno) |
| `python -m kit.servidor --modelo azure:<deployment>` | La demo con el modelo real |
| `python -m kit.medir` | Antes y después en el peor caso simulado (un modelo que obedece todo) |
| `python -m kit.medir --modelo azure:<deployment>` | Antes y después con el modelo real: el número del pitch. Se compara solo con la medición anterior y avisa si algo empeoró |
| `python -m kit.bitacora verificar` | Comprueba que nadie alteró la bitácora |
| `python -m seguridad.pentest` | Intenta romper el kit por todos los frentes (`--modelo azure:demo` agrega ataques contra el modelo real) |
| `python -m kit.integridad sellar` | Sella los datos del caso después de cargarlos (`revisar` dice si cambiaron) |
| `python -m kit.mcp` | Servidor MCP para agentes (ver abajo) |
| `KIT_DATOS=respaldo/dane python -m kit.servidor` | La demo con otro caso, sin tocar el código |
| `KIT_DATOS=casos/cafe python -m kit.servidor` | **El caso de café** (exportadora ficticia): exportaciones, calidad, trazabilidad para Europa y pagos a cooperativas |
| `KIT_DATOS=casos/presupuesto python -m kit.servidor` | El caso de presupuesto por rubros: el guardián bloquea gastos por encima del saldo (para los AI Budget Games) |
| `python -m pytest -q` | Las pruebas (sin internet; las de Azure simulan el servicio) |

### Conectarlo a Azure

1. Creen los recursos siguiendo [`docs/MICROSOFT_PARA_ESTUDIANTES.md`](docs/MICROSOFT_PARA_ESTUDIANTES.md).
2. Copien `.env.ejemplo` a `.env` y llénenlo. El kit lo lee solo; el `.env` nunca se sube porque está en
   `.gitignore`.
3. `python -m kit.verificar --modelo azure:<deployment> --escudo --voz`

También funciona con un modelo local: `--modelo ollama:qwen2.5:7b`.

### Conectarlo a lo que ya usa el cliente

- **Power Automate o Copilot Studio**: creen un conector personalizado importando `kit/conector/swagger.json`
  (o `http://localhost:8000/swagger.json` con el servidor corriendo). Necesita una dirección pública: expongan
  el puerto 8000 con un túnel, por ejemplo Dev Tunnels de Microsoft, y pongan esa dirección como host.
- **GitHub Copilot en VS Code (modo agente)**: agreguen el servidor MCP en `.vscode/mcp.json`:
  `{"servers": {"asistente-verificado": {"type": "stdio", "command": "python", "args": ["-m", "kit.mcp"]}}}`.
  El agente tendrá las herramientas `buscar_cifras`, `obtener_cifra`, `revisar_documento` y `proponer_accion`.
- **Avisos en Teams**: con `NOTIFICAR_URL` cada acción pendiente se envía como JSON a esa dirección (por
  ejemplo, el disparador HTTP de un flujo de Power Automate que publica en Teams).

**Probado con Azure real (24 de noviembre de 2026):** Azure OpenAI (gpt-4.1-mini), Prompt Shields y Azure Speech,
con `kit.verificar` y una primera medición (`docs/INFRAESTRUCTURA.md`, sección Límites). **Sin probar todavía:** el
aviso a Power Automate, el conector en Copilot Studio y el despliegue en App Service.

## Reglas del equipo

- **Claves solo en `.env`.** Si una clave se sube por error, regenérenla en el portal de Azure de inmediato.
- **Datos del cliente:** este repositorio es privado. Antes de hacerlo público, quiten lo confidencial.
- **Crédito de Azure:** alerta de presupuesto por debajo de USD 100 y borrar los recursos que no se usen.
- Commits pequeños y frecuentes el día del evento, con mensajes claros.

Código escrito con ayuda de IA (Claude) y revisado por el equipo.
