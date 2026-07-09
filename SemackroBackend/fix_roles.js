const pool = require('./db');

async function fixRolesTable() {
    try {
        console.log('Modifying Roles table...');
        await pool.execute('ALTER TABLE Roles MODIFY id_rol INT AUTO_INCREMENT');
        console.log('Successfully altered Roles table.');
    } catch (err) {
        console.error('Error modifying Roles table:', err.message);
    } finally {
        process.exit();
    }
}

fixRolesTable();
