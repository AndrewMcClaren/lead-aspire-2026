-- Pone la tabla CIFRAS de Snowflake al día con el caso del café (corran todo con "Run All").
-- 1) Devuelve el porcentaje de geolocalización a 71 (se cambió a 74 en la prueba del martes).
-- 2) Agrega los dos precios reales de mercado del 25-nov-2026 (fuente: Federación Nacional de Cafeteros).
-- Después, en el computador, en este orden:
--   KIT_DATOS=casos/cafe python -m kit.snowflake traer
--   KIT_DATOS=casos/cafe python -m kit.mercado actualizar   (TRM y precio del café oficiales del día)
USE DATABASE CAFE;
USE SCHEMA PUBLIC;

UPDATE CAFE.PUBLIC.CIFRAS SET VALOR = 71 WHERE CLAVE IN ('pct_lotes_con_geolocalizacion');

DELETE FROM CAFE.PUBLIC.CIFRAS WHERE CLAVE IN ('precio_contrato_c_usd_lb', 'precio_interno_cop_carga');
INSERT INTO CAFE.PUBLIC.CIFRAS (CLAVE, DESCRIPCION, VALOR, UNIDAD, DECIMALES, FUENTE, SINONIMOS) VALUES
  ('precio_contrato_c_usd_lb',
   'Precio del contrato C de café arábica en la bolsa de Nueva York al cierre del 25 de noviembre de 2026',
   2.7, 'dólares por libra', 2,
   'Federación Nacional de Cafeteros, precio de referencia publicado el 25-nov-2026 (dato real de mercado): federaciondecafeteros.org',
   'precio bolsa contrato c nueva york cotizacion libra cierre hoy mercado'),
  ('precio_interno_cop_carga',
   'Precio interno de referencia de la carga de 125 kg de café pergamino seco publicado por la Federación el 25 de noviembre de 2026',
   2180000, 'pesos por carga', 0,
   'Federación Nacional de Cafeteros, precio de referencia publicado el 25-nov-2026 (dato real de mercado): federaciondecafeteros.org',
   'precio interno carga pesos federacion productor caficultor referencia pergamino');

SELECT CLAVE, VALOR, UNIDAD FROM CAFE.PUBLIC.CIFRAS ORDER BY CLAVE;
