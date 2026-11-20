# LEAD ASPIRE 2026 · Bogotá

Preparación y kit de demo del equipo para el hackatón **Microsoft LEAD ASPIRE**, el 27 de noviembre de 2026
en Microsoft Bogotá. En este formato no hay reto al llegar: se entrevista a un cliente, se escoge un
problema, se construye una solución con IA de Microsoft y se presenta.

## Qué hay aquí

| Carpeta | Para qué |
|---|---|
| [`docs/LEAD_ASPIRE_Bogota.md`](docs/LEAD_ASPIRE_Bogota.md) | Qué se sabe del evento, plan del día, preguntas al cliente, pitch, roles y **plan día por día hasta el 27** |
| [`docs/MICROSOFT_PARA_ESTUDIANTES.md`](docs/MICROSOFT_PARA_ESTUDIANTES.md) | Herramientas de Microsoft con correo institucional, límites, cómo probarlas y **lista de chequeo por integrante** |
| [`plantillas/`](plantillas) | Para el día del evento: entrevista con el cliente, lienzo del problema, pitch, preguntas del jurado y cómo adaptar el kit |
| [`kit/`](kit) | La demo lista para adaptar (abajo) |

## El kit de demo

Un asistente que responde con los datos del cliente, por voz, **sin inventar cifras** y **sin ejecutar solo
lo delicado**:

- **Cifras verificadas.** El modelo no escribe números: cita una clave de `kit/datos/cifras.csv` y el código
  pone el valor. Una cifra escrita a mano o una clave inventada no llega a la persona. Si no tiene el dato,
  dice "No tengo ese dato verificado".
- **Escudo.** Prompt Shields (Azure AI Content Safety) revisa los documentos externos antes de que el
  modelo los lea.
- **Voz.** Azure AI Speech con voz colombiana; sin Azure usa el micrófono y la voz del navegador.
- **Aprobación humana.** Pagos, envíos de datos y montos grandes esperan a que una persona los apruebe.

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

Abran http://localhost:8000 en Chrome o Edge. El modo `simulado` busca por palabras: sirve para ensayar
el recorrido, no es inteligencia real y puede escoger mal una cifra.

### Conectarlo a Azure

1. Creen los recursos siguiendo [`docs/MICROSOFT_PARA_ESTUDIANTES.md`](docs/MICROSOFT_PARA_ESTUDIANTES.md).
2. Copien `.env.ejemplo` a `.env` y llénenlo. El kit lo lee solo; el `.env` nunca se sube porque está en
   `.gitignore`.
3. Prueben:

```bash
python -m kit.verificar --modelo azure:<deployment> --escudo --voz
```

```bash
python -m kit.servidor --modelo azure:<deployment>
```

También funciona con un modelo local: `--modelo ollama:qwen2.5:7b`.

### Pruebas

```bash
python -m pytest -q
```

Corren sin internet. Las de Azure simulan la respuesta del servicio; la prueba real es `kit.verificar`.

## Reglas del equipo

- **Claves solo en `.env`.** Si una clave se sube por error, regenérenla en el portal de Azure de inmediato.
- **Datos del cliente:** este repositorio es privado. Antes de hacerlo público, quiten lo confidencial.
- **Crédito de Azure:** alerta de presupuesto por debajo de USD 100 y borrar los recursos que no se usen.
- Commits pequeños y frecuentes el día del evento, con mensajes claros.

Código escrito con ayuda de IA (Claude) y revisado por el equipo.
