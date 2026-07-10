const pool = require('./db');

async function createTable() {
    try {
        console.log('🔄 Creando tabla d_usuarios_opciones...');
        await pool.query(`
            CREATE TABLE IF NOT EXISTS d_usuarios_opciones (
                usuario_id INT,
                opcion_id INT,
                concedido BOOLEAN,
                PRIMARY KEY (usuario_id, opcion_id),
                FOREIGN KEY (usuario_id) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE,
                FOREIGN KEY (opcion_id) REFERENCES opciones(opcion_id) ON DELETE CASCADE
            )
        `);
        console.log('✅ Tabla d_usuarios_opciones creada con éxito.');
    } catch (error) {
        console.error('❌ Error creando tabla d_usuarios_opciones:', error);
    } finally {
        pool.end();
    }
}

createTable();
