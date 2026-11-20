# Respaldo: Datatón del DANE (DataJam CENU 2026)

Ganamos la DataJam CENU 2026 del DANE (24 de octubre de 2026, Ruta 2, Bogotá) con un dashboard y un agente de
voz que responde con cifras oficiales: en qué sectores de Bogotá hay señal de subsistencia y en cuáles hay
base para escalar y emprender. Repositorio completo: https://github.com/AndrewMcClaren/DATATON-DANE-2026

## Archivos

| Archivo | Qué es |
|---|---|
| `cifras.csv` | Las 126 cifras verificadas contra la API del Visor del CENU, en el formato del kit (con sinónimos para el modo simulado) |
| `contexto.md` | El contexto del asistente para este caso: resultados preliminares, año de referencia 2023, sin datos por localidad |
| `sugeridas.json` | Las preguntas sugeridas de la página, incluida la pregunta sin dato ("Kennedy") |
| `casos.json` | Casos de medición: 6 preguntas, 3 sin dato y 4 ataques |
| `base_conocimiento_agente_voz.txt` | La base de conocimiento del agente de voz del día |
| `dataton_entrega/` | Lo que se entregó: guion de 4 minutos con las preguntas del jurado, notebook, Excel verificado, prompt del agente y el dashboard oscuro (abre sin internet) |

El dashboard de esta carpeta **no trae el widget del agente de ElevenLabs**: lo quitamos para que el
identificador del agente no quede en un repositorio. El original está en el repositorio de la Datatón.

## Qué aprendimos ese día (y quedó en el kit)

- La primera pantalla respondió la pregunta del reto con números: "Pregunta reto" y al lado "Respuesta".
- Cada cifra se verificó contra la API; el dashboard tenía un verificador.
- El prompt del agente se escribió a mano y tenía una cifra vieja (19,6 % en vez de 36,1 % de ingreso alto en
  el comercio al por mayor). Por eso en el kit el modelo no escribe números: cita claves.
- Una pregunta sin dato ensayada ("¿Cuántos negocios hay en Kennedy?") mostró que el agente decía "no sé".

## Cómo usarla en el kit

```bash
KIT_DATOS=respaldo/dane python -m kit.servidor
```

Resultados preliminares del CENU 2024 (DANE); publicar solo agregados (reserva estadística, Ley 79 de 1993).
