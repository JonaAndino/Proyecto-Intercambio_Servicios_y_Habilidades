-- =========================================================
-- SCRIPT SQL PARA ROLES, PERMISOS Y MOTIVOS DE BLOQUEO
-- Ejecutar en la base de datos SkillConnect2025/SEMACKRO2025
-- =========================================================

-- 1. Tabla de Permisos del Sistema
CREATE TABLE IF NOT EXISTS Permisos (
    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    clave_permiso VARCHAR(50) NOT NULL UNIQUE,
    nombre_permiso VARCHAR(100) NOT NULL
);

-- 2. Insertar los permisos base del sistema
INSERT IGNORE INTO Permisos (id_permiso, clave_permiso, nombre_permiso) VALUES
(1, 'VER_METRICAS', 'Panel de administración'),
(2, 'MODERAR_USUARIOS', 'Bloquear y moderar usuarios de la comunidad'),
(3, 'GESTIONAR_CONFIGURACION', 'Editar configuraciones y tablas maestras'),
(4, 'ACEPTAR_INTERCAMBIOS', 'Solicitar y concretar intercambios de habilidades'),
(5, 'VER_HISTORIAL_PERSONAL', 'Visualizar historial de trabajos personales'),
(6, 'VER_DIRECTORIO', 'Ver listado y tabla del directorio general'),
(7, 'CREAR_CUENTAS', 'Crear y enrolar nuevas cuentas de usuario'),
(8, 'EDITAR_USUARIOS', 'Editar perfiles y datos de usuarios'),
(9, 'ASIGNAR_ROLES_PERMISOS', 'Asignar roles y dar permisos a los usuarios'),
(10, 'VER_SOLICITUDES_VERIFICACION', 'Cola de validadores para identidad y certificaciones');

-- 3. Tabla de Relación de Roles y Permisos (Muchos a Muchos)
CREATE TABLE IF NOT EXISTS Roles_Permisos (
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES Permisos(id_permiso) ON DELETE CASCADE
);

-- 4. Modificar la tabla Roles para añadir descripción y es_default si no existen
ALTER TABLE Roles ADD COLUMN IF NOT EXISTS descripcion_rol VARCHAR(255) DEFAULT NULL;
ALTER TABLE Roles ADD COLUMN IF NOT EXISTS es_default TINYINT(1) DEFAULT 0;

-- 5. Actualizar los roles base
UPDATE Roles SET descripcion_rol = 'Acceso total a la administración, reportes, métricas y configuraciones globales.', es_default = 1 WHERE id_rol = 1;
UPDATE Roles SET descripcion_rol = 'Usuario general de la plataforma con derecho a intercambios y vistas personales.', es_default = 1 WHERE id_rol = 2;

-- 6. Insertar permisos iniciales para los roles por defecto
-- Administrador (id_rol = 1) -> Obtiene todos los permisos
INSERT IGNORE INTO Roles_Permisos (id_rol, id_permiso)
SELECT 1, id_permiso FROM Permisos;

-- Usuario Estandar (id_rol = 2) -> Aceptar intercambios e historial de trabajos
INSERT IGNORE INTO Roles_Permisos (id_rol, id_permiso)
SELECT 2, id_permiso FROM Permisos WHERE clave_permiso IN ('ACEPTAR_INTERCAMBIOS', 'VER_HISTORIAL_PERSONAL');

-- 7. Tabla de Motivos de Bloqueo Predefinidos
CREATE TABLE IF NOT EXISTS Motivos_Bloqueo_Predefinidos (
    id_motivo INT AUTO_INCREMENT PRIMARY KEY,
    motivo TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Insertar motivos iniciales
INSERT IGNORE INTO Motivos_Bloqueo_Predefinidos (id_motivo, motivo) VALUES
(1, 'Usted no se apegó a las reglas de la plataforma'),
(2, 'Comportamiento indebido o lenguaje ofensivo en la comunidad.'),
(3, 'Múltiples reportes de usuarios por incumplimiento en los intercambios pactados.');
