const mysql = require('mysql2/promise');
require('dotenv').config({ path: '.env' });

async function checkConfig() {
    try {
        const connection = await mysql.createConnection({
            host: process.env.DB_HOST || '104.155.156.171',
            user: process.env.DB_USER || 'usuario1',
            password: process.env.DB_PASSWORD || 'equipo2',
            database: process.env.DB_DATABASE || 'SkillConnect2025',
            port: process.env.DB_PORT || 3306
        });

        const [rows] = await connection.execute('SELECT * FROM Configuraciones_Sistema;');
        console.log("Configuraciones_Sistema:");
        console.log(rows);
        
        await connection.end();
    } catch (e) {
        console.error(e);
    }
}
checkConfig();
