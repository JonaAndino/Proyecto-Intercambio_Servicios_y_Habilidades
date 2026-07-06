-- ========================================
-- SCRIPT SQL PARA CONFIGURACIONES DEL SISTEMA
-- Ejecutar en la base de datos SEMACKRO2025
-- ========================================

-- 1. Tabla de Configuraciones Generales del Sistema
CREATE TABLE IF NOT EXISTS Configuraciones_Sistema (
    id_configuracion BIGINT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    tipo VARCHAR(50) DEFAULT 'string', -- string, number, boolean, json
    descripcion TEXT,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Tabla de Modalidades de Intercambio (virtual, presencial, etc.)
CREATE TABLE IF NOT EXISTS Modalidades_Intercambio (
    id_modalidad BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    activo TINYINT DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Datos iniciales por defecto
INSERT IGNORE INTO Configuraciones_Sistema (clave, valor, tipo, descripcion) VALUES 
('jwt_reset_password_duration', '3600', 'number', 'Duración en segundos del token JWT para restablecer contraseña'),
('driver_perfil_activado', '1', 'boolean', 'Activar/desactivar el driver en el perfil de usuario'),
('driver_descubrir_activado', '1', 'boolean', 'Activar/desactivar el driver en la página de descubrir');

INSERT IGNORE INTO Modalidades_Intercambio (nombre, activo) VALUES 
('Virtual', 1),
('Presencial', 1);

-- ========================================
-- STORED PROCEDURES
-- ========================================

-- SP: Obtener todas las configuraciones
DELIMITER //
DROP PROCEDURE IF EXISTS sp_obtener_configuraciones //
CREATE PROCEDURE sp_obtener_configuraciones()
BEGIN
    SELECT clave, valor, tipo, descripcion FROM Configuraciones_Sistema;
END //
DELIMITER ;

-- SP: Actualizar una configuración
DELIMITER //
DROP PROCEDURE IF EXISTS sp_actualizar_configuracion //
CREATE PROCEDURE sp_actualizar_configuracion(
    IN p_clave VARCHAR(100),
    IN p_valor TEXT
)
BEGIN
    INSERT INTO Configuraciones_Sistema (clave, valor)
    VALUES (p_clave, p_valor)
    ON DUPLICATE KEY UPDATE valor = p_valor;
END //
DELIMITER ;

-- SP: Obtener todas las modalidades
DELIMITER //
DROP PROCEDURE IF EXISTS sp_obtener_modalidades //
CREATE PROCEDURE sp_obtener_modalidades()
BEGIN
    SELECT id_modalidad, nombre, activo FROM Modalidades_Intercambio;
END //
DELIMITER ;

-- SP: Agregar una modalidad
DELIMITER //
DROP PROCEDURE IF EXISTS sp_agregar_modalidad //
CREATE PROCEDURE sp_agregar_modalidad(
    IN p_nombre VARCHAR(100)
)
BEGIN
    INSERT INTO Modalidades_Intercambio (nombre) VALUES (p_nombre);
END //
DELIMITER ;

-- SP: Actualizar una modalidad
DELIMITER //
DROP PROCEDURE IF EXISTS sp_actualizar_modalidad //
CREATE PROCEDURE sp_actualizar_modalidad(
    IN p_id_modalidad BIGINT,
    IN p_nombre VARCHAR(100),
    IN p_activo TINYINT
)
BEGIN
    UPDATE Modalidades_Intercambio
    SET nombre = p_nombre, activo = p_activo
    WHERE id_modalidad = p_id_modalidad;
END //
DELIMITER ;

-- SP: Eliminar una modalidad
DELIMITER //
DROP PROCEDURE IF EXISTS sp_eliminar_modalidad //
CREATE PROCEDURE sp_eliminar_modalidad(
    IN p_id_modalidad BIGINT
)
BEGIN
    DELETE FROM Modalidades_Intercambio WHERE id_modalidad = p_id_modalidad;
END //
DELIMITER ;
