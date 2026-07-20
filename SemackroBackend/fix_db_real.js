const mysql = require('mysql2/promise');

async function updateDb() {
  const connection = await mysql.createConnection({
    host: '104.155.156.171',
    user: 'usuario1',
    password: 'equipo2',
    database: 'SkillConnect2025'
  });
  
  try {
    const [result] = await connection.execute('UPDATE opciones SET link = "VER_POSTULACIONES_GLOBALES" WHERE link = "VER_HISTORIAL_PERSONAL"');
    console.log("Database update result:", result.affectedRows, "rows affected");
  } catch (error) {
    console.error("Query Error:", error);
  }
  
  await connection.end();
}

updateDb();
