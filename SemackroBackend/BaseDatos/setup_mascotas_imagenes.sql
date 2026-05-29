-- ========================================
-- Script: Soporte para mascotas con imágenes personalizadas
-- ========================================

-- Paso 1: Modificar la columna mascota en Personas para aceptar URLs
SET @columna_existe = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'Personas'
      AND COLUMN_NAME = 'mascota'
);

SET @sql = IF(@columna_existe = 0,
    'ALTER TABLE Personas ADD COLUMN mascota VARCHAR(500) DEFAULT NULL COMMENT "Tipo de mascota (CAT,DOG,...) o URL de imagen personalizada"',
    'ALTER TABLE Personas MODIFY COLUMN mascota VARCHAR(500) DEFAULT NULL COMMENT "Tipo de mascota (CAT,DOG,...) o URL de imagen personalizada"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Paso 2 (Opcional): Crear tabla de mascotas predefinidas para referencia
CREATE TABLE IF NOT EXISTS MascotasPredefinidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    emoji VARCHAR(10) NOT NULL,
    url_imagen VARCHAR(500),
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar mascotas predefinidas
INSERT IGNORE INTO MascotasPredefinidas (tipo, nombre, emoji) VALUES
('CAT', 'Gato Neko', '🐈'),
('DOG', 'Perro Rocky', '🐕'),
('SLIME', 'Slime Bubbles', '🟢'),
('CRAB', 'Cangrejo Sebastián', '🦀'),
('FOX', 'Zorro Foxy', '🦊'),
('FROG', 'Rana Kero', '🐸'),
('DINO', 'Dino Rex', '🦕'),
('GHOST', 'Fantasmita Boo', '👻');

-- Verificar finalización
SELECT 
    'Setup de mascotas con imágenes completado' AS estado,
    COLUMN_NAME, 
    COLUMN_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT, 
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'Personas'
  AND COLUMN_NAME = 'mascota';
