const mysql = require('mysql2/promise');
require('dotenv').config({path: './.env'});
async function run() {
  const db = await mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
    port: process.env.DB_PORT || 3306
  });
  
  const [rows] = await db.query(`
    SELECT u.id_usuario, u.correo, p.nombre_Persona, ur.rol_id, r.nombre_rol
    FROM Usuarios u
    LEFT JOIN Personas p ON p.id_Usuario = u.id_usuario
    LEFT JOIN d_usuarios_roles ur ON u.id_usuario = ur.usuario_id
    LEFT JOIN Roles r ON ur.rol_id = r.id_rol
    WHERE p.nombre_Persona LIKE '%Eli%' OR p.nombre_Persona LIKE '%Juanito%' OR p.nombre_Persona LIKE '%Moreira%'
  `);
  console.log('Eli/Juanito query result:', rows);
  
  db.end();
}
run().catch(console.error);
