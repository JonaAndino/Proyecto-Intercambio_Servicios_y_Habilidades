const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../db');
const { enviarCorreoRecuperacion } = require('../config/email');
const JWT_SECRET = process.env.JWT_SECRET || 'tu_clave_secreta_super_segura_2025_SEMACKRO';

// Función para obtener configuración del sistema
async function getConfigValue(clave) {
    try {
        const [configs] = await db.execute('SELECT id_configuracion, clave, valor, tipo, descripcion FROM Configuraciones_Sistema');
        const config = configs.find(c => c.clave === clave);
        if (!config) return null;
        if (config.tipo === 'number') return Number(config.valor);
        if (config.tipo === 'boolean') return config.valor === '1' || config.valor === 'true';
        return config.valor;
    } catch (error) {
        console.error('Error al obtener configuración:', error);
        return null;
    }
}

// Mapa para limitar usos exitosos de tokens de recuperación de contraseña (máximo 2 usos)
const tokenUsageMap = new Map();

function maskEmail(email) {
    if (!email || typeof email !== 'string' || !email.includes('@')) return '[email-invalido]';
    const [local, domain] = email.split('@');
    const visibleLocal = local.length <= 2 ? local[0] || '*' : local.slice(0, 2);
    return `${visibleLocal}***@${domain}`;
}

function buildTraceId() {
    return `pwdrec-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

// POST /api/password/solicitar-recuperacion
// Solicitar recuperación de contraseña
router.post('/solicitar-recuperacion', async (req, res) => {
    const { tipoIdentificacion, numeroIdentificacion, FRONTEND_URL, EMAIL_FROM_NAME } = req.body;
    const traceId = buildTraceId();
    const startedAt = Date.now();

    console.log(`[password-recovery][${traceId}] Inicio solicitud por identificación`);

    if (!tipoIdentificacion || !numeroIdentificacion) {
        console.warn(`[password-recovery][${traceId}] Solicitud rechazada: datos de identificación incompletos`);
        return res.status(400).json({ 
            success: false, 
            mensaje: 'Los datos de identificación son requeridos' 
        });
    }

    // Limpiar identificación
    let identificacionLimpia = String(numeroIdentificacion).trim();
    if (tipoIdentificacion === 'DNI') {
        identificacionLimpia = identificacionLimpia.replace(/-/g, '');
        // Validar DNI hondureño (13 dígitos)
        if (!/^\d{13}$/.test(identificacionLimpia)) {
            console.warn(`[password-recovery][${traceId}] Solicitud rechazada: DNI inválido`);
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El DNI debe contener 13 dígitos' 
            });
        }
    } else if (tipoIdentificacion === 'Pasaporte') {
        // Validar pasaporte hondureño (letra + 6 dígitos)
        if (!/^[A-Za-z]\d{6}$/.test(identificacionLimpia)) {
            console.warn(`[password-recovery][${traceId}] Solicitud rechazada: pasaporte inválido`);
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El pasaporte debe contener 1 letra seguida de 6 dígitos' 
            });
        }
    }

    try {
        // Verificar si el usuario existe y coincide con la identificación
        const query = `
            SELECT u.id_usuario, u.correo 
            FROM Usuarios u
            INNER JOIN Personas p ON u.id_usuario = p.id_Usuario
            WHERE (p.tipoIdentificacion_Persona = ? OR p.tipoIdentificacion_Persona IS NULL) 
              AND REPLACE(p.identificacion_Persona, '-', '') = ?
        `;
        const [usuarios] = await db.query(query, [tipoIdentificacion, identificacionLimpia]);
        console.log(`[password-recovery][${traceId}] Resultado búsqueda usuario: ${usuarios.length > 0 ? 'encontrado' : 'no encontrado'}`);

        // Por seguridad, siempre devolvemos el mismo mensaje
        // (no revelamos explícitamente detalles que faciliten enumeración, aunque ahora devolveremos el correo enmascarado si se encuentra para el modal)
        const mensajeGenerico = 'Si los datos son correctos, recibirás instrucciones en el correo asociado para recuperar tu contraseña.';

        if (usuarios.length === 0) {
            console.log(`[password-recovery][${traceId}] Identificación no encontrada. Respuesta genérica enviada en ${Date.now() - startedAt}ms`);
            return res.status(200).json({ 
                success: true, 
                mensaje: mensajeGenerico,
                emailEnmascarado: '*****@****.***'
            });
        }

        const usuario = usuarios[0];
        const cleanCorreo = usuario.correo;
        const maskedCorreo = maskEmail(cleanCorreo);

        // Obtener duración del token desde configuraciones (en segundos)
        const tokenDuration = await getConfigValue('jwt_reset_password_duration');
        const expiresIn = tokenDuration ? `${tokenDuration}s` : '1d'; // Default to 1 day if config not found
        
        // Generar token JWT
        const token = jwt.sign(
            { 
                id_usuario: usuario.id_usuario, 
                correo: usuario.correo,
                tipo: 'recuperacion_password'
            },
            JWT_SECRET,
            { expiresIn }
        );
        console.log(`[password-recovery][${traceId}] Token de recuperación generado para usuario ${usuario.id_usuario}`);

        // Responder de inmediato para evitar timeouts en la interfaz.
        res.status(200).json({
            success: true,
            mensaje: mensajeGenerico,
            emailEnmascarado: maskedCorreo
        });
        console.log(`[password-recovery][${traceId}] Respuesta genérica enviada en ${Date.now() - startedAt}ms`);

        // Enviar correo en segundo plano; los fallos se registran en logs.
        setImmediate(async () => {
            const mailStartedAt = Date.now();
            try {
                console.log(`[password-recovery][${traceId}] Intentando envío de correo a ${maskedCorreo}`);
                const resultado = await enviarCorreoRecuperacion(cleanCorreo, token, {
                    frontendUrl: FRONTEND_URL,
                    emailFromName: EMAIL_FROM_NAME,
                    traceId,
                    tokenDuration: tokenDuration
                });
                if (resultado.success) {
                    console.log(`[password-recovery][${traceId}] Correo enviado correctamente (${maskedCorreo}) messageId=${resultado.messageId || 'n/a'} en ${Date.now() - mailStartedAt}ms`);
                } else {
                    console.error(`[password-recovery][${traceId}] Fallo al enviar correo (${maskedCorreo}) en ${Date.now() - mailStartedAt}ms:`, resultado.error);
                }
            } catch (mailError) {
                console.error(`[password-recovery][${traceId}] Error inesperado en envío de correo (${maskedCorreo}) en ${Date.now() - mailStartedAt}ms:`, mailError);
            }
        });

        return;

    } catch (error) {
        console.error(`[password-recovery][${traceId}] Error en solicitar-recuperacion tras ${Date.now() - startedAt}ms:`, error);
        return res.status(500).json({ 
            success: false, 
            mensaje: 'Error del servidor' 
        });
    }
});

// POST /api/password/validar-token
// Validar si el token es válido
router.post('/validar-token', async (req, res) => {
    const { token } = req.body;

    if (!token) {
        return res.status(400).json({ 
            success: false, 
            mensaje: 'Token requerido' 
        });
    }

    try {
        // Verificar y decodificar el token
        const decoded = jwt.verify(token, JWT_SECRET);

        // Verificar que sea un token de tipo recuperación
        if (decoded.tipo !== 'recuperacion_password') {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'Token inválido' 
            });
        }

        // Verificar límite de usos exitosos
        const currentCount = tokenUsageMap.get(token) || 0;
        if (currentCount >= 2) {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El enlace ha superado el número máximo de usos permitidos (2).' 
            });
        }

        // Verificar que el usuario aún existe
        const query = 'SELECT id_usuario FROM Usuarios WHERE id_usuario = ?';
        const [usuarios] = await db.query(query, [decoded.id_usuario]);

        if (usuarios.length === 0) {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'Usuario no encontrado' 
            });
        }

        return res.status(200).json({ 
            success: true, 
            mensaje: 'Token válido',
            correo: decoded.correo
        });

    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El enlace ha expirado. Solicita uno nuevo.' 
            });
        } else if (error.name === 'JsonWebTokenError') {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El enlace es inválido.' 
            });
        }

        console.error('Error en validar-token:', error);
        return res.status(500).json({ 
            success: false, 
            mensaje: 'Error del servidor' 
        });
    }
});

// POST /api/password/restablecer
// Restablecer contraseña con token válido
router.post('/restablecer', async (req, res) => {
    const { token, nuevaPassword } = req.body;

    if (!token || !nuevaPassword) {
        return res.status(400).json({ 
            success: false, 
            mensaje: 'Token y nueva contraseña son requeridos' 
        });
    }

    if (nuevaPassword.length < 6) {
        return res.status(400).json({ 
            success: false, 
            mensaje: 'La contraseña debe tener al menos 6 caracteres' 
        });
    }

    try {
        // Verificar y decodificar el token
        const decoded = jwt.verify(token, JWT_SECRET);

        // Verificar que sea un token de tipo recuperación
        if (decoded.tipo !== 'recuperacion_password') {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'Token inválido' 
            });
        }

        // Verificar límite de usos exitosos
        const currentCount = tokenUsageMap.get(token) || 0;
        if (currentCount >= 2) {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El enlace ha superado el número máximo de usos permitidos (2).' 
            });
        }

        // Hash de la nueva contraseña
        const hashedPassword = await bcrypt.hash(nuevaPassword, 10);

        // Actualizar la contraseña en la base de datos
        const updateQuery = 'UPDATE Usuarios SET contrasena_hash = ? WHERE id_usuario = ?';
        const [result] = await db.query(updateQuery, [hashedPassword, decoded.id_usuario]);

        console.log(`Contraseña actualizada para usuario ID: ${decoded.id_usuario}`, result);

        // Incrementar el uso exitoso del token
        tokenUsageMap.set(token, currentCount + 1);

        return res.status(200).json({ 
            success: true, 
            mensaje: 'Contraseña actualizada exitosamente. Ya puedes iniciar sesión.' 
        });

    } catch (error) {
        console.error('Error completo en restablecer:', error);
        if (error.name === 'TokenExpiredError') {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El enlace ha expirado. Solicita uno nuevo.' 
            });
        } else if (error.name === 'JsonWebTokenError') {
            return res.status(400).json({ 
                success: false, 
                mensaje: 'El enlace es inválido.' 
            });
        }

        console.error('Error en restablecer:', error);
        return res.status(500).json({ 
            success: false, 
            mensaje: 'Error del servidor: ' + error.message 
        });
    }
});

module.exports = router;
