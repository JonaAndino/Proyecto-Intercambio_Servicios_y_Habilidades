const fs = require('fs');
const path = require('path');
const pool = require('./db');

async function ejecutarSQL() {
    try {
        console.log('🔄 Iniciando la creación y actualización de tablas de configuración, roles y motivos...');
        
        // 1. Ejecutar setup_configuraciones_sistema.sql (si no se ha ejecutado)
        const sqlConfigPath = path.join(__dirname, 'BaseDatos', 'setup_configuraciones_sistema.sql');
        if (fs.existsSync(sqlConfigPath)) {
            const sqlConfig = fs.readFileSync(sqlConfigPath, 'utf8');
            await ejecutarSentencias(sqlConfig);
            console.log('✅ Tabla Configuraciones_Sistema y Modalidades listas.');
        }

        // 2. Ejecutar setup_roles_permisos_motivos.sql
        const sqlRolesPath = path.join(__dirname, 'BaseDatos', 'setup_roles_permisos_motivos.sql');
        const sqlRoles = fs.readFileSync(sqlRolesPath, 'utf8');
        await ejecutarSentencias(sqlRoles);
        console.log('✅ Tablas de Roles, Permisos y Motivos de bloqueo listas.');

        console.log('🚀 ¡Configuración de base de datos completada exitosamente!');
        process.exit(0);
    } catch (error) {
        console.error('❌ Error al ejecutar el script de base de datos:', error);
        process.exit(1);
    }
}

async function ejecutarSentencias(sqlText) {
    // Quitar comentarios y saltos raros
    const cleanSql = sqlText.replace(/--.*$/gm, '');
    
    // Separar sentencias por ;
    const sentencias = cleanSql
        .split(';')
        .map(s => s.trim())
        .filter(s => s.length > 0);

    for (let sentencia of sentencias) {
        // Ignorar sentencias DELIMITER y delimitadores complejos de SPs para que node-mysql2 no de error de sintaxis
        if (sentencia.toUpperCase().startsWith('DELIMITER')) continue;
        
        try {
            await pool.query(sentencia);
        } catch (err) {
            // Ignorar errores esperados de ALTER TABLE duplicado
            if (err.code === 'ER_DUP_FIELDNAME' || err.message.includes('Multiple primary key defined')) {
                continue;
            }
            console.warn(`⚠️ Advertencia al ejecutar sentencia: ${err.message}\nSentencia: ${sentencia}`);
        }
    }
}

ejecutarSQL();
