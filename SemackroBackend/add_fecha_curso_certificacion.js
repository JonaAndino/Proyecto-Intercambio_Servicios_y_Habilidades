const db = require('./db');

async function run() {
    try {
        console.log('Intentando agregar la columna fecha_curso a la tabla Certificaciones...');

        try {
            await db.query(`
                ALTER TABLE Certificaciones ADD COLUMN fecha_curso DATE NULL;
            `);
            console.log('✅ Columna fecha_curso agregada exitosamente.');
        } catch (dbErr) {
            if (dbErr.errno === 1060 || dbErr.code === 'ER_DUP_FIELDNAME') {
                console.log('ℹ️ La columna fecha_curso ya existe en la base de datos.');
            } else {
                throw dbErr;
            }
        }

        console.log('Actualizando el stored procedure sp_insertar_certificacion para incluir fecha_curso...');

        await db.query(`DROP PROCEDURE IF EXISTS sp_insertar_certificacion;`);

        await db.query(`
            CREATE PROCEDURE sp_insertar_certificacion(
                IN p_id_persona BIGINT,
                IN p_titulo VARCHAR(255),
                IN p_institucion VARCHAR(255),
                IN p_url TEXT,
                IN p_fecha_curso DATE
            )
            BEGIN
                INSERT INTO Certificaciones (id_Perfil_Persona, titulo_certificacion, institucion, url_certificado, fecha_curso)
                VALUES (p_id_persona, p_titulo, p_institucion, p_url, p_fecha_curso);
            END
        `);

        console.log('✅ Stored procedure sp_insertar_certificacion actualizado exitosamente.');

    } catch (err) {
        console.error('❌ Error ejecutando migración:', err);
    } finally {
        process.exit();
    }
}

run();
