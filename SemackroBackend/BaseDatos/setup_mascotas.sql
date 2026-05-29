-- ========================================
-- SCRIPT: Añadir columna de mascota a la tabla Personas
-- ========================================

-- Primero, verificar si la columna ya existe para evitar errores
SET @columna_existe = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'Personas'
      AND COLUMN_NAME = 'mascota'
);

SET @sql = IF(@columna_existe = 0,
    'ALTER TABLE Personas ADD COLUMN mascota VARCHAR(50) DEFAULT NULL COMMENT "Tipo de mascota seleccionada por el usuario: CAT, DOG, SLIME, CRAB, FOX, FROG, DINO, GHOST"',
    'SELECT "Columna mascota ya existe en la tabla Personas" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar el resultado
SELECT 
    'Configuración de mascotas completada' AS estado,
    COLUMN_NAME, 
    COLUMN_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT, 
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'Personas'
  AND COLUMN_NAME = 'mascota';
