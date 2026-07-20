const db = require('./db.js');

async function up() {
    try {
        await db.execute("INSERT INTO opciones (link, nombre) VALUES ('VER_REPORTES_USUARIOS', 'Ver tabla de usuarios reportados') ON DUPLICATE KEY UPDATE nombre='Ver tabla de usuarios reportados'");
        
        // Asignarlo al administrador por defecto
        const [rows] = await db.execute("SELECT * FROM roles_opciones WHERE id_rol = 1 AND link = 'VER_REPORTES_USUARIOS'");
        if (rows.length === 0) {
            await db.execute("INSERT INTO roles_opciones (id_rol, link) VALUES (1, 'VER_REPORTES_USUARIOS')");
        }
        
        console.log('Permission added');
        process.exit(0);
    } catch(e) {
        console.error(e);
        process.exit(1);
    }
}
up();
