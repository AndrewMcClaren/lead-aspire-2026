# La ventaja de cada equipo del Defensive Acceleration Hackathon y dónde quedó en el kit

El 14 de noviembre de 2026 compitieron 18 proyectos (AI Safety Colombia × IEEE CS Uniandes). Revisamos el
código de 15 repositorios y los comentarios del jurado. Esta tabla dice qué hacía mejor cada equipo y cómo se
llevó al kit de LEAD ASPIRE. El análisis completo, con cómo funciona cada proyecto por dentro, está en
`guia_18_proyectos.html` (ábranlo en el navegador).

| Equipo | Puesto | Su mejor idea | En el kit | Archivo |
|---|---|---|---|---|
| Defensa por capas en español colombiano | 1.º | Capas en orden de costo; juez LLM con canario y falla cerrada; guardián de acciones (intención, procedencia del destino, monto ≤ lo pedido); estado de la tarea | Escudo en capas; juez con canario; guardián con intención, destino y monto; sesión sospechosa | `kit/escudo.py`, `kit/juez.py`, `kit/aprobacion.py` |
| DEDALUS | 2.º | Señuelos: algo que nadie honesto tocaría delata al atacante, a costo casi cero | Canario en el prompt: si aparece en una respuesta, la IA está revelando sus instrucciones | `kit/asistente.py` |
| Eco | 3.º | Mostrar la fuente y la procedencia en vez de pedir confianza; llegar a los agentes por MCP | Cada cifra con su fuente visible; servidor MCP | `kit/cifras.py`, `kit/mcp.py` |
| Agente Auditor de Confianza Cero | — | Un broker determinista como único camino a las herramientas; mínimo privilegio; registro de auditoría | El guardián es el único camino a las acciones; niveles de autonomía; bitácora | `kit/aprobacion.py`, `kit/bitacora.py` |
| Centinela | — | Reglas en español sin internet; reglas congeladas con un hash; librería instalable | Escudo local en español (firmas v2 del Guardián); huella de las reglas | `kit/firmas.py` |
| TaintWarden | — | Decidir sobre las llamadas a herramientas, no sobre el texto | El guardián decide con la acción y la política, no con lo que diga el modelo | `kit/aprobacion.py` |
| Open Witness | — | Bitácora encadenada por hashes y firmada: se puede probar qué pasó | Bitácora encadenada con HMAC opcional y verificación | `kit/bitacora.py` |
| VanguardIA | — | Sanear en vez de bloquear: retirar solo los trozos con el ataque | Saneado por oraciones: la IA conserva la información legítima | `kit/firmas.py` (`sanear`) |
| Quórum | — | La decisión es una función pura de (solicitud, política); etiquetas de origen que se propagan | `revisar_accion` es una función pura; la sesión se contamina con contenido externo | `kit/aprobacion.py`, `kit/servidor.py` |
| Vigilio Bear | — | Datos maestros, reglas de negocio, segregación de funciones, mapeo a normas | `maestros.json`, aprobador distinto de quien pide, mapa a OWASP, NIST e ISO | `kit/datos/maestros.json`, `docs/INFRAESTRUCTURA.md` |
| Radar | — | El agente solo redacta; un verificador compara con la fuente; reporta el costo real | Verificación de cifras; latencia, tokens y costo por respuesta | `kit/asistente.py` |
| Monitor estable | — | Varias lecturas del monitor para que un cambio menor no voltee el veredicto; significancia estadística | `juzgar(..., lecturas=2)`; intervalos de Wilson en la medición | `kit/juez.py`, `kit/medir.py` |
| HonestSkills | — | Comparar con líneas base triviales; detectar arreglos falsos | Medición contra "sin controles" con el mismo modelo | `kit/medir.py` |
| Patchlayer | — | Propiedades que deben cumplirse siempre, verificadas con muchas entradas | Prueba de invariantes de la política con 500 acciones al azar | `tests/test_infraestructura.py` |
| COLOSSUS | — | Política de autonomía antes de actuar | Nivel de autonomía en la política | `kit/datos/politica.json` |
| RiskShift | — | Separar lo que el agente afirma de la evidencia observada | La cifra la pone el código, no la afirmación del modelo | `kit/asistente.py` |
| AI Guardian | — | Estándar de requisitos sí/no con evidencia | Lista de verificación de IA responsable | `plantillas/checklist_ia_responsable.md` |
| GRIZZLY PIASG | — | Compuertas Go / Go condicionado / No-go | Compuerta al final de la lista de verificación | `plantillas/checklist_ia_responsable.md` |

## Lo que dijo el jurado que faltaba, y cómo lo cubre el kit

| Crítica repetida | Respuesta en el kit |
|---|---|
| "Los ataques los escribió el mismo equipo" | `casos.json` es del cliente; la lista de verificación pregunta si alguien externo escribió ataques |
| "No hay modelo real" | `--modelo azure:<deployment>` u `ollama:<modelo>` en todo: servidor, verificación y medición |
| "¿Le gana a un buen prompt o a un juez LLM?" | `kit.medir` compara con la línea base; el juez está disponible como capa |
| "¿Es significativa la diferencia?" | Intervalos de Wilson en cada métrica |
| "Lo que dice la ficha no está en el repo" | La demo, la medición y la bitácora salen del mismo código |

## Lo que no se llevó, y por qué

- **Detección de voz clonada y C2PA (Eco)**: es otro problema (desinformación); no aplica a un asistente con datos del cliente.
- **Laberinto generativo y autoparches (DEDALUS, COLOSSUS, HonestSkills, Patchlayer)**: son defensa de aplicaciones y código, no de un asistente de negocio. Del enfoque se tomó la idea, no la maquinaria.
- **Separación en enclaves con tokens firmados (Auditor)**: demasiada infraestructura para un día; el guardián cumple el papel de único camino a las acciones.

## Repositorios (públicos al 19 de noviembre de 2026)

Defensa por capas: github.com/Jmpardos1/proyecto_defacc · DEDALUS: github.com/AISAFETY-HACKATON-DEDALO/DEDALUS ·
Eco: github.com/SadidRomero77/eco · Auditor: github.com/CamMV/Defensive-Acceleration · Centinela:
github.com/alinedmooner/centinela · Open Witness: github.com/defacc-hackathon-2026/LasNewjeans-OpenWitness ·
VanguardIA: github.com/AmogusAzul/guardian-contexto · Monitor estable: github.com/EstebanHerna/defacc-dualview ·
RiskShift: github.com/JEstebanBav/riskshift-behavioral-signals · COLOSSUS: github.com/YamidGT/COLOSSUS ·
HonestSkills: github.com/da600vo/DeffAcc · Radar: github.com/mikerb95/hackaton-DefAcc · Patchlayer:
github.com/samuelnor/patchlayer · Quórum: github.com/JhostinAleck/quorum · Vigilio Bear: github.com/santiesc06/defacchack ·
AI Guardian: github.com/DreamHunterG/AI-Guardian-SL5-Defensive-Hackathon. TaintWarden (jonma0107/shield) es privado;
GRIZZLY no publicó código. Fichas y comentarios del jurado: aisafetycolombia.org/defacchackathon.
