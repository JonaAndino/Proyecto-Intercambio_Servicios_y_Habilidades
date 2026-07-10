const pool = require('./db');

async function checkFares() {
    try {
        const [rows] = await pool.query(`
            SELECT u.id_usuario, u.correo, ur.rol_id 
            FROM Usuarios u
            LEFT JOIN d_usuarios_roles ur ON u.id_usuario = ur.usuario_id
            WHERE u.correo = 'fares@gmail.com'
        `);
        console.log(rows);
        process.exit(0);
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
}
checkFares();
