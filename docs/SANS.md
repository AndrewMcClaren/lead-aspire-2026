# Lo que tomamos de SANS y cómo lo usamos

Fuente: un cuaderno de NotebookLM con las charlas de las cumbres de IA de SANS (2024 y 2025), la guía de
controles críticos de seguridad en IA de SANS (versión 1.1, que es un **borrador**) y material de OWASP y NIST.
Este documento dice qué controles de esa guía cubre el kit, cuáles no, y cómo usarlo el 27.

## Antes de citar algo: el cuaderno tiene errores

NotebookLM resume y a veces se equivoca. Errores que se ven en lo que nos dio:

| Dice | Es |
|---|---|
| "OAS AI Exchange", "oasai.org" | **OWASP** AI Exchange (owaspai.org) |
| "Westerm's Topology" | Tipología de culturas organizacionales de **Westrum** |
| "Derailment Errors" (archivos pickle) | Vulnerabilidades de **deserialización** |
| El glosario repite "K-NN" cientos de veces y mezcla un carácter chino | Fallas de generación: ignórenlas |

**Cifras que NO deben ir al pitch sin abrir la fuente original:** "el 75 % de los empleados ya usa IA
generativa", "98 % de precisión" y "31.300 millones de eventos diarios en 18 millones de nodos de Azure" (el caso
SCADE), y "de 7 días a 24 horas" en reentrenamiento. Pueden ser ciertas, pero vienen de un resumen. Si las usan,
digan "según una charla de la cumbre de IA de SANS" y tengan el enlace a la charla. Ante la duda, no las usen:
el jurado valora más los números propios medidos con `kit.medir`.

## La guía de SANS frente al kit, control por control

Estado: **Sí** = lo hace el kit y se muestra en la demo. **Parcial** = lo hace en parte; la columna dice qué
falta. **No aplica** = no tiene sentido para esta demo, y por qué.

| Área de SANS | Control | Estado | Dónde está o qué falta |
|---|---|---|---|
| **Acceso** | Autenticación y control de acceso a la API | Parcial | `KIT_API_KEY`: una clave para toda la API. Sin roles ni usuarios; en producción, Microsoft Entra ID |
| | Mínimo privilegio del agente | Sí | El modelo no ejecuta nada: propone. El código decide y una persona aprueba. Las herramientas MCP son cuatro y ninguna paga ni borra |
| **Datos** | Defender los datos (envenenamiento) | Sí | No entrenamos modelos; protegemos los datos que el asistente usa: `python -m kit.integridad` sella cifras, política y maestros, y avisa si cambian |
| | Evitar mezclar datos sensibles con el contexto | Sí | El modelo ve los **nombres** de las cifras, nunca sus valores: el código los pone al final (`kit/cifras.py`) |
| | Limitar el contenido sensible en los prompts | Sí | Cédulas, correos, teléfonos, cuentas, tarjetas, IP y nombres con "señor/señora" se cambian por marcadores antes de salir del computador (`kit/privacidad.py`) |
| **Despliegue** | Escanear y firmar modelos, cadena de suministro | No aplica | Usamos Azure OpenAI administrado; no descargamos modelos. Dependencias: solo `openai` y `pytest` |
| | Aislar el ejecutor de herramientas (sandbox), nada de `eval` | Sí | El kit nunca ejecuta código ni comandos que escriba el modelo; las herramientas tienen esquemas fijos (Swagger y MCP) |
| **Inferencia** | Guardrails | Sí | Instrucciones, Prompt Shields, juez opcional y, sobre todo, controles en código que no dependen del prompt |
| | Sanear y filtrar la entrada | Sí | Firmas locales, Prompt Shields y juez, con falla cerrada (`kit/escudo.py`) |
| | Sanear y filtrar la salida | Sí | Verificación de cifras, canario y tachado de datos personales que el modelo escriba por su cuenta |
| | Separar las entradas no confiables | Sí | Documentos entre etiquetas `<documento>`; si uno trae trampa, la sesión queda "sospechosa" |
| | Controlar el uso de la API (límite de tasa) | Sí | `KIT_LIMITE_MINUTO` (60 por defecto) y costo por respuesta. Falta: alerta automática de picos |
| **Monitoreo** | Registro del comportamiento, etiquetado | Sí | Bitácora encadenada: cada evento con sus capas, estado y motivos |
| | Correlacionar lo que pide la persona y lo que hace la IA | Sí | La bitácora une petición, acción propuesta, solicitante y aprobador |
| | Detectar anomalías y deriva | Sí | Cada `kit.medir` se compara con la medición anterior del mismo modelo y caso, y avisa si algo empeoró y qué archivos cambiaron. Con `--estricto` falla (para correrlo cada semana o en CI). Falta: correrlo solo, de forma programada |
| **Gobierno** | Inventario del sistema de IA | Parcial | Al arrancar, la bitácora registra modelo, caso, huellas de los datos y capas activas. La ficha completa está en `plantillas/checklist_ia_responsable.md` |
| | Evaluación de riesgos antes de desplegar | Sí | Lista de IA responsable con compuerta Go / No-go |
| | Humano en el ciclo para lo de alto riesgo | Sí | Bandeja de aprobaciones y segregación de funciones |
| | Detener y aislar si se porta mal | Sí | Parada automática: al tercer documento con trampa (`parada_automatica` en `politica.json`) la sesión queda "detenida" y ninguna acción pasa hasta que una persona la revise y la reinicie, con su nombre en la bitácora. Detener el sistema entero sigue siendo manual |
| | Políticas de uso y capacitación | No aplica | Es del cliente. La entrevista pregunta si sus empleados ya usan IA por su cuenta |

**Resumen honesto:** de 20 controles, 16 sí, 2 parciales y 2 que no aplican a esta demo. En el pitch digan "nos
guiamos por la guía de controles críticos de SANS", nunca "cumplimos SANS": la guía es un borrador y no certifica.

## Cómo nos ayuda el 27

1. **Una respuesta preparada para "¿cómo saben que es seguro?"**: la tabla de arriba, como lámina de respaldo.
   Abran con lo que se ve en la demo (cifras verificadas, documento con trampa, aprobación) y después la tabla.
2. **Mejores preguntas al cliente** (los errores más comunes al adoptar IA, según las fuentes):
   - *IA en la sombra:* "¿Sus empleados ya usan ChatGPT u otra IA por su cuenta? ¿Con qué datos?" Si dicen que sí,
     el riesgo ya existe, y la propuesta es darles una alternativa aprobada, no prohibir.
   - *Políticas solo en papel:* "¿Cómo sabrían hoy qué datos se le mandaron a una IA?" Si no pueden saberlo,
     la bitácora es parte del valor.
   - *Agencia excesiva:* "¿Qué decisiones nunca puede tomar una IA sola?" Ya está en la entrevista.
3. **Una frase para el pitch:** "La seguridad no es el departamento del no: es lo que permite usar la IA en
   procesos que hoy no se atreven a tocar." Mueve la palanca de seguridad hacia la de ingresos o productividad.
4. **Un escenario nuevo:** si el cliente es el área de ciberseguridad (SOC), ver el caso 12 de
   [`ESCENARIOS.md`](ESCENARIOS.md).

## Lo que no usamos y por qué

- Robo de modelos, firma de modelos, archivos pickle: no entrenamos ni descargamos modelos.
- Ataques a la infraestructura de AWS (SageMaker, Bedrock): el evento es de Microsoft y la demo corre en Azure.
- Detección de amenazas con clustering y autoencoders: es otro tipo de proyecto; solo sirve si el cliente es un SOC
  con datos de registros.
- Modelos mentales (Cynefin, OODA, DIKW): buenos para entender, poco útiles en un pitch de pocos minutos.
- Privacidad diferencial: sirve para entrenar o publicar estadísticas, no para un asistente con cifras de una tabla.

## Qué agregamos al kit por esto

| Agregado | Comando o variable | Prueba |
|---|---|---|
| Datos personales a marcadores antes de llamar al modelo, y de vuelta en la respuesta | `KIT_PRIVACIDAD=0` lo apaga | `test_datos_personales_…`, `test_asistente_oculta_datos…` |
| Sello de integridad de los datos del caso | `python -m kit.integridad sellar` / `revisar` | `test_integridad_…`, `test_casos_incluidos_estan_sellados` |
| Límite de solicitudes por minuto | `KIT_LIMITE_MINUTO` | `test_limite_de_uso_por_minuto` |
| Inventario al arrancar (modelo, caso, huellas, capas) | evento `inicio` en la bitácora | se ve en `python -m kit.bitacora ver` |
| Parada automática de la sesión al tercer intento de engaño | `parada_automatica` en `politica.json` (0 la apaga) | `test_parada_automatica_…` (3 pruebas) |
| Comparación con la medición anterior | `python -m kit.medir` (`--estricto` falla si empeoró) | `test_comparar_mediciones_…` |
