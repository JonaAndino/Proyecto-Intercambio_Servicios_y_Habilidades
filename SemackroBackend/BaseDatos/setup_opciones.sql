CREATE TABLE IF NOT EXISTS Opciones_Menu (
    id_opcion INT AUTO_INCREMENT PRIMARY KEY,
    nombre_opcion VARCHAR(100) NOT NULL,
    link VARCHAR(255) NOT NULL UNIQUE,
    icono VARCHAR(255),
    orden INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Roles_Opciones (
    id_rol INT,
    id_opcion INT,
    PRIMARY KEY (id_rol, id_opcion),
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_opcion) REFERENCES Opciones_Menu(id_opcion) ON DELETE CASCADE
);

-- Insertar opciones basicas
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Descubrir', 'descubrir', 'mdi:compass-outline', 1);
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Mi perfil', 'perfil', 'mdi:account-outline', 2);
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Postulaciones', 'ordenesTrabajo', 'mdi:clipboard-list-outline', 3);
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Mensajes', 'mensajes', 'mdi:message-outline', 4);
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Solicitudes de trabajo', 'solicitudesEnviadas', 'mdi:file-send-outline', 5);
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Mis favoritos', 'favoritos', 'ph:heart-bold', 6);
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Historial', 'historial', 'mdi:history', 7);
INSERT IGNORE INTO Opciones_Menu (nombre_opcion, link, icono, orden) VALUES ('Reportes', 'reportes', 'mdi:chart-bar', 8);

-- Administrador (rol 1)
INSERT IGNORE INTO Roles_Opciones (id_rol, id_opcion) SELECT 1, id_opcion FROM Opciones_Menu;

-- Tecnico (rol 2)
INSERT IGNORE INTO Roles_Opciones (id_rol, id_opcion) SELECT 2, id_opcion FROM Opciones_Menu WHERE link != 'reportes';

-- Cliente (rol 3)
INSERT IGNORE INTO Roles_Opciones (id_rol, id_opcion) SELECT 3, id_opcion FROM Opciones_Menu WHERE link != 'reportes';
