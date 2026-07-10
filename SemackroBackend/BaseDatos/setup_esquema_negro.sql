-- Eliminar las tablas creadas en el paso anterior si existen
DROP TABLE IF EXISTS Roles_Opciones;
DROP TABLE IF EXISTS Opciones_Menu;

-- Crear las tablas exactas del esquema (fondo negro)
CREATE TABLE IF NOT EXISTS opciones (
    opcion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    link VARCHAR(255) NOT NULL UNIQUE,
    orden INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS d_roles_opciones (
    d_rol_opcion INT AUTO_INCREMENT PRIMARY KEY,
    rol_id INT,
    opcion_id INT,
    FOREIGN KEY (rol_id) REFERENCES Roles(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (opcion_id) REFERENCES opciones(opcion_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS d_usuarios_roles (
    d_usuario_rol INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    rol_id INT,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (rol_id) REFERENCES Roles(id_rol) ON DELETE CASCADE
);

-- Migrar usuarios existentes a la nueva tabla d_usuarios_roles
INSERT IGNORE INTO d_usuarios_roles (usuario_id, rol_id)
SELECT id_usuario, id_rol FROM Usuarios WHERE id_rol IS NOT NULL;

-- Insertar opciones basicas en la nueva tabla 'opciones'
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Descubrir', 'descubrir', 1);
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Mi perfil', 'perfil', 2);
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Postulaciones', 'ordenesTrabajo', 3);
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Mensajes', 'mensajes', 4);
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Solicitudes de trabajo', 'solicitudesEnviadas', 5);
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Mis favoritos', 'favoritos', 6);
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Historial', 'historial', 7);
INSERT IGNORE INTO opciones (nombre, link, orden) VALUES ('Reportes', 'reportes', 8);

-- Asignar opciones al Administrador (rol 1)
INSERT IGNORE INTO d_roles_opciones (rol_id, opcion_id) 
SELECT 1, opcion_id FROM opciones;

-- Asignar opciones al Tecnico (rol 2)
INSERT IGNORE INTO d_roles_opciones (rol_id, opcion_id) 
SELECT 2, opcion_id FROM opciones WHERE link != 'reportes';

-- Asignar opciones al Cliente (rol 3)
INSERT IGNORE INTO d_roles_opciones (rol_id, opcion_id) 
SELECT 3, opcion_id FROM opciones WHERE link != 'reportes';
