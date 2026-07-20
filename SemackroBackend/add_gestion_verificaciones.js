const db = require('./db.js');

async function up() {
    try {
        await db.execute("INSERT INTO opciones (link, nombre) VALUES ('GESTIONAR_VERIFICACIONES', 'Aprobar o rechazar verificaciones') ON DUPLICATE KEY UPDATE nombre='Aprobar o rechazar verificaciones'");
        
        const [opcionRows] = await db.execute("SELECT opcion_id FROM opciones WHERE link = 'GESTIONAR_VERIFICACIONES'");
        if (opcionRows.length > 0) {
            const opcionId = opcionRows[0].opcion_id;
            const [rows] = await db.execute("SELECT * FROM d_roles_opciones WHERE rol_id = 1 AND opcion_id = ?", [opcionId]);
            if (rows.length === 0) {
                await db.execute("INSERT INTO d_roles_opciones (rol_id, opcion_id) VALUES (1, ?)", [opcionId]);
            }
        }
        
        console.log('Permission added');
        process.exit(0);
    } catch(e) {
        console.error(e);
        process.exit(1);
    }
}
up();
