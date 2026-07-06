const pool = require('./db');

async function checkSchema() {
    try {
        console.log('--- DESCRIBE Usuarios ---');
        const [usuariosCols] = await pool.query('DESCRIBE Usuarios');
        console.table(usuariosCols);

        console.log('--- DESCRIBE Personas ---');
        const [personasCols] = await pool.query('DESCRIBE Personas');
        console.table(personasCols);

        console.log('--- Roles en la Base de Datos ---');
        const [roles] = await pool.query('SELECT * FROM Roles').catch(() => [[]]);
        console.table(roles);

        process.exit(0);
    } catch (e) {
        console.error('Error describiendo tablas:', e);
        process.exit(1);
    }
}

checkSchema();
