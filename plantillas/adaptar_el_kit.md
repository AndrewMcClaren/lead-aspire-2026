# Adaptar el kit al caso del cliente (30 minutos)

El kit funciona con cualquier tabla de cifras. El día del evento solo se cambian tres cosas; el código no
se toca. Practíquenlo antes con otros datos (por ejemplo, unas cifras públicas de su ciudad).

## 1. Las cifras: `kit/datos/cifras.csv` (15 minutos)

Una fila por cifra que el asistente pueda decir. Columnas:

| Columna | Qué va | Ejemplo |
|---|---|---|
| `clave` | Nombre corto, sin espacios ni tildes | `devoluciones_pct` |
| `descripcion` | Qué es la cifra, en palabras de una persona | `% de pedidos devueltos en octubre` |
| `valor` | El número, con punto decimal | `4.8` |
| `unidad` | `%`, `pesos`, `millones de pesos`, `clientes`, `días`… | `%` |
| `decimales` | Cuántos decimales mostrar | `1` |
| `fuente` | De dónde salió: archivo, sistema o persona del cliente | `Reporte de ventas de octubre (cliente)` |
| `sinonimos` | Opcional: palabras que usaría alguien al preguntar (solo ayuda al modo simulado) | `devoluciones devuelven` |

Reglas:
- Solo cifras que el cliente les dio o que ustedes calcularon y pueden mostrar cómo.
- Si una cifra es una estimación, dilo en la descripción ("estimado", "aproximado").
- Datos del cliente: si son confidenciales, no los suban a un repositorio público.

## 2. El contexto: `kit/datos/contexto.md` (5 minutos)

Quién es el cliente, qué hace el asistente y qué datos NO tiene (por ejemplo "no hay cifras por ciudad").
**Sin números**: los números van solo en el CSV.

## 3. Las preguntas sugeridas: `SUGERIDAS` en `kit/servidor.py` (5 minutos)

Cuatro preguntas que muestren lo más importante y **una sin dato**, para mostrar en vivo que el asistente
dice "no tengo ese dato verificado" en vez de inventar.

## 4. Probar (5 minutos)

```bash
python -m pytest -q
```

Las pruebas que usan las cifras de ejemplo se saltan solas cuando cambian el CSV ("skipped"). Las que
importan siguen corriendo: cifras escritas a mano, claves inventadas, documento con trampa y aprobaciones.

```bash
python -m kit.servidor --modelo azure:<deployment>
```

Hagan las cinco preguntas sugeridas, peguen el documento con trampa y propongan un pago. Si todo responde
bien, la demo está lista.
