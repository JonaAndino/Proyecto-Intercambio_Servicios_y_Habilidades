const db = require('./db');

async function run() {
    try {
        console.log('Intentando agregar la columna perfil_publico_Persona a la tabla Personas...');

        // Por defecto el perfil es privado (0). El usuario puede cambiarlo a público (1) desde su perfil.
        try {
            await db.query(`
                ALTER TABLE Personas ADD COLUMN perfil_publico_Persona TINYINT(1) NOT NULL DEFAULT 0;
            `);
            console.log('✅ Columna perfil_publico_Persona agregada exitosamente (por defecto: privado).');
        } catch (dbErr) {
            if (dbErr.errno === 1060 || dbErr.code === 'ER_DUP_FIELDNAME') {
                console.log('ℹ️ La columna perfil_publico_Persona ya existe en la base de datos.');
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
