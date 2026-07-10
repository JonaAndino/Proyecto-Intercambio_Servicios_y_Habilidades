const fs = require('fs');
const path = require('path');
const pool = require('./db');

async function ejecutarSQL() {
    try {
        console.log('🔄 Ejecutando setup_esquema_negro.sql...');
        const sqlPath = path.join(__dirname, 'BaseDatos', 'setup_esquema_negro.sql');
        const sqlContent = fs.readFileSync(sqlPath, 'utf8');
        
        const sentencias = sqlContent.split(';').filter(s => s.trim().length > 0);
        for (let sentencia of sentencias) {
            if (sentencia.trim()) {
                await pool.query(sentencia);
            }
        }
        console.log('✅ Base de datos actualizada con las tablas del esquema ejemplo.');
        process.exit(0);
    } catch (error) {
        console.error('❌ Error:', error);
        process.exit(1);
    }
}

ejecutarSQL();
