# El cliente de punta a punta: Asoexport (LEAD Aspire Colombia, 27-nov-2026)

Lectura completa de la plataforma del evento (Equipo 9) y de todos sus recursos, hecha el 27 de noviembre de 2026.
Todo lo que viene del caso lleva su fuente. Lo que es inferencia nuestra está marcado como **hipótesis** y hay que
validarlo con el cliente en vivo.

Fuentes leídas:
- Plataforma: Descubre (El reto, Perfil de Asoexport, La cadena del café con los perfiles completos, Panel del
  sector), Configura tu equipo, Define la estrategia, Diseña tu solución y Presenta y entrega.
- PDF: *Asoexport_Caso_Cafe.pdf* (informe del caso, 4 págs.), *consulting-es* (resolución consultiva), *mdreview-es*
  (checklist para el director general), *sow-es.docx* (Statement of Work), ejemplo de pizarra, *foundry-es*,
  *copilot-es*, *security-es* (seguridad y gobernanza), *buildcheck-es* (checklist de creación) y *playbook-es*
  (estrategia del pitch).

## 1. Cómo funciona el reto

Somos un **equipo de cuenta de Microsoft**. El informe aclara que es "un ejercicio de aprendizaje, no una consultoría
real".

| Fase | Qué hay que entregar | Recurso |
|---|---|---|
| Configura tu equipo | Nombre (DeepMachine) y **5 roles**: Account Executive, AI Specialist, Solutions Engineer, Customer Success Account Manager y Cloud Solutions Architect. Hay 6 integrantes registrados y **0 roles asignados** | — |
| 1. Descubre | Entender el reto, a Asoexport, la cadena y el panel. Conversar con los 4 personajes ("Hacer una pregunta") | Informe del caso |
| 2. Define la estrategia | Pizarra de mapeo de oportunidades, **Statement of Work (SOW)** y revisión con el "director general" | consulting, sow, mdreview |
| 3. Diseña tu solución | Prototipo funcional con IA, seguro y responsable | foundry, copilot, security, buildcheck |
| 4. Presenta y entrega | Pitch y **subir la presentación final (y el enlace a la demo) antes del pitch**: no se conectan laptops en el escenario | playbook |

Además hay un coach con IA ("Preguntar al coach") y la opción de conversar con cada personaje.

## 2. El cliente

**Asoexport**, la Asociación Nacional de Exportadores de Café de Colombia (informe del caso, pág. 1):
- Gremio privado sin ánimo de lucro con sede en Bogotá. Nació el 17-jun-1933 como Sociedad de Exportadores de Café.
- Representa **más del 75 % de las exportaciones** de café. Tiene alianza con Analdex desde 2017.
- Hace gestión gremial ante ministerios, ICA, Invima y DIAN; trabaja con puertos y navieras; ofrece formación
  (Asoexport Academy); publica cifras con Analdex; organiza la Cumbre Cafetera (edición 90, Cartagena, 5 y 6-nov-2026).
- Expone en vivo su presidente ejecutivo, **Gustavo Andrés Gómez Montero**.

**Hipótesis:** Asoexport no opera fincas ni compra café. Representa a los exportadores. Una solución "para
Asoexport" tiene que servirle **al gremio**: un estándar o servicio compartido que adopten sus afiliados, no
un software para una sola empresa.

## 3. El problema

> "No existen sistemas interoperables que conecten la información de la finca con la trilladora. En el café
> convencional es casi imposible saber de qué predio viene un lote." (informe, pág. 1)

**Por qué importa ahora:**
- La Unión Europea compra entre el 25 % y el 27 % del café colombiano.
- El reglamento europeo contra la deforestación (EUDR, UE 2023/1115) exige **geolocalización poligonal y debida
  diligencia**.
- La directiva CS3D (UE 2024/1760) exige debida diligencia en sostenibilidad a las empresas compradoras.

**La pregunta del reto:** *¿Cómo puede la IA ayudar a construir trazabilidad desde fincas pequeñas, con poca señal
y baja adopción digital?*

### Cifras del caso (fuente: informe de Asoexport)

| Indicador | Dato |
|---|---|
| Exportaciones de enero a octubre de 2026 | 9,57 M de sacos, 11,9 % menos que en 2025 |
| Año 2025 | 13,14 M de sacos por USD 6.480 M, el mayor valor de la historia |
| Se exporta | 92 % de la producción, casi todo como café verde |
| Productores | 557.000 productores y 661.000 fincas, la mayoría de menos de 5 ha. La plataforma también dice "550.000 familias" |
| Destinos (primer semestre de 2026) | EE. UU. 39 %, UE más de 27 %, Asia 11 %, Canadá 7 % |
| Puertos | Buenaventura 62,4 %, Cartagena 29,8 %, Santa Marta 6,5 % |
| Peso en el agro | Cerca del 15 % del PIB agropecuario y más de 2 M de empleos |
| Conectividad | 28 % de internet móvil rural frente a 76 % urbano. Acceso a internet: 41,4 % en zonas rurales dispersas frente a 70,5 % en cabeceras. El 96,1 % de las conexiones es desde el celular, con predominio de 2G y 3G |
| Adopción digital | SICA, Agronet y SIPSA tienen baja adopción porque "no están pensadas para la población rural". En Huila, el 50 % no usa ninguna herramienta informática para planear su logística |

Para el pitch, usemos las cifras de Asoexport con su fuente: el cliente es Asoexport.
`docs/INDUSTRIA_CAFE_2026.md` tiene otras series (FNC, DANE/DIAN) con diferencias pequeñas.

**Ojo con SICA.** Nuestra investigación (Racafé, citado por Mongabay) dice que la geolocalización "está en gran parte
resuelta" gracias al SICA. El caso dice que el SICA tiene baja adopción. No hay que afirmar ninguna de las dos
versiones: hay que **preguntárselo a Gustavo Gómez**.

### Tres territorios (informe, pág. 3)

| Departamento | Producción | Fincas | Uso de TIC |
|---|---|---|---|
| Huila | 169.251 t (20,1 %), 1,46 t/ha | Más de 100.000, de 1,43 ha en promedio | 68 % usa algún insumo TIC; mucha dependencia de 2G |
| Cauca | 98.465 t (11,7 %), cafés de origen | Más de 113.000, de 0,81 ha (las más pequeñas) | 53 %, la mayor brecha digital; retos de seguridad y vías |
| Santander | 50.567 t (6,0 %), en expansión | 38.009 en 75 municipios, 1,37 ha | 90 %, la mayor penetración; dispersión y cafetales viejos |

### Otros problemas estructurales (informe, pág. 3)

- Pagos en efectivo: impiden la trazabilidad financiera.
- Clima: El Niño y La Niña.
- Costo de los insumos y falta de recolectores.
- Ingreso atado al contrato C de Nueva York y a la tasa de cambio.
- Envejecimiento de productores y cafetales, y migración juvenil.
- Brechas de género: las mujeres son más del 50 % de la mano de obra rural, con menos acceso a recursos.

## 4. La cadena y dónde se rompe

| Eslabón | Qué pasa | Dolor | Datos disponibles | Peso en la trazabilidad |
|---|---|---|---|---|
| 1. Aprovisionamiento | Insumos desde cabeceras y cooperativas | Insumos caros, zonas dispersas | Bajo | Medio |
| 2. Producción | Ladera, recolección manual. Cosecha de septiembre a diciembre y mitaca de marzo a junio | Fragmentación, clima, falta de recolectores | **Muy bajo** | **Alto** |
| 3. Beneficio | En la finca: despulpado, fermentación de 18 a 24 h, secado hasta 10 %–12 % de humedad | Secado artesanal sin control | **Muy bajo** | **Alto** |
| 4. Acopio | Pesaje, muestreo, calidad y consolidación | Pocas bodegas adecuadas, pagos en efectivo | Bajo | **Alto** |
| 5. Trilla e industria | Más de 80 trilladoras en 13 departamentos y 837 torrefactoras (97 % micro y pequeñas) | **Sin enlace de datos con la finca de origen** | Medio | **Alto** |
| 6. Distribución y exportación | Más de 90 % por carretera, con 30 %–50 % más carga en cosecha | Vías terciarias, pocos contenedores, hurto | Medio | Medio |

**Hipótesis central:** la trazabilidad se rompe en el **acopio**. Es el primer punto donde se mezcla café de cientos
de fincas, se paga en efectivo y se registra en papel. Lo que no se registra ahí ya no se puede reconstruir en la
trilla ni en la exportadora.

## 5. Las cuatro personas (perfiles completos de la plataforma)

Son personajes ficticios construidos con datos reales.

| Persona | Su realidad (perfil completo) | Su frase | Qué necesita |
|---|---|---|---|
| **Rosa Elvira Cuéllar**, caficultora en Huila (1,4 ha) | Recoge a mano en cosecha y mitaca. Seca al sol y vende pergamino seco a la cooperativa. Celular de gama media con WhatsApp; "la señal 2G va y viene" | "Yo sé de dónde sale mi café. El problema es demostrarlo." | Precio justo; herramientas simples que funcionen sin señal; no perder tiempo en cosecha |
| **Hernán Muñoz**, jefe de acopio de una cooperativa en Cauca | Recibe pergamino de cientos de fincas de menos de 1 ha. Pesa, muestrea, revisa la humedad y paga casi siempre en efectivo. **Registros en papel y en una hoja de cálculo.** La bodega no controla la humedad | "Recibo café de cientos de fincas y casi todo se paga en efectivo." | Registrar lotes sin papel; operar sin internet; cuidar la calidad |
| **Laura Restrepo**, gerente de cumplimiento de una exportadora en Bogotá | Responde por la debida diligencia de cada lote que va a Europa. Coordina trilladoras, transporte a Buenaventura, VUCE y DIAN | "Si no tengo el polígono de cada finca, no entro a Europa." | Cumplir el EUDR; conectar los datos de finca con DIAN y VUCE; controlar el costo por lote |
| **Anke Vogel**, compradora de una tostadora en Hamburgo | Compra arábigo lavado colombiano. No puede vender en la UE sin debida diligencia, y su empresa responde a la CS3D. **Colombia compite con Brasil y Vietnam** | "Necesito pruebas de no deforestación antes de firmar el contrato." | Debida diligencia por lote; certificaciones verificables; entregas a tiempo |

**Hipótesis:**
- Cada persona necesita algo distinto. Rosa y Hernán **producen** el dato; Laura y Anke lo **consumen** y responden
  por él.
- Si la solución no le da algo a Rosa (precio, tiempo, cero esfuerzo), Rosa no la usa.
- Anke tiene alternativas (Brasil, Vietnam): la trazabilidad es una **ventaja competitiva** para Colombia, no solo
  cumplimiento.

## 6. Lo que pide Asoexport: principios de diseño (informe, pág. 4)

Asoexport "recomienda respetar esta secuencia":

1. **Madurez digital por etapas.** Primero ordenar el dato y la trazabilidad por lote. Después, sensores IoT y
   analítica avanzada.
2. **Diseño para el campo:**
   - Funcionar sin conexión y sincronizar después.
   - Canales de bajo consumo, como WhatsApp Business o USSD.
   - Pictogramas o voz, pensados para celulares de gama media.
   - Wi-Fi comunitario en los centros de acopio.
3. **Interoperabilidad y cumplimiento:**
   - Polígonos GPS capturados sin conexión.
   - Verificar la no deforestación con Open Foris o alertas GLAD/GFW.
   - Seguir el estándar GS1 EPCIS 2.0.
   - Conectar con certificadoras y con RNDC, VUCE y DIAN.
4. **Gobernanza y apropiación.** Reglas claras sobre propiedad, consentimiento y privacidad del dato, y
   alfabetización digital con redes de productores líderes.

**Esto es lo más valioso del caso.** El cliente ya dijo cómo quiere que se diseñe. Una propuesta que empiece por
IoT, por un modelo de IA sofisticado o por blockchain va contra su principio 1.

## 7. Mapa de oportunidades (borrador, siguiendo la guía de resolución consultiva)

| Paso | Contenido |
|---|---|
| Señales | Las cuatro frases de la sección 5. "Sin enlace de datos con la finca de origen". Registros en papel y hoja de cálculo. Efectivo. 2G. Baja adopción de SICA, Agronet y SIPSA |
| Patrón | El origen lo conoce la caficultora, pero se pierde en el acopio y no llega a la trilla ni a la exportadora |
| Insight (hipótesis) | El problema es de **captura en el momento de la compra**, no de tecnología de exportación. Y quien carga el dato (Rosa, Hernán) no es quien recibe el beneficio (Laura, Anke) |
| Causa raíz (hipótesis) | La compra en el acopio no produce un registro digital ligado al predio. No hay estándar compartido ni incentivo para quien registra |
| Oportunidad | "¿Cómo podríamos lograr que cada compra en el acopio deje, sin señal y sin esfuerzo extra, la evidencia de origen que la exportadora necesita para Europa?" |

**Opciones (abrir antes de elegir):**

| Opción | Para quién | Alineación con los principios de Asoexport |
|---|---|---|
| A. Registro de compra sin conexión en el acopio (voz o pictogramas, se sincroniza con Wi-Fi en la bodega) | Hernán | Alta (principios 1 y 2) |
| B. Registro único del polígono de cada finca, guiado por WhatsApp y capturado sin señal | Rosa | Alta (principios 2 y 3) |
| C. Expediente de debida diligencia por lote, que la IA arma y el código verifica antes de despachar | Laura y Anke | Alta (principio 3) |
| D. Pago digital ligado al lote | Rosa y Hernán | Media: depende de bancos y de los hábitos de pago |
| E. Sensores IoT de humedad en las bodegas | Hernán | Baja por ahora: Asoexport lo pone después (principio 1) |

**Propuesta para discutir en equipo (hipótesis):** "Pasaporte del lote", hecho de **A + B + C**:

1. **Finca (una sola vez):**
   - Rosa registra el polígono de su finca por WhatsApp, con voz o pictogramas, aunque no tenga señal.
   - Da su consentimiento explícito.
   - El polígono se cruza con alertas de deforestación.
2. **Acopio (cada compra):**
   - Hernán registra peso, humedad y finca en el celular, sin internet.
   - Al consolidar, el lote conserva la lista de fincas que lo componen, como eventos GS1 EPCIS.
3. **Exportadora:**
   - Laura recibe por lote un expediente con cada dato y su evidencia.
   - La IA redacta la declaración de debida diligencia y **el código verifica** cada dato.
   - El código bloquea un despacho a Europa si falta un polígono o si el volumen es imposible para el área de la
     finca (en Huila el rendimiento promedio es de 1,46 t/ha).
4. **Comprador:** Anke recibe pruebas verificables por lote.

### Qué del kit ya sirve y qué falta

| Ya existe en el kit | Falta (no está construido) |
|---|---|
| Guardián que bloquea despachar a Europa un lote sin geolocalización (`maestros.json`, regla del reglamento europeo) | Captura en el campo sin conexión (WhatsApp o app) |
| "La IA propone, el código verifica": cifras y citas comprobadas | Polígonos GPS y cruce con alertas de deforestación |
| Alerta de cifras imposibles (`kit/exportar.py`) | Eventos GS1 EPCIS y conexión con VUCE y DIAN |
| Aprobación humana en Teams, bitácora encadenada, sello de integridad | Consentimiento y gobernanza del dato de cada productor |
| Revisión de documentos con trampas (fraude por correo, instrucciones escondidas) | Interfaz para Rosa y Hernán (voz o pictogramas) |

En el pitch hay que decir con claridad qué está en vivo, qué está simulado y qué es maqueta (lo exige el checklist
de creación).

## 8. Preguntas para Gustavo Gómez en vivo

1. ¿En qué eslabón se pierde hoy el dato de la finca: en el acopio, en la trilla o en ambos?
2. ¿Cuántos afiliados ya tienen polígonos de sus fincas proveedoras, y de dónde los sacaron (SICA, levantamiento
   propio)?
3. ¿Quién debería pagar la trazabilidad: la caficultora, la cooperativa, la exportadora o el comprador? ¿Hay prima?
4. ¿Qué evidencia acepta hoy un comprador europeo como Anke? ¿Un PDF, un sistema, una certificadora?
5. ¿Asoexport quiere ofrecer un estándar o servicio gremial, o que cada exportador resuelva por su cuenta?
6. ¿Qué tan dispuestas están las cooperativas a dejar el papel y el efectivo? ¿Qué intentos fallaron antes?
7. ¿Qué datos no deberían salir de la finca (privacidad, seguridad en zonas como el Cauca)?

## 9. Lo que se entrega y cómo lo van a evaluar

**Revisión con el director general (checklist `mdreview`).** Hay que poder decir que sí a esto:
- La recomendación se basa en lo que dijo el cliente.
- El problema se explica en 1 o 2 frases.
- Se ataca la causa raíz, no el síntoma.
- Se evaluaron varias opciones.
- El alcance es claro: qué entra y qué no.
- El valor se puede medir.
- Hay riesgos con mitigación.
- Hay seguridad e IA responsable.
- El mapa de solución está dentro del SOW.
- La historia "Evidencia → Problema → Parte interesada → Solución → Impacto" se cuenta en menos de 60 s.
- Sabemos exactamente qué decisión le vamos a pedir.

**Statement of Work (17 secciones).** Resumen ejecutivo (150–250 palabras), problema y tamaño de la oportunidad con
supuestos marcados, evidencia, preparación del cliente, solución, mapa de solución ejecutiva (captura de la
pizarra), alcance dentro y fuera, partes interesadas, equipo y recursos de Microsoft, valor, medidas de éxito,
tecnología, plan de entrega, riesgos, seguridad e IA responsable, decisión solicitada y comentarios del director.

**Pitch (`playbook`).** Gancho → Problema → Insight → Solución → Demo → Impacto.
- "Si el público solo recuerda tres cosas, que sean el problema, tu recomendación y el valor."
- Títulos que sean conclusiones, una idea por diapositiva.
- Demostrar el valor, no la arquitectura.
- Ser transparentes con lo que está en vivo y lo que está simulado.
- Tener un plan B.
- Responder preguntas con esta forma: respuesta → evidencia → limitación → qué haríamos después.

**Seguridad (`security`).** Confianza Cero, identidad (Entra ID), privilegio mínimo, secretos fuera del código (Key
Vault), recorrido de los datos (recopilar, clasificar, proteger, usar, conservar), registros sin secretos, IA
responsable y aprobación humana para las acciones. El kit ya cubre buena parte de esto; los límites conocidos
están en `docs/SEGURIDAD.md`.

## 10. Pendientes del equipo en la plataforma

- Asignar los 5 roles (hoy hay 0 de 5).
- Usar "Hacer una pregunta" con cada personaje para tener evidencia propia de descubrimiento.
- Llenar la pizarra y el SOW.
- Subir la presentación final antes del pitch.
