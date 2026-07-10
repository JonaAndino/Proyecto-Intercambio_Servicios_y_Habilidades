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
    SELECT r.id_rol, r.nombre_rol, r.descripcion_rol, r.es_default,
           GROUP_CONCAT(o.link) as permisos_lista
    FROM Roles r
    LEFT JOIN d_roles_opciones ro ON r.id_rol = ro.rol_id
    LEFT JOIN opciones o ON ro.opcion_id = o.opcion_id
    GROUP BY r.id_rol
  `);
  
  const roles = rows.map(r => ({
      id_rol: r.id_rol,
      nombre_rol: r.nombre_rol,
      descripcion_rol: r.descripcion_rol,
      es_default: r.es_default === 1,
      permisos: r.permisos_lista ? r.permisos_lista.split(',') : []
  }));
  
  console.log('Roles from API logic:', JSON.stringify(roles, null, 2));
  
  db.end();
}
run().catch(console.error);
