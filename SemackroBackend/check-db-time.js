
const pool = require('./db.js');

async function checkDB() {
    try {
        const [rows] = await pool.query('SELECT id_usuario, en_linea, ultima_conexion, NOW() AS db_now FROM Usuarios LIMIT 5');
        console.log('Usuarios table sample:');
        console.table(rows);
        
        console.log('\nChecking type of ultima_conexion:');
        rows.forEach(row => {
            console.log(`ID ${row.id_usuario} - ultima_conexion:`, row.ultima_conexion, '- tipo:', typeof row.ultima_conexion, '- instanceof Date:', row.ultima_conexion instanceof Date);
        });
        
        process.exit(0);
    } catch (err) {
        console.error(err);
        process.exit(1);
    }
}

checkDB();
