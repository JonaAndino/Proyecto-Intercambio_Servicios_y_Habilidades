-- Ignoramos la creación de 'usuarios' y 'roles' porque ya existen en tu sistema actual.
-- Primero eliminamos las tablas si ya se habían creado para forzar esta estructura exacta.
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS d_empresas_usuarios;
DROP TABLE IF EXISTS empresas;
DROP TABLE IF EXISTS t_empresas;
DROP TABLE IF EXISTS d_usuarios_roles;
DROP TABLE IF EXISTS d_roles_opciones;
DROP TABLE IF EXISTS opciones;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Tabla opciones
CREATE TABLE IF NOT EXISTS `opciones` (
  `opcion_id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `link` varchar(500) DEFAULT NULL,
  `orden` int(11) DEFAULT NULL,
  PRIMARY KEY (`opcion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 2. Tabla d_roles_opciones (Apuntando a tu tabla actual 'Roles' usando 'id_rol')
CREATE TABLE IF NOT EXISTS `d_roles_opciones` (
  `d_rol_opcion` int(11) NOT NULL AUTO_INCREMENT,
  `rol_id` int(11) DEFAULT NULL,
  `opcion_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`d_rol_opcion`),
  KEY `d_rores_opciones_fk_roles` (`opcion_id`),
  KEY `d_rores_opciones_fk_1` (`rol_id`),
  CONSTRAINT `d_rores_opciones_fk_1` FOREIGN KEY (`rol_id`) REFERENCES `Roles` (`id_rol`) ON DELETE CASCADE,
  CONSTRAINT `d_rores_opciones_fk_roles` FOREIGN KEY (`opcion_id`) REFERENCES `opciones` (`opcion_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 3. Tabla d_usuarios_roles (Apuntando a tu tabla actual 'Usuarios' usando 'id_usuario')
CREATE TABLE IF NOT EXISTS `d_usuarios_roles` (
  `d_usuario_rol` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) DEFAULT NULL,
  `rol_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`d_usuario_rol`),
  KEY `d_usuarios_roles_fk_usuarios` (`usuario_id`),
  KEY `d_usuarios_roles_fk` (`rol_id`),
  CONSTRAINT `d_usuarios_roles_fk` FOREIGN KEY (`rol_id`) REFERENCES `Roles` (`id_rol`) ON DELETE CASCADE,
  CONSTRAINT `d_usuarios_roles_fk_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `Usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 4. Tabla t_empresas (Requerida por el FK de 'empresas')
CREATE TABLE IF NOT EXISTS `t_empresas` (
  `t_empresa_id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`t_empresa_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- 5. Tabla empresas
CREATE TABLE IF NOT EXISTS `empresas` (
  `empresa_id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rtn` char(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `direccion` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telefono` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `contacto` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t_empresa_id` int(11) DEFAULT NULL,
  `logo` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `correo` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`empresa_id`),
  KEY `empresas_FK` (`t_empresa_id`),
  CONSTRAINT `empresas_FK` FOREIGN KEY (`t_empresa_id`) REFERENCES `t_empresas` (`t_empresa_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- 6. Tabla d_empresas_usuarios (Vista en tu diagrama, conectando empresas y usuarios)
CREATE TABLE IF NOT EXISTS `d_empresas_usuarios` (
  `d_empresa_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `empresa_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`d_empresa_usuario`),
  CONSTRAINT `d_empresas_usuarios_fk_emp` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`empresa_id`) ON DELETE CASCADE,
  CONSTRAINT `d_empresas_usuarios_fk_usu` FOREIGN KEY (`usuario_id`) REFERENCES `Usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- INSERCIONES DE EJEMPLO Y MIGRACIÓN (Para no dejar el sistema vacío)
INSERT IGNORE INTO d_usuarios_roles (usuario_id, rol_id)
SELECT id_usuario, id_rol FROM Usuarios WHERE id_rol IS NOT NULL;

INSERT IGNORE INTO opciones (nombre, link, orden) VALUES 
('Descubrir', 'descubrir', 1),
('Mi perfil', 'perfil', 2),
('Postulaciones', 'ordenesTrabajo', 3),
('Mensajes', 'mensajes', 4),
('Solicitudes de trabajo', 'solicitudesEnviadas', 5),
('Mis favoritos', 'favoritos', 6),
('Historial', 'historial', 7);

-- Asignar opciones al Administrador (rol 1)
INSERT IGNORE INTO d_roles_opciones (rol_id, opcion_id) 
SELECT 1, opcion_id FROM opciones;

-- Asignar opciones al Tecnico (rol 2) y Cliente (rol 3)
INSERT IGNORE INTO d_roles_opciones (rol_id, opcion_id)
SELECT 2, opcion_id FROM opciones;
INSERT IGNORE INTO d_roles_opciones (rol_id, opcion_id)
SELECT 3, opcion_id FROM opciones;
