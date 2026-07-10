const fs = require('fs');
const path = require('path');
const pool = require('./db');

async function ejecutarSQL() {
    try {
        console.log('🔄 Ejecutando setup_opciones.sql...');
        const sqlPath = path.join(__dirname, 'BaseDatos', 'setup_opciones.sql');
        const sqlContent = fs.readFileSync(sqlPath, 'utf8');
        
        const sentencias = sqlContent.split(';').filter(s => s.trim().length > 0);
        for (let sentencia of sentencias) {
            if (sentencia.trim()) {
                await pool.query(sentencia);
            }
        }
        console.log('✅ Opciones de menú creadas y asignadas.');
        process.exit(0);
    } catch (error) {
        console.error('❌ Error:', error);
        process.exit(1);
    }
}

ejecutarSQL();
