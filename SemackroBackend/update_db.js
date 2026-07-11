const mysql = require('mysql2/promise');
mysql.createConnection({
    host: '104.155.156.171',
    user: 'usuario1',
    password: 'equipo2',
    database: 'SkillConnect2025',
    port: 3306
}).then(async c => {
    try {
        await c.query("UPDATE opciones SET nombre = 'Panel de administración' WHERE link = 'VER_METRICAS'");
        await c.query("DELETE FROM d_roles_opciones WHERE opcion_id = (SELECT opcion_id FROM opciones WHERE link = 'reportes')");
        await c.query("DELETE FROM d_usuarios_opciones WHERE opcion_id = (SELECT opcion_id FROM opciones WHERE link = 'reportes')");
        await c.query("DELETE FROM opciones WHERE link = 'reportes'");
        console.log('Successfully updated DB');
    } catch(e) {
        console.error(e);
    }
    process.exit(0);
});
