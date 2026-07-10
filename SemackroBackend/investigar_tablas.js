const pool = require('./db');

async function investigarRedundancia() {
    try {
        console.log("--- PERMISOS ---");
        const [permisos] = await pool.query("SELECT * FROM Permisos");
        console.log(permisos);

        console.log("--- ROLES_PERMISOS ---");
        const [rolesPermisos] = await pool.query("SELECT * FROM Roles_Permisos");
        console.log(rolesPermisos);

        console.log("--- OPCIONES ACTUALES ---");
        const [opciones] = await pool.query("SELECT * FROM opciones");
        console.log(opciones);
        
        console.log("--- COLUMNAS USUARIOS ---");
        const [columnasUsuarios] = await pool.query("SHOW COLUMNS FROM Usuarios");
        const redundantCols = columnasUsuarios.filter(c => c.Field === 'id_rol' || c.Field === 'rol');
        console.log(redundantCols);

        process.exit(0);
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
}
investigarRedundancia();
