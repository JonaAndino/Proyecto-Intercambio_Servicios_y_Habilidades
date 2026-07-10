const mysql = require('mysql2/promise');
require('dotenv').config();

async function run() {
    console.log('Connecting to', process.env.DB_HOST, process.env.DB_DATABASE);
    const pool = mysql.createPool({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_DATABASE,
        connectionLimit: 1
    });

    try {
        const [rows] = await pool.query("SELECT u.id_usuario, u.correo, dur.rol_id, r.nombre_rol FROM Usuarios u LEFT JOIN d_usuarios_roles dur ON u.id_usuario = dur.usuario_id LEFT JOIN Roles r ON dur.rol_id = r.id_rol WHERE u.correo = 'fares@gmail.com'");
        console.log('User role info:', rows);
    } catch (e) {
        console.error('Error fetching role info:', e);
    }

    try {
        const [sp] = await pool.query('SHOW CREATE PROCEDURE GetIdUsuarioByCorreo');
        console.log('SP GetIdUsuarioByCorreo:', sp[0]['Create Procedure']);
    } catch (e) {
        console.error('Error fetching SP:', e);
    }

    pool.end();
}
run();
