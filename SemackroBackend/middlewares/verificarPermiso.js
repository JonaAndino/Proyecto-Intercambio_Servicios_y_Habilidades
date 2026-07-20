const jwt = require('jsonwebtoken');
const db = require('../db');
require('dotenv').config();

const JWT_SECRET = process.env.JWT_SECRET || 'secreto_super_seguro_123';

/**
 * Middleware para verificar si el usuario logueado tiene un permiso específico.
 * @param {string} permisoRequerido - La clave del permiso (ej: 'modalidades:crear')
 */
const verificarPermiso = (permisoRequerido) => {
    return async (req, res, next) => {
        try {
            // 1. Extraer y verificar el token JWT
            const authHeader = req.headers['authorization'];
            const token = authHeader && authHeader.split(' ')[1];

            if (!token) {
                return res.status(401).json({ error: 'Token no proporcionado. Inicia sesión nuevamente.' });
            }

            const decoded = jwt.verify(token, JWT_SECRET);
            req.user = decoded; // { usuarioId, correo, etc. }

            // 2. Verificar el permiso en la base de datos
            // Obtenemos los permisos del usuario usando el SP o query equivalente
            // En este caso, usaremos la lógica estándar para consultar los permisos del usuario por su rol.
            
            const query = `
                SELECT 
                    IFNULL(duo.concedido, IF(dro.opcion_id IS NOT NULL, 1, 0)) AS tiene_permiso
                FROM opciones o
                LEFT JOIN d_usuarios_opciones duo ON o.opcion_id = duo.opcion_id AND duo.usuario_id = ?
                LEFT JOIN (
                    SELECT DISTINCT dro.opcion_id 
                    FROM d_roles_opciones dro
                    JOIN d_usuarios_roles dur ON dro.rol_id = dur.rol_id
                    WHERE dur.usuario_id = ?
                ) dro ON o.opcion_id = dro.opcion_id
                WHERE o.link = ?
            `;
            
            const [rows] = await db.execute(query, [req.user.usuarioId, req.user.usuarioId, permisoRequerido]);

            if (rows.length === 0 || rows[0].tiene_permiso != 1) {
                // Si no tiene el permiso, denegar
                return res.status(403).json({ error: `Acceso denegado. Requiere el permiso: ${permisoRequerido}` });
            }

            // Si llegamos aquí, el usuario tiene el permiso
            next();
        } catch (error) {
            console.error('Error en verificarPermiso:', error.message);
            if (error.name === 'TokenExpiredError' || error.name === 'JsonWebTokenError') {
                return res.status(403).json({ error: 'Token inválido o expirado.' });
            }
            return res.status(500).json({ error: 'Error interno del servidor al verificar permisos.' });
        }
    };
};

module.exports = verificarPermiso;
