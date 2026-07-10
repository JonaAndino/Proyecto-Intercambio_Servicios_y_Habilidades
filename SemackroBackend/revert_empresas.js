const pool = require('./db');

async function revertirEmpresas() {
    try {
        console.log('🔄 Eliminando tablas de empresas no deseadas...');
        await pool.query('SET FOREIGN_KEY_CHECKS = 0;');
        await pool.query('DROP TABLE IF EXISTS d_empresas_usuarios;');
        await pool.query('DROP TABLE IF EXISTS empresas;');
        await pool.query('DROP TABLE IF EXISTS t_empresas;');
        await pool.query('SET FOREIGN_KEY_CHECKS = 1;');
        console.log('✅ Tablas de empresas eliminadas exitosamente.');
        process.exit(0);
    } catch (e) {
        console.error('❌ Error al eliminar tablas:', e);
        process.exit(1);
    }
}
revertirEmpresas();
