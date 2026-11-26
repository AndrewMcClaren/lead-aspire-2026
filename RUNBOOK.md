# RUNBOOK: poner la demo a funcionar sin ayuda

Una página para que cualquier integrante del equipo levante el kit solo. Si algo falla, busquen el error en la
tabla del final antes de pedir ayuda. Comandos para **Git Bash** en Windows.

**Prueba de fuego (23 de noviembre):** alguien que no construyó el kit hace los pasos 1 a 5 solo, con el
cronómetro corriendo. Debe tardar menos de 20 minutos.

## 1. Traer el repositorio (una sola vez)

```bash
gh auth login
```

```bash
gh repo clone AndrewMcClaren/lead-aspire-2026 && cd lead-aspire-2026
```

(Tienen que haber aceptado la invitación al repositorio que llega al correo.)

## 2. Instalar (una sola vez)

```bash
python --version
```

Si no responde con 3.10 o más, instalen Python desde PowerShell con `winget install Python.Python.3.12` y reabran Git Bash.

```bash
pip install -r requirements.txt
```

## 3. Comprobar

```bash
python -m pytest -q
```

```bash
python -m kit.verificar
```

Debe decir "Todo lo obligatorio está listo". Las líneas `[--]` son opcionales (Azure).

## 4. Levantar la demo

La mañana del evento, traigan los datos oficiales del día (TRM y precio del café). Si no hay internet, el kit sigue con
los del día anterior:

```bash
KIT_DATOS=casos/cafe python -m kit.mercado actualizar
```

```bash
KIT_DATOS=casos/cafe python -m kit.servidor --modelo azure:demo
```

Sin claves de Azure, `python -m kit.servidor` usa el modelo simulado. Para la demo de documentos: en **Control →
Documentos** están los tres ejemplos del caso (instrucción de embarque limpia, lote sin geolocalización a Bélgica con
texto escondido, y correo de una "cooperativa" que cambia la cuenta). También pueden arrastrar cualquier PDF, Word o
correo a la conversación.

```bash
python -m kit.servidor
```

**No cierren esa ventana**: mientras el servidor está prendido, no vuelve el `$`. Abran http://localhost:8000 en
Chrome o Edge. Para apagarlo: Ctrl+C. Si necesitan otros comandos, abran otra ventana de Git Bash.

## 5. Cambiar al caso del cliente (30 minutos)

```bash
cp -r kit/datos casos_cliente
```

Editen en `casos_cliente/`: `cifras.csv` (las cifras del cliente), `contexto.md` (quién es, sin números) y, si hay
acciones, `politica.json` y `maestros.json`. Guía completa: `plantillas/adaptar_el_kit.md`.

Cuando terminen de editar, sellen los datos (si no, la página muestra "Datos: alterada", porque la copia trae el
sello del ejemplo):

```bash
KIT_DATOS=casos_cliente python -m kit.integridad sellar
```

```bash
KIT_DATOS=casos_cliente python -m kit.servidor
```

En PowerShell: `$env:KIT_DATOS="casos_cliente"; python -m kit.integridad sellar` y luego `python -m kit.servidor`.

## 6. Conectar Azure (cuando tengan los recursos)

```bash
cp .env.ejemplo .env
```

Llenen `.env` con las claves del portal de Azure (sin los signos `< >`). El kit lo lee solo. Prueben:

```bash
python -m kit.verificar --modelo azure:NOMBRE_DEL_DEPLOYMENT --escudo --voz
```

## 7. Medir para el pitch

```bash
python -m kit.medir --modelo azure:NOMBRE_DEL_DEPLOYMENT
```

La tabla queda en `resultados/`. Sin Azure, `python -m kit.medir` mide el peor caso simulado.

## Si algo falla

| Lo que ven | Qué hacer |
|---|---|
| `python: command not found` | Instalar Python (paso 2) y reabrir Git Bash |
| `No module named 'openai'` o `'pytest'` | `pip install -r requirements.txt` |
| El navegador dice "rechazó la conexión" | El servidor está apagado: paso 4, y no cerrar esa ventana |
| `Address already in use` | Otro servidor usa el puerto: `python -m kit.servidor --puerto 8001` y abrir http://localhost:8001 |
| La página pide una clave | El servidor tiene `KIT_API_KEY`: pídanla a quien lo levantó |
| `DeploymentNotFound` o 404 con Azure | El nombre después de `azure:` debe ser el del *deployment*, no el del modelo |
| `RequestDisallowedByAzure` | La región no está permitida para su cuenta de estudiante: ver `docs/MICROSOFT_PARA_ESTUDIANTES.md` |
| 429 o "quota" | Sin cuota: esperar un minuto, pedir cuota o usar la cuenta de otro integrante |
| La respuesta siempre es "No tengo ese dato verificado" | Están en modo simulado con una pregunta que no coincide con las palabras del CSV: agreguen `sinonimos` o usen Azure |
| Nada funciona a 30 minutos del pitch | Usen el video de respaldo de la demo y `KIT_DATOS=respaldo/dane` en modo simulado |
