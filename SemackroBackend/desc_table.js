const db = require('./db.js');

async function check() {
    try {
        const [rows] = await db.execute("DESCRIBE d_roles_opciones");
        console.log(rows);
        process.exit(0);
    } catch(e) {
        console.error(e);
        process.exit(1);
    }
}
check();
