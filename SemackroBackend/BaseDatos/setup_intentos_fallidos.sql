-- ==============================================
-- Agregar columnas para intentos fallidos y bloqueo de cuenta
-- ==============================================

ALTER TABLE Usuarios 
ADD COLUMN intentos_fallidos INT DEFAULT 0,
ADD COLUMN bloqueado_hasta DATETIME DEFAULT NULL;
