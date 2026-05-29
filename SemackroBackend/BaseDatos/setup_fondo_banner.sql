-- ========================================
-- Script: Soporte para URL de fondo del banner de la tarjeta
-- ========================================

-- Paso 1: Agregar la columna url_fondo_banner en Personas
SET @columna_existe = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'Personas'
      AND COLUMN_NAME = 'url_fondo_banner'
);

SET @sql = IF(@columna_existe = 0,
    'ALTER TABLE Personas ADD COLUMN url_fondo_banner VARCHAR(500) DEFAULT NULL COMMENT "URL de la imagen de fondo del banner de la tarjeta"',
    'SELECT "Columna url_fondo_banner ya existe en Personas" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar finalización
SELECT 
    'Setup de fondo del banner completado' AS estado,
    COLUMN_NAME, 
    COLUMN_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT, 
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'Personas'
  AND COLUMN_NAME = 'url_fondo_banner';
