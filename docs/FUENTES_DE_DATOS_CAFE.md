# Fuentes oficiales de datos del café: qué tiene API y qué no

Probado el 26 de noviembre de 2026 desde el kit, sin claves. Resumen: **no existe una API pública de la Federación
Nacional de Cafeteros ni de una asociación de exportadores**. Sí hay una API abierta del Estado (datos.gov.co) y la
Federación publica archivos que se leen solos (PDF con texto y Excel). El kit ya trae dos de esas fuentes con
`python -m kit.mercado`.

| Fuente | Qué trae | ¿API? | Cómo se usa | Estado en el kit |
|---|---|---|---|---|
| **TRM, Superintendencia Financiera** en datos.gov.co (conjunto `32sa-8pi3`) | Tasa de cambio oficial de cada día, desde 1991 | **Sí**, abierta (Socrata/SODA), sin clave | `https://www.datos.gov.co/resource/32sa-8pi3.json?$order=vigenciadesde DESC&$limit=1` | **Conectado**: `kit.mercado actualizar` (cifra `trm_cop_usd`) y la serie de Power BI (`trm_oficial.csv`) |
| **Precio del café, Federación** (`precio_cafe.pdf`) | Cada día hábil: cierre del contrato C en Nueva York y precio interno de la carga de 125 kg | No; PDF con texto, misma dirección todos los días | Se descarga y se lee con reglas; si cambia el formato, el kit avisa y no toca la cifra | **Conectado**: cifras `precio_contrato_c_usd_lb` y `precio_interno_cop_carga` |
| **Estadísticas de la Federación** (Excel) | Precio interno diario y mensual, precio ex-dock, precio OIC, área, producción mensual; exportaciones por tipo, puerto, destino y **exportador** | No; Excel descargable (`Precios-area-y-produccion-de-cafe-<Mes>-2026.xlsx`, `Exportaciones-<Mes>-2026.xlsx`) | Power BI → Obtener datos → Web, con la dirección del Excel; o cargarlos a Snowflake | Sin conectar. Fue la fuente de las cifras de `docs/INDUSTRIA_CAFE_2026.md` |
| **Aptitud del suelo para café, UPRA** en datos.gov.co (`kwvf-nwea`) | 508.129 polígonos con municipio, departamento, área y aptitud (alta, media, baja, no apta) | **Sí**, abierta (Socrata, con geometría) | `https://www.datos.gov.co/resource/kwvf-nwea.json?municipio=...` | Sin conectar. Sirve para dar contexto a un lote (¿la finca está en zona apta?), **no** prueba ausencia de deforestación |
| **DANE**: exportaciones (partida 0901), ENA, IPC, PIB | Valor y volumen exportado oficiales, por destino y departamento | No se encontró API para comercio exterior; boletines en PDF, anexos en Excel y microdatos | `microdatos.dane.gov.co` (catálogos de exportaciones y ENA) | Sin conectar |
| **Banco de la República** | Series macro y boletines regionales (Central Cafetera) | No se verificó una API; descargas desde su portal de series | Excel o CSV descargados | Sin conectar |
| **Contrato C de ICE (bolsa de Nueva York)** | Precio intradía y diario | Sí, pero **con licencia de pago** (o proveedores en Snowflake Marketplace) | No usar sin licencia | El kit usa el cierre que publica la Federación |
| **SICA y cédula cafetera (Federación)** | Fincas, lotes georreferenciados, productores | No es público | Por convenio con la Federación y con autorización de cada productor (Ley 1581) | No aplica en la demo |

## Cómo contarlo el viernes

> "No inventamos el precio ni lo copiamos a mano: el asistente trae la TRM de la Superintendencia Financiera por la API
> abierta de datos.gov.co y el precio del café que publica la Federación cada mañana. Cada cifra queda con su fecha, su
> fuente y su huella, y si una fuente falla, el asistente lo dice en vez de inventar."

Y si la cafetera pregunta "¿y nuestros datos?": esos van por Snowflake (`kit.snowflake traer`), con el mismo sello.

## Para el equipo

```bash
KIT_DATOS=casos/cafe python -m kit.mercado actualizar
```

```bash
python -m kit.mercado trm --desde 2025-11-20 --csv plantillas/powerbi/datos/trm_oficial.csv
```

```bash
python plantillas/powerbi/generar_datos.py
```

Límites honestos: datos.gov.co sin clave tiene un límite de solicitudes (suficiente para esto); el PDF de la Federación
puede cambiar de formato sin aviso; el precio interno que publica la Federación es un precio base de mercado para
pergamino FR 94, no lo que paga cada exportadora.
