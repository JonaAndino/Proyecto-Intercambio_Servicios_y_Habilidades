const db = require('./db.js');

const permissions = [
    { clave: 'modalidades:ver', nombre: 'Ver Modalidades de Intercambio', orden: 90 },
    { clave: 'modalidades:crear', nombre: 'Crear Modalidades de Intercambio', orden: 91 },
    { clave: 'modalidades:editar', nombre: 'Editar Modalidades de Intercambio', orden: 92 },
    { clave: 'modalidades:eliminar', nombre: 'Eliminar Modalidades de Intercambio', orden: 93 },
    { clave: 'categorias:ver', nombre: 'Ver Categorías de Habilidades', orden: 94 },
    { clave: 'categorias:crear', nombre: 'Crear Categorías de Habilidades', orden: 95 },
    { clave: 'categorias:editar', nombre: 'Editar Categorías de Habilidades', orden: 96 },
    { clave: 'categorias:eliminar', nombre: 'Eliminar Categorías de Habilidades', orden: 97 },
    { clave: 'variables:ver', nombre: 'Ver Variables de Entorno', orden: 98 },
    { clave: 'variables:crear', nombre: 'Crear Variables de Entorno', orden: 99 },
    { clave: 'variables:editar', nombre: 'Editar Variables de Entorno', orden: 100 },
    { clave: 'variables:eliminar', nombre: 'Eliminar Variables de Entorno', orden: 101 },
    { clave: 'motivosBloqueo:ver', nombre: 'Ver Motivos de Bloqueo', orden: 102 },
    { clave: 'motivosBloqueo:crear', nombre: 'Crear Motivos de Bloqueo', orden: 103 },
    { clave: 'motivosBloqueo:editar', nombre: 'Editar Motivos de Bloqueo', orden: 104 },
    { clave: 'motivosBloqueo:eliminar', nombre: 'Eliminar Motivos de Bloqueo', orden: 105 },
    { clave: 'rolesPermisos:ver', nombre: 'Ver Roles y Permisos', orden: 106 },
    { clave: 'rolesPermisos:crear', nombre: 'Crear Roles y Permisos', orden: 107 },
    { clave: 'rolesPermisos:editar', nombre: 'Editar Roles y Permisos', orden: 108 },
    { clave: 'rolesPermisos:eliminar', nombre: 'Eliminar Roles y Permisos', orden: 109 },
    { clave: 'configGenerales:ver', nombre: 'Ver Ajustes Globales', orden: 110 },
    { clave: 'configGenerales:editar', nombre: 'Editar Ajustes Globales', orden: 111 },
    { clave: 'crearOrdenesTrabajo', nombre: 'Crear Órdenes de Trabajo', orden: 112 },
    { clave: 'editarOrdenesTrabajo', nombre: 'Editar Órdenes de Trabajo', orden: 113 },
    { clave: 'eliminarOrdenesTrabajo', nombre: 'Eliminar Órdenes de Trabajo', orden: 114 },
    { clave: 'CREAR_POSTULACIONES_GLOBALES', nombre: 'Crear Postulaciones', orden: 115 },
    { clave: 'EDITAR_POSTULACIONES_GLOBALES', nombre: 'Editar Postulaciones', orden: 116 },
    { clave: 'ELIMINAR_POSTULACIONES_GLOBALES', nombre: 'Eliminar Postulaciones', orden: 117 },
    { clave: 'GESTIONAR_CONFIGURACION', nombre: 'Acceso al Panel de Configuraciones', orden: 20 },
    { clave: 'VER_METRICAS', nombre: 'Métricas', orden: 14 },
    { clave: 'VER_REPORTES_USUARIOS', nombre: 'Ver usuarios reportados', orden: 15 },
    { clave: 'BLOQUEAR_REPORTADOS', nombre: 'Bloquear usuarios reportados', orden: 16 }
];

async function seedPermissions() {
    try {
        console.log('Iniciando inserción de permisos...');
        for (let p of permissions) {
            const [rows] = await db.execute('SELECT opcion_id FROM opciones WHERE link = ?', [p.clave]);
            if (rows.length === 0) {
                await db.execute('INSERT INTO opciones (nombre, link, orden) VALUES (?, ?, ?)', [p.nombre, p.clave, p.orden]);
                console.log(`Insertado: ${p.clave}`);
            } else {
                console.log(`Ya existe: ${p.clave}`);
            }
        }
        console.log('¡Todos los permisos insertados correctamente!');
        process.exit(0);
    } catch (err) {
        console.error('Error insertando permisos:', err);
        process.exit(1);
    }
}

seedPermissions();
