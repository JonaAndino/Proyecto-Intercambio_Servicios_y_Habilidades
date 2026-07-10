const pool = require('./db');

async function dropRedundancy() {
    try {
        console.log('🔄 Buscando nombre de Foreign Key en Usuarios para id_rol...');
        const [rows] = await pool.query(`
            SELECT CONSTRAINT_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = 'SkillConnect2025' 
              AND TABLE_NAME = 'Usuarios' 
              AND COLUMN_NAME = 'id_rol'
              AND REFERENCED_TABLE_NAME IS NOT NULL
        `);
        
        if (rows.length > 0) {
            const fkName = rows[0].CONSTRAINT_NAME;
            console.log('Encontrado FK:', fkName, '- Procediendo a eliminarlo...');
            await pool.query(`ALTER TABLE Usuarios DROP FOREIGN KEY ${fkName}`);
        } else {
            console.log('No se encontró FK explícito para id_rol en Usuarios.');
        }

        console.log('🔄 Eliminando columnas id_rol y rol de la tabla Usuarios...');
        
        // Es posible que id_rol tenga un índice que necesite ser borrado también.
        try {
            await pool.query('ALTER TABLE Usuarios DROP COLUMN id_rol, DROP COLUMN rol');
            console.log('✅ Columnas id_rol y rol eliminadas.');
        } catch (colErr) {
            console.log('Intento fallido de borrar columna, probablemente por un index. Buscando índice...');
            const [indexRows] = await pool.query(`
                SHOW INDEX FROM Usuarios WHERE Column_name = 'id_rol'
            `);
            if (indexRows.length > 0) {
                const indexName = indexRows[0].Key_name;
                console.log('Borrando índice:', indexName);
                await pool.query(`ALTER TABLE Usuarios DROP INDEX ${indexName}`);
                await pool.query('ALTER TABLE Usuarios DROP COLUMN id_rol, DROP COLUMN rol');
                console.log('✅ Columnas eliminadas después de borrar el índice.');
            } else {
                throw colErr;
            }
        }
        
        process.exit(0);
    } catch (e) {
        console.error('❌ Error:', e);
        process.exit(1);
    }
}
dropRedundancy();
