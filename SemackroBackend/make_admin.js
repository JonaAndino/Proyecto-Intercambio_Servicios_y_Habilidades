const pool = require('./db');

async function makeAdmin() {
    try {
        console.log('🔄 Otorgando permisos de Administrador a fares@gmail.com...');
        
        // Buscar ID del usuario por correo
        const [users] = await pool.query("SELECT id_usuario FROM Usuarios WHERE correo = 'fares@gmail.com'");
        if (users.length === 0) {
            console.log('❌ No se encontró un usuario con el correo fares@gmail.com');
            process.exit(1);
        }

        const uid = users[0].id_usuario;
        console.log(`✅ Usuario encontrado (ID: ${uid})`);

        // Verificar si el usuario existe en d_usuarios_roles
        const [rows] = await pool.query('SELECT d_usuario_rol FROM d_usuarios_roles WHERE usuario_id = ?', [uid]);
        if (rows.length > 0) {
            await pool.query('UPDATE d_usuarios_roles SET rol_id = 1 WHERE usuario_id = ?', [uid]);
            console.log('✅ Rol de Administrador actualizado (rol_id = 1).');
        } else {
            await pool.query('INSERT INTO d_usuarios_roles (usuario_id, rol_id) VALUES (?, 1)', [uid]);
            console.log('✅ Rol de Administrador insertado (rol_id = 1).');
        }

        console.log('✅ ¡Permisos de Administrador restaurados en la base de datos!');
        process.exit(0);
    } catch (e) {
        console.error('❌ Error:', e);
        process.exit(1);
    }
}
makeAdmin();
