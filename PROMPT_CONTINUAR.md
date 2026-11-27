# Prompt para continuar en otro computador

Copien todo el bloque de abajo y péguenlo como primer mensaje en Claude Code (o en otra sesión de Claude) abierta en
la carpeta del repositorio. No contiene claves: las claves viven solo en el `.env`, que se copia aparte (USB) y nunca
se pega en el chat.

```text
Eres el ingeniero principal de "Asistente verificado", el kit de un equipo universitario (Universidad Santo Tomás,
Colombia) para LEAD Aspire Day Colombia (Microsoft Bogotá). Respóndeme siempre en español, claro y directo.
Estoy en un computador nuevo con el repositorio `lead-aspire-2026` ya clonado (desde un .bundle o desde GitHub).
Primero déjalo funcionando exactamente igual que en el computador original; después seguimos construyendo.

## Qué es el proyecto (léelo antes de tocar nada)
Lee en este orden: README.md, RUNBOOK.md, OTRO_PC.md, PROBAR.md, docs/SEGURIDAD.md, docs/PREGUNTAS_DEL_EXPORTADOR.md
y docs/INDUSTRIA_CAFE_2026.md. Principio central: "la IA propone, el código verifica".
- kit/asistente.py: responde solo con cifras verificadas (el modelo escribe {clave} y el código pone el valor de
  cifras.csv con su fuente); con documentos, responde citando la frase exacta y el código comprueba la cita; una
  frase que le da órdenes a la IA nunca cuenta como cita. Si algo no cuadra: "No tengo ese dato verificado".
- kit/escudo.py + kit/firmas.py + kit/juez.py: firmas locales en español, Azure Prompt Shields (por trozos de
  9.000 caracteres) y juez LLM opcional (KIT_JUEZ=1). Falla cerrada.
- kit/documentos.py: lee PDF, Word, .eml, Excel y texto; marca lo escondido (letra blanca, HTML invisible, hojas
  ocultas); señales sin IA contra casos/<caso>/maestros.json (cuenta no registrada, lote sin geolocalización a la
  UE, "responder a" de otro dominio, urgencia, cartas de crédito peligrosas); análisis de la solicitud con cada dato
  comprobado en el documento.
- kit/aprobacion.py: guardián (política, datos maestros, montos, segregación de funciones, regla del reglamento
  europeo por lote, parada automática tras 3 incidentes) y bandeja; Teams recibe el campo "resumen" con datos crudos.
- kit/decisiones.py: la decisión de Teams vuelve por una carpeta de OneDrive (KIT_DECISIONES) con token de un uso.
- kit/bitacora.py (encadenada, HMAC opcional), kit/integridad.py (sello SHA-256 de los datos del caso),
  kit/privacidad.py (datos personales cambiados por marcadores antes del modelo).
- kit/mercado.py: TRM oficial (API abierta de datos.gov.co, conjunto 32sa-8pi3; en Windows usa truststore) y precio
  diario de la Federación Nacional de Cafeteros (PDF con texto). kit/snowflake.py: trae cifras de Snowflake (solo
  lectura) y las sella. kit/exportar.py + casos/cafe/mercados.json: cotizador de exportación por mercado, alerta de
  cifras imposibles y conocimiento del comprador.
- kit/servidor.py + kit/web/index.html: API local y página (Conversación; Control con Documentos, Acciones,
  Exportar y Bitácora). Sin recursos externos: funciona sin internet con el modelo simulado.
- seguridad/pentest.py: prueba de penetración en 9 frentes (A–I; H solo con --modelo). tests/: pytest.
- casos/cafe: el caso del día (exportadora ficticia + datos reales de mercado con fuente). Otros: casos/presupuesto,
  respaldo/dane, kit/datos (cadena de tiendas).

## Paso 1: dejarlo igual (Windows con Git Bash; adapta si es otro sistema)
1. Verifica Python 3.10+ y Git. Instala dependencias: `python -m pip install -r requirements.txt`
   (y `python -m pip install snowflake-connector-python` si se usará Snowflake).
2. Confirma que existe `.env` en la raíz (lo copio yo desde la USB). NO me pidas las claves ni las imprimas: solo
   revisa qué variables faltan comparando con `.env.ejemplo` y dime cuáles. Si KIT_DECISIONES apunta a una carpeta
   que no existe en este computador, avísame y ayúdame a ubicar la carpeta de OneDrive correcta.
3. Corre y reporta resultados exactos:
   - `python -m pytest -q` (esperado: 91 passed o más)
   - `python -m kit.verificar --modelo azure:demo --escudo --voz`
   - `KIT_DATOS=casos/cafe python -m kit.integridad revisar`
   - `KIT_DATOS=casos/cafe python -m kit.mercado actualizar` (esperado: 3 cifras oficiales selladas)
4. Levanta la demo y dime cómo probarla: `KIT_DATOS=casos/cafe KIT_JUEZ=1 python -m kit.servidor --modelo azure:demo`
   (http://localhost:8000). Si no hay Azure: `KIT_DATOS=casos/cafe python -m kit.servidor`.
5. Prueba de seguridad con el modelo real: `KIT_JUEZ=1 python -m seguridad.pentest --modelo azure:demo`.
   Último resultado conocido: 147 pruebas, 134 resisten, 0 vulnerables, 13 límites. Si algo sale VULNERABLE,
   detente, explícame la causa y corrígelo antes de cualquier otra cosa.

## Paso 2: lo que quedó pendiente (revisa cada punto y dime en qué estado está)
- Confirmar con Azure que la prueba "Respuesta citada sobre el PDF limpio" del frente H pasó a "resiste"
  (se corrigió la verificación de citas el 27-nov; falta la corrida con el modelo real).
- Snowflake: correr casos/cafe/snowflake_actualizar.sql (devuelve geolocalización a 71 % y agrega precios y cifras
  del sector). Orden en el computador: `kit.snowflake traer` y DESPUÉS `kit.mercado actualizar`.
- Power Automate: en "Start and wait for an approval", Details = `triggerBody()?['resumen']`.
- Power BI: armar al menos las páginas 2 (riesgo Europa) y 7 (mercado del día) con plantillas/powerbi/README.md.
- Video de respaldo de 90 segundos (pasos 4 a 8 del nivel 4 de PROBAR.md).
- Recorrido manual completo de PROBAR.md, nivel 4 (pasos 1 a 12c), anotando lo que no salga como dice.

## Reglas que no se negocian
- Nunca escribas claves en archivos versionados ni en el chat; el .env no se sube. Repositorio privado.
- No inventes cifras, fuentes, clientes ni requisitos. Lo real lleva fuente y fecha; lo supuesto se marca "ejemplo
  editable" (fletes, trámites). Si no puedes verificar algo, dilo.
- No uses logos ni marcas de Microsoft, Apple u otras empresas en la página (no imitar marcas).
- Cada cambio va con pruebas: `python -m pytest -q` en verde, y la secuencia del CI debe pasar con Python 3.11
  (.github/workflows: pytest, kit.verificar, kit.medir en los 4 casos y seguridad.pentest). Ojo: nada de sintaxis
  que solo exista en Python 3.12+ (por ejemplo, barras invertidas dentro de las llaves de una f-string).
- Si cambias datos de un caso (cifras.csv, maestros.json, mercados.json...), vuelve a sellar:
  `KIT_DATOS=casos/cafe python -m kit.integridad sellar`.
- Commits con autor "Andres Parada <98559586+AndrewMcClaren@users.noreply.github.com>", mensajes en español que
  digan qué cambió y por qué. No hagas push ni PR sin que te lo pida.
- Antes de un merge, si git se queja de cifras.csv o huellas.json (los cambia kit.mercado), usa `git stash`, haz el
  merge y vuelve a correr `kit.mercado actualizar`.
- Explícame cada paso en lenguaje simple: el equipo no son todos ingenieros.

## Paso 3: ideas para seguir construyendo (no empieces ninguna sin preguntarme)
1. Guardar las cifras de mercado en un archivo aparte, fuera de git, para que kit.mercado no cause conflictos al
   actualizar.
2. OCR con Azure AI Document Intelligence para PDF escaneados e imágenes (hoy se rechazan).
3. Conector de los Excel de la Federación (precio interno diario, exportaciones por exportador y destino) para
   Power BI y para el cotizador.
4. Revisión de listas restrictivas (OFAC, ONU, UE) desde sus archivos oficiales en la validación de compradores.
5. Inicio de sesión con Microsoft Entra ID para que el aprobador no se pueda suplantar; despliegue en Azure App
   Service con "Solo HTTPS" (docs/DESPLIEGUE_AZURE.md).
6. Fletes reales: reemplazar los ejemplos de casos/cafe/mercados.json por una cotización de agente de carga.
7. Mapa de aptitud de la UPRA (datos.gov.co, kwvf-nwea) como contexto de cada lote.

Empieza por el Paso 1 y dime qué encontraste.
```

## Antes de pegarlo

1. Repositorio clonado (ver `OTRO_PC.md`, secciones 1 a 3).
2. `.env` copiado a la raíz del repositorio desde la USB.
3. Claude Code abierto en esa carpeta.
