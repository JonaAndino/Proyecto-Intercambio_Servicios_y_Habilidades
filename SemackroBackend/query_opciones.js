const mysql = require('mysql2/promise');

async function checkDb() {
  const connection = await mysql.createConnection({
    host: '104.155.156.171',
    user: 'usuario1',
    password: 'equipo2',
    database: 'SkillConnect2025'
  });
  
  try {
    const [rows] = await connection.execute('SELECT link, nombre FROM opciones WHERE link LIKE "%modalidad%" OR link LIKE "%categoria%" OR link LIKE "%variab%" OR link LIKE "%motiv%" OR link LIKE "%roles%" OR link LIKE "%config%"');
    console.log("Opciones:", rows);
  } catch (error) {
    console.error("Query Error:", error);
  }
  
  await connection.end();
}

checkDb();
