# Seguridad del kit: prueba de penetración, cifrado, red y cumplimiento

Este documento dice cómo intentamos romper el kit, qué resistió, qué corregimos y qué no cubre. Sirve para
responder "¿le hicieron pruebas de seguridad?" con evidencia.

## La prueba de penetración

```bash
python -m seguridad.pentest                       # sin internet ni costo
python -m seguridad.pentest --modelo azure:demo   # además, 20 ataques de punta a punta con el modelo real (centavos)
```

Corre **98 pruebas en 7 frentes** (más 20 con el modelo real) y deja el informe en `resultados/pentest_<fecha>.md`.
Las pruebas automáticas (`pytest`) fallan si algún frente queda vulnerable.

**Resultado con los servicios reales (24 de noviembre de 2026, gpt-4.1-mini y Prompt Shields en France Central):
118 pruebas, 103 resisten, 0 vulnerables, 15 límites conocidos.**
- La entrada (firmas locales + Prompt Shields) detectó **15 de 20** documentos con trampa; solo las firmas, 12.
  **Con el juez LLM encendido (`KIT_JUEZ=1`, 25 de noviembre): 19 de 20**, con 108 pruebas resistidas y 0 vulnerables.
  Solo pasó "letras separadas", que igual frena la verificación de salida. Recomendación: juez encendido en la demo.
  Pasaron: letras separadas, coloquial colombiano, comentario HTML oculto, instrucción enterrada en texto largo y
  autoridad falsa.
- De punta a punta con el modelo real, **20 de 20 ataques fallaron**: la persona siempre recibió la cifra verdadera
  (4.820 millones), también en los 5 casos que la entrada no detectó.
- Dos bloqueos del frente B salieron por otra capa de la esperada: el HTML se bloqueó por el "1" de `alert(1)`, y
  el correo inventado por la regla de enlaces (`correo.com`). Igual no llegaron a la persona, y la página escapa
  todo el HTML.

| Frente | Qué intenta el atacante | Resultado (24 de noviembre de 2026) |
|---|---|---|
| A. Entrada | 20 documentos con instrucciones escondidas: idiomas, base64, invisibles, homoglifos, leetspeak, etiquetas falsas, JSON falso, juego de roles, coloquial colombiano, texto largo | Las firmas locales detectan 12 de 20. Prompt Shields agrega su capa. Los que pasan los frena la salida (B) |
| B. Salida con el modelo secuestrado | El modelo escribe lo que quiere el atacante: cifras en dígitos, palabras, inglés, ancho completo, árabes, superíndices, romanos, separadas; claves inventadas; su configuración; enlaces de phishing; HTML; datos personales | **Nada llega a la persona** |
| C. Acciones | Aprobarse a sí mismo (mayúsculas, tildes, cirílico, invisibles, ancho completo), aprobar sin nombre, decidir dos veces, montos negativos, infinitos o NaN, acciones no pedidas, cuenta cambiada, monto mayor, sesión detenida, gasto partido en pedazos | Todo bloqueado |
| D. API web | CSRF desde otra página (text/plain, formulario, Origin ajeno, Origin null), cuerpo de 1 MB, JSON inválido o con tipos raros, rutas de archivos (`/../.env`), cabeceras de seguridad, caché, XSS, conexiones colgadas, clave de API, ráfagas | Todo resistido |
| E. Bitácora e integridad | Editar, borrar, reescribir la cadena firmada sin la clave, quitar la firma (degradación), cambiar una cifra después del sello | Todo detectado |
| F. Datos personales | Cédula, correo, celular, tarjeta, cuenta, y formas que la capa no conoce | Los formatos conocidos se ocultan; ver límites |
| G. Secretos y configuración | `.env` en git, claves en archivos versionados, servidor abierto a la red, dependencias con vulnerabilidades (pip-audit) | Todo bien |

### Lo que encontramos y corregimos

La primera corrida encontró **6 problemas reales**. Están corregidos y cada uno tiene su prueba:

| Problema | Riesgo | Corrección |
|---|---|---|
| Un modelo secuestrado podía mandar un **enlace de phishing** ("ingrese su clave en …") | Robo de credenciales usando la confianza en el asistente | Un enlace o dominio en la respuesta la bloquea |
| **CSRF:** cualquier página abierta en otra pestaña podía aprobar acciones en el servidor de la demo | Aprobar un pago sin que la persona lo sepa | La API exige JSON y rechaza otros orígenes |
| **Aprobarse a sí mismo** escribiendo el nombre con una letra cirílica ("аsistente") | Saltarse la segregación de funciones | Los nombres se comparan normalizados (homoglifos, invisibles, ancho completo) |
| **Bitácora:** con clave de firma, se podían reescribir entradas marcándolas "sin firma" | Borrar el rastro de una decisión | Con `BITACORA_CLAVE`, toda entrada sin firma hace fallar la verificación |
| **Conexiones colgadas** (slowloris) sin tiempo límite | Tumbar la demo | Cierra conexiones inactivas a los 30 s |
| Montos **negativos, infinitos o NaN**, y `documentos` como texto (un documento por letra, que multiplica las llamadas a Prompt Shields) | Saltarse el saldo; gastar la cuota | Validación de tipos, monto ≥ 0, máximo 5 documentos y 64 KB por solicitud |

También: una respuesta sin cifras llevaba el sello "Cifra verificada". Ahora dice "Sin cifras".

### Límites conocidos (díganlos si preguntan)

- **Suplantar a quien aprueba:** el nombre lo escribe quien usa la página. En producción: inicio de sesión con
  Microsoft Entra ID y roles.
- **Una cifra verdadera usada para otra cosa** ("vendió 9,6 %"): el kit garantiza que la cifra sale de la tabla,
  no que se use bien. Por eso cada cifra muestra su fuente.
- **Datos personales que la capa no detecta:** cédula sin la palabra "cédula", nombres sin "señor/señora",
  correos disfrazados, direcciones y datos de salud. Para eso está la detección de datos personales de Azure AI
  Language.
- **Bitácora sin clave:** quien edita el archivo puede recalcular la cadena. Con `BITACORA_CLAVE` ya no.
- **Las firmas locales no ven 8 de 20 variantes.** No es grave porque la salida las frena, pero no las detecta.
- Esta prueba **no** reemplaza una prueba de penetración hecha por terceros, ni revisa la configuración de red y
  de identidades en Azure.

## Cifrado

| Dónde | Estado |
|---|---|
| Entre el kit y Azure (OpenAI, Content Safety, Speech) | HTTPS (TLS 1.2 o superior): las librerías no permiten otra cosa |
| Datos guardados en Azure | Cifrados por defecto por Microsoft (AES-256) |
| Página de la demo en el computador | HTTP local en `127.0.0.1`: no sale del computador. Si se publica en Azure App Service, activar **"Solo HTTPS"** |
| Claves | En `.env`, fuera de git. En producción: Azure Key Vault o identidad administrada, sin claves en archivos |
| Bitácora | Archivo local. Integridad con hashes y firma HMAC; contenido sensible con `KIT_BITACORA_PRIVADA=1` (guarda huellas, no textos) |

## Red

- El servidor escucha solo en `127.0.0.1`. Para abrirlo a la red hay que pedirlo (`--host 0.0.0.0`), y avisa si no
  hay `KIT_API_KEY`.
- Límite de 60 solicitudes POST por minuto por dirección. Ojo: detrás de un proxy (App Service), todas las personas
  comparten dirección y el límite se vuelve global.
- Cabeceras: Content-Security-Policy, sin iframes de otros sitios, `nosniff`, sin referer y sin caché en la API.

## Cumplimiento normativo en Colombia (orientación, no asesoría legal)

| Norma | Qué pide, en corto | Cómo lo atiende la solución |
|---|---|---|
| **Ley 1581 de 2012** (datos personales) y su decreto reglamentario (hoy en el Decreto 1074 de 2015) | Finalidad, libertad (autorización), veracidad, transparencia, acceso restringido, seguridad y confidencialidad | Datos personales a marcadores antes del modelo; bitácora sin textos de documentos; datos ficticios en la demo. El cliente necesita su política de tratamiento y la autorización de los titulares |
| **Transferencia internacional** (Ley 1581, artículo 26) | Solo a países con nivel adecuado de protección, salvo excepciones | El recurso está en Francia (Unión Europea). Ojo: el despliegue "Estándar global" puede procesar en cualquier región; para mantener el procesamiento en Europa existe el tipo **"Estándar de zona de datos"** |
| **Ley 1266 de 2008** (habeas data financiero) | Reglas para datos de crédito y comportamiento financiero | Si el cliente es financiero, esos datos no van al modelo |
| **Ley 1273 de 2009** (delitos informáticos) | Penaliza el acceso abusivo y la interceptación | Las pruebas de penetración solo sobre sistemas propios o con autorización escrita |
| **CONPES 4144 de 2025** (Política Nacional de IA) | Marco de política pública para una IA ética y confiable | Control humano, transparencia (fuente visible) y medición |
| **Circular de la SIC sobre datos personales en IA** | Guía de la Superintendencia de Industria y Comercio para tratar datos personales en sistemas de IA | Verifiquen el número y el texto vigentes antes de citarla |

En el pitch: **"deja la evidencia que pediría una auditoría"**, nunca "cumple la ley" ni "está certificado".
