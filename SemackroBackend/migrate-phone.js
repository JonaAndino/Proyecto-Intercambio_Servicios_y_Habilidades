const pool = require('./db');

async function migrate() {
    try {
        console.log('Iniciando migración: Agregar columna telefono_Persona a la tabla Personas...');
        
        // Ejecutar ALTER TABLE
        await pool.query('ALTER TABLE Personas ADD COLUMN telefono_Persona VARCHAR(20) NULL')
            .then(() => {
                console.log('✓ Columna telefono_Persona agregada exitosamente.');
            })
            .catch(err => {
                if (err.code === 'ER_DUP_COLUMN_NAME') {
                    console.log('ℹ La columna telefono_Persona ya existe en la tabla Personas.');
                } else {
                    throw err;
                }
            });

        console.log('Migración completada con éxito.');
        process.exit(0);
    } catch (e) {
        console.error('Error durante la migración:', e);
        process.exit(1);
    }
}

migrate();
