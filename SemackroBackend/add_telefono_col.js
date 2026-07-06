const db = require('./db');

async function run() {
    try {
        console.log('Intentando agregar la columna telefono_Persona a la tabla Personas...');
        
        // Ejecutamos alter table. Si ya existe, capturamos el error de columna duplicada (código 1060).
        try {
            await db.query(`
                ALTER TABLE Personas ADD COLUMN telefono_Persona VARCHAR(45) NULL;
            `);
            console.log('✅ Columna telefono_Persona agregada exitosamente.');
        } catch (dbErr) {
            if (dbErr.errno === 1060 || dbErr.code === 'ER_DUP_FIELDNAME') {
                console.log('ℹ️ La columna telefono_Persona ya existe en la base de datos.');
            } else {
                throw dbErr;
            }
        }
        
    } catch (err) {
        console.error('❌ Error ejecutando migración:', err);
    } finally {
        process.exit();
    }
}

run();
