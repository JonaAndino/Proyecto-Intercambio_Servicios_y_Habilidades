-- ========================================
-- Script simple para agregar columna url_fondo_banner
-- ========================================

-- Agregar la columna (si no existe, no se hará nada en MySQL 8.0+)
ALTER TABLE Personas 
ADD COLUMN IF NOT EXISTS url_fondo_banner VARCHAR(500) DEFAULT NULL 
COMMENT 'URL de la imagen de fondo del banner';

-- Verificar que se agregó correctamente
SHOW COLUMNS FROM Personas LIKE 'url_fondo_banner';
