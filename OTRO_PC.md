# Montar el kit en otro computador

Todos los comandos, en orden, para dejar el asistente funcionando en un computador prestado (Windows con Git Bash).
Calculen 20 minutos y háganlo **la noche antes**, no en el evento. Cada bloque es un comando: cópienlo, péguenlo
en Git Bash y esperen a que termine antes del siguiente.

## 0. Qué llevar (en una USB)

| Archivo | De dónde sale | Cuidado |
|---|---|---|
| `lead-aspire-2026.bundle` | El último paquete del repositorio | Lleven también una copia en su OneDrive personal |
| `.env` | La carpeta del repositorio en su computador | Tiene las claves de Azure, Snowflake y Power Automate: **solo en la USB**, nunca por chat ni por correo |

Si en su computador el repositorio tiene cambios recientes, generen un paquete nuevo antes de salir:

```bash
git bundle create /e/lead-aspire-2026.bundle --all
```

(`/e/` es la USB: cambien la letra por la que muestre "Este equipo").

## 1. Instalar Git y Python (una sola vez)

En **PowerShell**:

```bash
winget install Git.Git
```

```bash
winget install Python.Python.3.12
```

Cierren PowerShell y abran **Git Bash** (menú Inicio → Git Bash). Comprueben:

```bash
python --version
```

Debe decir 3.10 o más. Si abre la Microsoft Store, desactiven el alias en Configuración → Aplicaciones →
Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones → `python.exe` (apagado) y reabran Git Bash.

## 2. Traer el repositorio desde la USB

**No lo pongan dentro de OneDrive.** En muchos computadores el Escritorio está en OneDrive
(`~/OneDrive/Desktop`): todo lo que quede ahí, incluido el `.env` con las claves, se sube a la nube de la persona
dueña del computador. Usen una carpeta fuera de OneDrive, por ejemplo `C:\lead`:

```bash
mkdir -p /c/lead && cd /c/lead
```

Si ya lo clonaron en `~/OneDrive/Desktop`, muevan la carpeta a `C:\lead` antes de copiar el `.env` (o, si el `.env`
ya está ahí, bórrenlo también de la papelera de OneDrive en la web y regeneren las claves al terminar).

```bash
git clone /e/lead-aspire-2026.bundle lead-aspire-2026
```

```bash
cd lead-aspire-2026
```

## 3. Instalar las librerías

```bash
python -m pip install -r requirements.txt
```

Solo si van a traer cifras desde Snowflake:

```bash
python -m pip install snowflake-connector-python
```

## 4. Copiar las claves

```bash
cp /e/.env .env
```

Abran el `.env` con el Bloc de notas y revisen `KIT_DECISIONES` (sección 8): apunta a una carpeta de **su**
computador (por ejemplo `C:\Users\<su usuario>\OneDrive\...`), que no existe en el prestado. Déjenla **vacía**
(`KIT_DECISIONES=`) hasta hacer la sección 8. Si la dejan con la ruta vieja, `kit.verificar` lo avisa y el servidor
arranca sin recibir decisiones de Teams.

```bash
notepad .env
```

## 5. Comprobar que todo funciona

```bash
python -m pytest -q
```

Debe decir **92 passed** (o más).

```bash
python -m kit.verificar --modelo azure:demo --escudo --voz
```

Debe decir "Todo lo obligatorio está listo" y probar Azure OpenAI, Prompt Shields y Speech. Si aparece la línea
"Carpeta de decisiones de Teams ... no existe en este computador", corrijan `KIT_DECISIONES` (secciones 4 y 8).

La prueba de seguridad con el modelo real (unos minutos; no manda avisos a Teams):

```bash
KIT_JUEZ=1 python -m seguridad.pentest --modelo azure:demo
```

Debe decir **0 vulnerables**. Si aparece "(error de la prueba)" en algún frente, ese frente no se probó: lean el
detalle en la tabla.

## 6. Datos del día (la mañana del evento)

Si van a usar Snowflake, primero las cifras de la empresa:

```bash
KIT_DATOS=casos/cafe python -m kit.snowflake traer
```

Después, **siempre al final**, los datos oficiales de mercado (TRM de la Superintendencia Financiera y precio del
café de la Federación):

```bash
KIT_DATOS=casos/cafe python -m kit.mercado actualizar
```

Debe decir "3 cifras oficiales ... selladas". Sin internet, el kit sigue con las cifras del día anterior.

## 7. Levantar la demo

```bash
KIT_DATOS=casos/cafe python -m kit.servidor --modelo azure:demo
```

No cierren esa ventana. Abran **http://localhost:8000** en Chrome o Edge. Para apagarlo: Ctrl+C.

Sin claves o sin internet, la misma demo con el modelo simulado (sirve para ensayar, no es IA real):

```bash
KIT_DATOS=casos/cafe python -m kit.servidor
```

Recorrido de la demo (2 minutos):

1. Pregunten: "¿A cuánto cerró el contrato C en la bolsa de Nueva York?" → cifra con fecha y fuente.
2. **Control → Documentos** → adjunten el ejemplo del correo de la cooperativa → cuatro señales de riesgo →
   "Analizar qué pide" → el guardián **bloquea** el pago: la cuenta no es la registrada.
3. Adjunten la instrucción de embarque en PDF → "Analizar qué pide" → "Enviar a aprobación" → llega a Teams.
4. Pregunten algo del PDF ("¿A qué puerto va el lote?") → respuesta con la **cita exacta** comprobada.
5. **Bitácora** → "Verificar": todo quedó encadenado.

## 8. Aprobación en Teams de ida y vuelta

- El **aviso** a Teams funciona en cualquier computador (es la dirección `NOTIFICAR_URL` del `.env`).
- La **respuesta** vuelve por una carpeta de OneDrive. En el computador prestado:
    1. Inicien sesión en OneDrive con su cuenta de la universidad y esperen a que aparezca `lead-aspire/decisiones`.
    2. Entren a esa carpeta en Git Bash y copien su ruta:

       ```bash
       pwd -W
       ```

    3. Pongan esa ruta en `KIT_DECISIONES` dentro del `.env` y reinicien el servidor (Ctrl+C y el comando de la sección 7).
- Si no hay tiempo: aprueben con el botón de la página y muestren en el celular que el aviso llegó a Teams.

## 9. Otros comandos útiles

| Para qué | Comando |
|---|---|
| Medir antes y después con el modelo real (el número del pitch) | `KIT_DATOS=casos/cafe python -m kit.medir --modelo azure:demo` |
| Prueba de seguridad completa | `python -m seguridad.pentest` (con el modelo real: `KIT_JUEZ=1 python -m seguridad.pentest --modelo azure:demo`) |
| Revisar que nadie alteró la bitácora | `python -m kit.bitacora verificar` |
| Revisar que nadie alteró las cifras | `KIT_DATOS=casos/cafe python -m kit.integridad revisar` |
| Volver a sellar después de cambiar cifras a mano | `KIT_DATOS=casos/cafe python -m kit.integridad sellar` |
| Regenerar los datos del tablero de Power BI (con la TRM oficial) | `python -m kit.mercado trm --desde 2025-11-20 --csv plantillas/powerbi/datos/trm_oficial.csv` y luego `python plantillas/powerbi/generar_datos.py` |
| El caso de presupuesto (AI Budget Games) | `KIT_DATOS=casos/presupuesto python -m kit.servidor --modelo azure:demo` |
| Traer cambios nuevos de un paquete actualizado | `git fetch /e/lead-aspire-2026.bundle main` y luego `git merge --ff-only FETCH_HEAD` |

Power BI Desktop es gratis en la Microsoft Store; la plantilla y sus pasos están en `plantillas/powerbi/README.md`.

## 10. Si algo falla

| Lo que ven | Qué hacer |
|---|---|
| `git merge` dice "Your local changes ... would be overwritten" | `git stash` y repitan el merge (sus cambios quedan guardados aparte) |
| `CERTIFICATE_VERIFY_FAILED` al traer la TRM | `python -m pip install -r requirements.txt` (instala `truststore`, que usa los certificados de Windows) |
| `Address already in use` o el puerto 8000 ocupado | Ya hay un servidor abierto en otra ventana: ciérrenlo con Ctrl+C, o usen `--puerto 8001` y abran http://localhost:8001 |
| "Prompt Shields: False" o "voz: False" al arrancar | Falta esa variable en el `.env` o está mal copiada: `python -m kit.verificar --escudo --voz` dice cuál |
| Error 401 o 403 de Azure | La clave del `.env` no corresponde al recurso, o el recurso está en otra región: revisen el portal de Azure |
| `PermissionError: [WinError 5] Acceso denegado: 'C:\\Users\\...'` | `KIT_DECISIONES` apunta a la carpeta del otro computador: déjenla vacía o pongan la ruta de la sección 8 |
| La página no carga los cambios | Ctrl+F5 en el navegador |
| Sin internet en el evento | `KIT_DATOS=casos/cafe python -m kit.servidor` (simulado) y el video de respaldo |

## 11. Al terminar (en el computador prestado)

```bash
rm /c/lead/lead-aspire-2026/.env
```

Después borren la carpeta `C:\lead` desde el Explorador de archivos, cierren su sesión de OneDrive y de
Teams, y si quieren más tranquilidad, regeneren las claves en el portal de Azure (recurso → Claves y punto de
conexión → Regenerar) y actualícenlas en el `.env` de su computador.
