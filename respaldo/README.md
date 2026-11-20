# Respaldo

Material de referencia del equipo. **No es parte del kit**: el kit funciona sin esta carpeta.

| Carpeta | Qué hay | Para qué sirve el 27 |
|---|---|---|
| [`dane/`](dane) | Las 126 cifras verificadas del CENU 2024 (DANE) para Bogotá con las que ganamos la Datatón, y la entrega de ese día | **Demo de respaldo**: si el caso del cliente no tiene datos a tiempo, el kit corre con estas cifras. También sirve para la lámina "experiencia previa" |
| [`defacc/`](defacc) | El análisis de los 18 proyectos del Defensive Acceleration Hackathon y qué se llevó de cada uno al kit | Saber de dónde sale cada capa y responder "¿por qué lo hicieron así?" |

Correr el kit con los datos del DANE (sin tocar el código):

```bash
KIT_DATOS=respaldo/dane python -m kit.servidor
```

```bash
KIT_DATOS=respaldo/dane python -m kit.medir
```

En Windows con PowerShell: `$env:KIT_DATOS="respaldo/dane"; python -m kit.servidor`.
