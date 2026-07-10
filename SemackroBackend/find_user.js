const pool = require('./db');
async function seeUsers() {
    try {
        const [rows] = await pool.query('SELECT id_usuario, nombre, correo FROM Usuarios LIMIT 10');
        console.log(rows);
        process.exit(0);
    } catch(e) {
        console.error(e);
        process.exit(1);
    }
}
seeUsers();
