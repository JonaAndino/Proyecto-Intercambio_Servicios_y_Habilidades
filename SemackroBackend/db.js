// db.js

// 1. Cargar variables de entorno (desde el archivo .env)
require('dotenv').config();

// 2. Importar el driver de MySQL (mysql2)
const mysql = require('mysql2');

// 3. Determinar host/puerto de DB
// - En producción respetamos `DB_HOST`/`DB_PORT` únicamente.
// - Para desarrollo/pruebas se permiten `DB_HOST_OVERRIDE`/`DB_PORT_OVERRIDE`.
const isProd = process.env.NODE_ENV === 'production';
const dbHost = (!isProd && process.env.DB_HOST_OVERRIDE) ? process.env.DB_HOST_OVERRIDE : (process.env.DB_HOST || 'localhost');
const dbPort = (!isProd && process.env.DB_PORT_OVERRIDE) ? process.env.DB_PORT_OVERRIDE : (process.env.DB_PORT || 3306);

// 4. Crear el pool de conexiones a la base de datos
const poolConfig = {
    host: dbHost,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
    port: dbPort,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    enableKeepAlive: false,
    keepAliveInitialDelay: 0
};

// Configuraciones adicionales SOLO para desarrollo (no afecta producción)
if (!isProd) {
    poolConfig.connectTimeout = 10000;
    console.log('ℹ️  Modo desarrollo: Configuraciones de keepalive activadas para conexiones DB');
}

const pool = mysql.createPool(poolConfig);

// 4. Función de prueba: Intenta conectarse a la DB al iniciar el servidor
pool.getConnection((err, connection) => {
    if (err) {
        // *** ESTA LÍNEA MOSTRARÁ EL ERROR REAL ***
        console.error('ERROR CRÍTICO DE CONEXIÓN A DB. Detalles del fallo:');
        console.error(err); 
        return;
    }
    const usedHost = dbHost;
    console.log(`Conexión exitosa a la base de datos SkillConnect2025 (host: ${usedHost}, port: ${dbPort}).`);
    if (usedHost === 'localhost') {
        console.log('Nota: `DB_HOST` está en localhost. Si la base de datos está en la nube, actualiza SemackroBackend/.env con el host remoto o usa DB_HOST_OVERRIDE para pruebas.');
    }
    connection.release(); // Libera la conexión de vuelta al pool
});

// 5. Exportar el pool con soporte para promesas (lo que usa 'await' en auth.js)
module.exports = pool.promise();