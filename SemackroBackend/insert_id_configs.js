const mysql = require('mysql2/promise');
require('dotenv').config({ path: '.env' });

async function insertIdentifications() {
    try {
        const connection = await mysql.createConnection({
            host: process.env.DB_HOST || '104.155.156.171',
            user: process.env.DB_USER || 'usuario1',
            password: process.env.DB_PASSWORD || 'equipo2',
            database: process.env.DB_DATABASE || 'SkillConnect2025',
            port: process.env.DB_PORT || 3306
        });

        const configs = [
            { clave: 'identificacion_dni_activado', valor: 'true', tipo: 'boolean', desc: 'Permitir DNI como tipo de identificación' },
            { clave: 'identificacion_pasaporte_activado', valor: 'true', tipo: 'boolean', desc: 'Permitir Pasaporte como tipo de identificación' },
            { clave: 'identificacion_licencia_activado', valor: 'true', tipo: 'boolean', desc: 'Permitir Licencia de Conducir como tipo de identificación' },
            { clave: 'identificacion_otro_activado', valor: 'true', tipo: 'boolean', desc: 'Permitir Otro documento como tipo de identificación' }
        ];

        for (const c of configs) {
            await connection.execute(`
                INSERT INTO Configuraciones_Sistema (clave, valor, tipo, descripcion)
                VALUES (?, ?, ?, ?)
                ON DUPLICATE KEY UPDATE valor = VALUES(valor)
            `, [c.clave, c.valor, c.tipo, c.desc]);
            console.log(`✅ ${c.clave} configurado.`);
        }
        
        await connection.end();
    } catch (e) {
        console.error(e);
    }
}
insertIdentifications();
