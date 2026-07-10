const fs = require('fs');
const path = require('path');
const pool = require('./db');

async function ejecutarSQL() {
    try {
        console.log('🔄 Ejecutando setup_final.sql con la estructura estricta solicitada...');
        const sqlPath = path.join(__dirname, 'BaseDatos', 'setup_final.sql');
        const sqlContent = fs.readFileSync(sqlPath, 'utf8');
        
        // Split por ';' pero evitando cortar dentro de comillas simples si es posible
        // O más fácil: usar statements simples.
        const sentencias = sqlContent.split(';').map(s => s.trim()).filter(s => s.length > 0);
        
        for (let sentencia of sentencias) {
            // Ignorar los comentarios puramente al inicio
            if (sentencia.startsWith('--')) {
                // Remove line comment
                sentencia = sentencia.replace(/^--.*$/gm, '').trim();
            }
            if (sentencia.length > 0) {
                await pool.query(sentencia);
            }
        }
        console.log('✅ Base de datos actualizada con TODAS las tablas (incluyendo empresas y t_empresas).');
        process.exit(0);
    } catch (error) {
        console.error('❌ Error:', error);
        process.exit(1);
    }
}

ejecutarSQL();
