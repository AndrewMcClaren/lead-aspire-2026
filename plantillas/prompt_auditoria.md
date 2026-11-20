# Prompt de auditoría: un jurado exigente cuando lo necesiten

Úsenlo cada vez que tengan un avance (la propuesta, el guion del pitch, las métricas), en la preparación y el día
del evento. Pídanle a la IA que sea dura: un jurado amable no les sirve.

**Antes de pegarlo:**
- **Datos del cliente:** no peguen información confidencial del cliente en herramientas personales. Usen
  Microsoft 365 Copilot Chat con la cuenta institucional (con la cuenta de trabajo o estudio, Microsoft aplica
  protección de datos empresariales; revisen que aparezca el escudo de protección) o quiten nombres y cifras
  sensibles.
- **No le crean todo:** la IA también inventa. Si dice "los jurados de Microsoft siempre preguntan X", eso es una
  suposición. Usen sus críticas para pensar, no como verdad.

```
Actúa como jurado senior de Microsoft y socio de una firma de consultoría estratégica, evaluando proyectos en
"LEAD ASPIRE Bogotá 2026". Audita de forma estricta, crítica y constructiva el avance de mi equipo. Este evento
NO es un hackatón de código: es una simulación de consultoría de un día. Se valora el impacto de negocio, la
viabilidad, el uso inteligente del ecosistema Microsoft, la experiencia de usuario y la claridad ejecutiva.

Contexto:
- Problema del cliente (con sus palabras): [pegar]
- Lo que descubrimos en la entrevista (datos y números que dio el cliente): [pegar]
- Nuestra solución y cómo funciona: [pegar]
- Herramientas de Microsoft: [por ejemplo Azure OpenAI, Copilot Studio, Power Automate, Power BI]
- Lo que ya funciona en la demo (no lo que planeamos): [pegar]
- Medición de antes y después que tenemos: [pegar la tabla o "todavía no tenemos"]
- Borrador del pitch: [pegar]

Califica del 1 al 10 cada dimensión, con un diagnóstico directo:
1. Dolor real: ¿resolvemos la causa raíz o ponemos un parche? ¿Se integra con lo que el cliente ya tiene o le
   exige cambiar su operación?
2. Valor y ROI: ¿queda claro en menos de 30 segundos si ahorra dinero, reduce riesgos, ahorra tiempo o aumenta
   ingresos? ¿Qué supuesto financiero falta para que un ejecutivo lo crea?
3. Evidencia: ¿cada número del pitch tiene de dónde salió (dato del cliente o medición nuestra)? Señala cada
   cifra que parezca inventada o sin fuente.
4. Realismo técnico y ecosistema Microsoft: para un prototipo de menos de 5 horas, ¿prometemos más de lo que
   mostramos? ¿Las herramientas elegidas son las adecuadas y escalan?
5. Confianza, seguridad y gobernanza: si la IA se equivoca o la engañan, ¿qué pasa? ¿Dónde está el control
   humano? ¿Qué datos personales toca y cómo se protegen?
6. Pitch ejecutivo: escuchándolo en 3 minutos, ¿en qué momento perderías el interés?

Entrega:
- Una tabla con las 6 calificaciones y su diagnóstico.
- Los 3 errores críticos que debemos corregir ya, en orden de importancia.
- Las 3 preguntas más difíciles que nos haría el jurado y la mejor respuesta para cada una.
- Un elevator pitch mejorado de máximo 4 líneas, centrado en el valor de negocio.
- Lo que NO sabes y estás suponiendo, en una lista aparte.
```

Frente al prompt original se agregaron dos dimensiones: **evidencia** (cada número con su fuente) y la lista de
**lo que la IA está suponiendo**. Son las dos críticas que más repitieron los jurados de otros hackatones.
