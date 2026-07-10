const pool = require('./db');

async function migrarPermisos() {
    let connection;
    try {
        connection = await pool.getConnection();
        console.log('🔄 Iniciando migración de Permisos a Opciones...');
        
        // 1. Iniciar transacción
        await connection.beginTransaction();

        // 2. Obtener Permisos actuales
        const [permisos] = await connection.query('SELECT * FROM Permisos');
        
        // Mapa para relacionar el viejo id_permiso con el nuevo opcion_id
        const mapPermisos = {};
        let ordenMax = 10; // Empezamos en 10 para que los permisos queden al final del menú si se pintaran

        for (const permiso of permisos) {
            // Revisar si ya existe en opciones para evitar duplicados
            const [existente] = await connection.query('SELECT opcion_id FROM opciones WHERE link = ?', [permiso.clave_permiso]);
            
            let nuevoOpcionId;
            if (existente.length > 0) {
                nuevoOpcionId = existente[0].opcion_id;
            } else {
                // Insertar en opciones
                const [result] = await connection.query(
                    'INSERT INTO opciones (nombre, link, orden) VALUES (?, ?, ?)', 
                    [permiso.nombre_permiso, permiso.clave_permiso, ordenMax++]
                );
                nuevoOpcionId = result.insertId;
            }
            mapPermisos[permiso.id_permiso] = nuevoOpcionId;
        }

        console.log('✅ Permisos migrados a la tabla opciones.');

        // 3. Obtener Roles_Permisos y migrar a d_roles_opciones
        const [rolesPermisos] = await connection.query('SELECT * FROM Roles_Permisos');
        
        for (const rp of rolesPermisos) {
            const nuevoOpcionId = mapPermisos[rp.id_permiso];
            if (nuevoOpcionId) {
                // Insertar usando INSERT IGNORE por si ya existe
                await connection.query(
                    'INSERT IGNORE INTO d_roles_opciones (rol_id, opcion_id) VALUES (?, ?)',
                    [rp.id_rol, nuevoOpcionId]
                );
            }
        }
        
        console.log('✅ Relaciones de roles migradas a d_roles_opciones.');

        // 4. Borrar tablas redundantes
        await connection.query('SET FOREIGN_KEY_CHECKS = 0;');
        await connection.query('DROP TABLE IF EXISTS Roles_Permisos;');
        await connection.query('DROP TABLE IF EXISTS Permisos;');
        await connection.query('SET FOREIGN_KEY_CHECKS = 1;');

        console.log('✅ Tablas Roles_Permisos y Permisos eliminadas (redundancia eliminada).');

        // 5. Confirmar transacción
        await connection.commit();
        console.log('🎉 Migración completada exitosamente.');
        
        process.exit(0);
    } catch (e) {
        if (connection) await connection.rollback();
        console.error('❌ Error durante la migración:', e);
        process.exit(1);
    } finally {
        if (connection) connection.release();
    }
}

migrarPermisos();
