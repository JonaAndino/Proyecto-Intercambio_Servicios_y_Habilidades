CREATE TABLE IF NOT EXISTS empresas (
    empresa_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    rtn VARCHAR(100),
    direccion TEXT,
    telefono VARCHAR(50),
    contacto VARCHAR(150),
    t_empresa_id INT,
    logo VARCHAR(255),
    correo VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS d_empresas_usuarios (
    d_empresa_usuario INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    usuario_id INT,
    FOREIGN KEY (empresa_id) REFERENCES empresas(empresa_id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
);
