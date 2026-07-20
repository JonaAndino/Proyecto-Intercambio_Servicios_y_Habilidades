const mysql = require('mysql2/promise');

async function checkDb() {
  const connection = await mysql.createConnection({
    host: '104.155.156.171',
    user: 'usuario1',
    password: 'equipo2',
    database: 'SkillConnect2025'
  });
  
  try {
    const [rows] = await connection.execute('DESCRIBE opciones');
    console.log("Rows:", rows);
    const [rows2] = await connection.execute('SELECT * FROM opciones WHERE clave_opcion LIKE "%HISTORIAL%"');
    console.log("Rows2:", rows2);
  } catch (error) {
    console.error("Query Error:", error);
  }
  
  await connection.end();
}

checkDb();
