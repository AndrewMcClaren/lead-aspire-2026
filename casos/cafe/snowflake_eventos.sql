-- Tabla de entregas del acopio (eventos EPCIS) que escribe kit.whatsapp a través de kit.snowflake.guardar_eventos.
-- Córranlo una vez en Snowflake y pongan SNOWFLAKE_TABLA_EVENTOS=CAFE.PUBLIC.EVENTOS_ACOPIO en el .env.

CREATE TABLE IF NOT EXISTS CAFE.PUBLIC.EVENTOS_ACOPIO (
    EVENT_ID     STRING PRIMARY KEY,
    EVENT_TIME   TIMESTAMP_TZ,
    LOTE         STRING,
    FINCA_ID     STRING,
    KG           NUMBER(12, 1),
    HUMEDAD_PCT  NUMBER(5, 2),
    APTO_UE      BOOLEAN,
    CANAL        STRING,
    EVENTO_JSON  STRING,           -- el evento completo; se puede leer con PARSE_JSON(EVENTO_JSON)
    CARGADO      TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP()
);

-- Recomendado: un rol que solo pueda insertar en esta tabla (el kit no necesita más permisos para escribir).
-- CREATE ROLE IF NOT EXISTS KIT_ACOPIO;
-- GRANT USAGE ON DATABASE CAFE TO ROLE KIT_ACOPIO;
-- GRANT USAGE ON SCHEMA CAFE.PUBLIC TO ROLE KIT_ACOPIO;
-- GRANT INSERT ON TABLE CAFE.PUBLIC.EVENTOS_ACOPIO TO ROLE KIT_ACOPIO;

-- Vista para Power BI: kilos por lote y cuánto es apto para la Unión Europea.
CREATE OR REPLACE VIEW CAFE.PUBLIC.ACOPIO_POR_LOTE AS
SELECT LOTE,
       COUNT(*)                          AS ENTREGAS,
       SUM(KG)                           AS KG_TOTAL,
       SUM(IFF(APTO_UE, KG, 0))          AS KG_APTO_UE,
       MAX(EVENT_TIME)                   AS ULTIMA_ENTREGA
FROM CAFE.PUBLIC.EVENTOS_ACOPIO
GROUP BY LOTE;
