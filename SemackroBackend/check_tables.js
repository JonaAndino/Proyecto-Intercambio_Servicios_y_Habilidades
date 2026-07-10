const pool = require('./db');

async function checkTables() {
    try {
        const [rows] = await pool.query('SHOW TABLES');
        console.log("Tablas en la base de datos:");
        console.log(rows);
        process.exit(0);
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
}
checkTables();
