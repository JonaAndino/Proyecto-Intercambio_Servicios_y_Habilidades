const pool = require('./db');

async function getOpciones() {
    try {
        const [rows] = await pool.query('SELECT * FROM opciones');
        console.log(rows);
        process.exit(0);
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
}
getOpciones();
