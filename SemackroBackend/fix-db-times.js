
const pool = require('./db.js');

function formatLocalDateTime(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

async function fixDB() {
    try {
        console.log('Fixing ultima_conexion in Usuarios table...');
        
        // Let's set ultima_conexion to current local time for testing
        const nowLocal = new Date();
        const formattedNow = formatLocalDateTime(nowLocal);
        console.log('Now local (object):', nowLocal);
        console.log('Now local (formatted string):', formattedNow);
        
        const [result] = await pool.query('UPDATE Usuarios SET ultima_conexion = ? WHERE ultima_conexion IS NOT NULL', [formattedNow]);
        
        console.log('Updated rows:', result.affectedRows);
        
        console.log('\nChecking results:');
        const [rows] = await pool.query('SELECT id_usuario, en_linea, ultima_conexion, NOW() AS db_now FROM Usuarios LIMIT 10');
        console.table(rows);
        
        process.exit(0);
    } catch (err) {
        console.error(err);
        process.exit(1);
    }
}

fixDB();
