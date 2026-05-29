// routes/auth.js

const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt'); // Necesario para el Hashing de Contraseñas
const jwt = require('jsonwebtoken'); // Para generar tokens JWT
const pool = require('../db'); // Importa la conexión a la base de datos (DB)

// El número de "rondas de sal" para bcrypt. Más alto es más seguro pero más lento.
const saltRounds = 10;

// ✅ CLAVE SECRETA PARA JWT (En producción, usar variable de entorno)
const JWT_SECRET = process.env.JWT_SECRET || 'tu_clave_secreta_super_segura_2025_SEMACKRO';
const JWT_EXPIRES_IN = '7d'; // Token válido por 7 días 

// **********************************************
// POST /api/registro 
// **********************************************

router.post('/registro', async (req, res) => {
    // 1. OBTENER DATOS (Paso F del Diagrama: Backend recibe datos)
    const { nombre, tipoIdentificacion, numeroIdentificacion, correo, contrasena } = req.body;

    // 1.1 Validación básica de campos no vacíos (una vez que el frontend falle en validarlo)
    if (!nombre || !tipoIdentificacion || !numeroIdentificacion || !correo || !contrasena) {
        return res.status(400).json({ error: 'Todos los campos son obligatorios.' });
    }

    // 1.2 Validar tipo de identificación
    const TIPOS_IDENTIFICACION_VALIDOS = ['DNI', 'Pasaporte'];
    if (!TIPOS_IDENTIFICACION_VALIDOS.includes(tipoIdentificacion)) {
        return res.status(400).json({ error: 'Tipo de identificación no válido.' });
    }

    // 1.3 Validar nombre completo (mínimo 3 caracteres, máximo 100)
    if (nombre.trim().length < 3 || nombre.trim().length > 100) {
        return res.status(400).json({ error: 'El nombre debe tener entre 3 y 100 caracteres.' });
    }

    // 1.4 Validar contraseña (mínimo 6 caracteres)
    if (contrasena.length < 6) {
        return res.status(400).json({ error: 'La contraseña debe tener al menos 6 caracteres.' });
    }

    // 1.5 Validar número de identificación según el tipo (Honduran standards)
    let identificacionLimpia = numeroIdentificacion.trim();
    if (tipoIdentificacion === 'DNI') {
        // DNI Hondureño: 13 dígitos (puede contener guiones, los quitamos para validar)
        identificacionLimpia = identificacionLimpia.replace(/-/g, '');
        if (!/^\d{13}$/.test(identificacionLimpia)) {
            return res.status(400).json({ error: 'El DNI debe contener 13 dígitos (ej: 0101199000123).' });
        }
    } else if (tipoIdentificacion === 'Pasaporte') {
        // Pasaporte Hondureño: empieza por H (o cualquier letra) seguido de 6 dígitos
        if (!/^[A-Za-z]\d{6}$/.test(identificacionLimpia)) {
            return res.status(400).json({ error: 'El pasaporte debe contener 1 letra seguida de 6 dígitos (ej: H123456).' });
        }
    }

    try {
        // 2. CONSULTAR DB: ¿CORREO YA EXISTE? (Paso G del Diagrama)
        const [rows] = await pool.execute('SELECT id_usuario FROM Usuarios WHERE correo = ?', [correo]);

        if (rows.length > 0) {
            // El correo ya existe (Paso H y I del Diagrama)
            return res.status(409).json({ error: 'El correo electrónico ya está registrado. Por favor, intenta con otro.' });
        }

        // 3. CONSULTAR DB: ¿IDENTIFICACIÓN YA EXISTE?
        const [identificacionRows] = await pool.execute('SELECT id_Usuario FROM Personas WHERE identificacion_Persona = ?', [identificacionLimpia]);
        if (identificacionRows.length > 0) {
            return res.status(409).json({ error: 'El número de identificación ya está registrado.' });
        }

        // 4. GENERAR HASH SEGURO (Paso J del Diagrama)
        const contrasena_hash = await bcrypt.hash(contrasena, saltRounds);

        // 5. GUARDAR NUEVO USUARIO EN DB (Paso K del Diagrama)
        const [result] = await pool.execute(
            'INSERT INTO Usuarios (correo, contrasena_hash) VALUES (?, ?)',
            [correo, contrasena_hash]
        );

        const nuevoUsuarioId = result.insertId;

        // 6. CREAR REGISTRO EN TABLA PERSONAS con los datos proporcionados
        // Vamos a dividir el nombre completo en nombre y apellido (solo como aproximación, el primer espacio es el separador)
        const nombreParts = nombre.trim().split(' ');
        const nombrePersona = nombreParts[0] || '';
        const apellidoPersona = nombreParts.slice(1).join(' ') || '';

        await pool.execute(
            'INSERT INTO Personas (id_Usuario, nombre_Persona, apellido_Persona, tipoIdentificacion_Persona, identificacion_Persona) VALUES (?, ?, ?, ?, ?)',
            [nuevoUsuarioId, nombrePersona, apellidoPersona, tipoIdentificacion, identificacionLimpia]
        );

        // 6. RESPUESTA DE ÉXITO (Paso L del Diagrama)
        res.status(201).json({ 
            mensaje: 'Usuario registrado exitosamente.',
            id_usuario: nuevoUsuarioId 
        });

    } catch (error) {
        console.error('Error durante el registro:', error);
        res.status(500).json({ error: 'Ocurrió un error en el servidor al intentar registrar el usuario.', details: error.message });
    }
});

// **********************************************
// POST /api/login 
// **********************************************

router.post('/login', async (req, res) => {
    // 1. OBTENER DATOS DEL FRONTEND
    const { correo, contrasena } = req.body;

    // 1.1 Validación básica de campos
    if (!correo || !contrasena) {
        return res.status(400).json({ error: 'Los campos no pueden estar vacíos.' });
    }

    try {
        // 2. BUSCAR USUARIO EN LA BASE DE DATOS POR CORREO
        const [rows] = await pool.execute(
            'SELECT id_usuario, correo, contrasena_hash, activo, intentos_fallidos, bloqueado_hasta FROM Usuarios WHERE correo = ?',
            [correo]
        );

        if (rows.length === 0) {
            return res.status(401).json({ error: 'El usuario no existe.' });
        }

        const usuario = rows[0];

        // Verificar si está bloqueado
        if (usuario.bloqueado_hasta && new Date() < new Date(usuario.bloqueado_hasta)) {
            if (usuario.bloqueado_hasta.getFullYear() === 9999) {
                return res.status(423).json({ error: 'Tu cuenta está bloqueada permanentemente. Contacta al administrador para desbloquearla.' });
            } else {
                const minutosRestantes = Math.ceil((new Date(usuario.bloqueado_hasta) - new Date()) / (1000 * 60));
                return res.status(423).json({ error: `Tu cuenta está bloqueada temporalmente. Intenta de nuevo en ${minutosRestantes} minuto(s).` });
            }
        } else if (usuario.bloqueado_hasta && new Date() >= new Date(usuario.bloqueado_hasta) && usuario.intentos_fallidos === 5) {
            // Si el bloqueo temporal terminó y estábamos en 5 intentos, mantener el contador en 5 para empezar los 3 intentos finales
            await pool.execute(
                'UPDATE Usuarios SET bloqueado_hasta = NULL WHERE id_usuario = ?',
                [usuario.id_usuario]
            );
        }

        // Verificar si el acceso está restringido
        if (usuario.activo === 0) {
            return res.status(403).json({ error: 'Tu cuenta ha sido restringida por el administrador. Ponte en contacto con el soporte técnico.' });
        }

        // 3. VERIFICAR CONTRASEÑA CON BCRYPT
        const contrasenaValida = await bcrypt.compare(contrasena, usuario.contrasena_hash);

        if (!contrasenaValida) {
            // Incrementar contador de intentos fallidos
            const nuevosIntentos = usuario.intentos_fallidos + 1;
            let bloqueadoHasta = usuario.bloqueado_hasta;
            
            if (nuevosIntentos === 5) {
                // Bloquear temporalmente por 2 minutos después de 5 intentos
                bloqueadoHasta = new Date(Date.now() + 2 * 60 * 1000);
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = ?, bloqueado_hasta = ? WHERE id_usuario = ?',
                    [nuevosIntentos, bloqueadoHasta, usuario.id_usuario]
                );
                return res.status(423).json({ error: 'Has alcanzado 5 intentos fallidos. Tu cuenta está bloqueada temporalmente por 2 minutos.' });
            } else if (nuevosIntentos === 6) {
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = ? WHERE id_usuario = ?',
                    [nuevosIntentos, usuario.id_usuario]
                );
                return res.status(401).json({ error: 'La contraseña es incorrecta. Te quedan 2 intentos antes del bloqueo permanente.' });
            } else if (nuevosIntentos === 7) {
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = ? WHERE id_usuario = ?',
                    [nuevosIntentos, usuario.id_usuario]
                );
                return res.status(401).json({ error: 'La contraseña es incorrecta. Te queda 1 intento antes del bloqueo permanente.' });
            } else if (nuevosIntentos >= 8) {
                // Bloquear permanentemente después de 8 intentos (5 + 3)
                bloqueadoHasta = new Date('9999-12-31 23:59:59');
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = 0, bloqueado_hasta = ? WHERE id_usuario = ?',
                    [bloqueadoHasta, usuario.id_usuario]
                );
                return res.status(423).json({ error: 'Tu cuenta está bloqueada permanentemente por demasiados intentos fallidos. Contacta con el administrador para poder acceder.' });
            }
            
            await pool.execute(
                'UPDATE Usuarios SET intentos_fallidos = ? WHERE id_usuario = ?',
                [nuevosIntentos, usuario.id_usuario]
            );
            return res.status(401).json({ error: 'La contraseña es incorrecta.' });
        }

        // Si la contraseña es correcta, resetear intentos fallidos y bloqueo
        await pool.execute(
            'UPDATE Usuarios SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id_usuario = ?',
            [usuario.id_usuario]
        );

        // 4. RESPUESTA DE ÉXITO - DEVOLVER ID DE USUARIO
        res.status(200).json({ 
            mensaje: 'Inicio de sesión exitoso',
            usuarioId: usuario.id_usuario,
            correo: usuario.correo
        });

    } catch (error) {
        console.error('Error durante el login:', error);
        res.status(500).json({ error: 'Ocurrió un error en el servidor al intentar iniciar sesión.', details: error.message });
    }
});

// **********************************************
// POST /api/login-jwt (CON TOKEN JWT)
// **********************************************

router.post('/login-jwt', async (req, res) => {
    const { correo, contrasena } = req.body;

    if (!correo || !contrasena) {
        return res.status(400).json({ error: 'Los campos no pueden estar vacíos.' });
    }

    try {
        // 1. BUSCAR USUARIO
        const [rows] = await pool.execute(
            'SELECT id_usuario, correo, contrasena_hash, activo, intentos_fallidos, bloqueado_hasta FROM Usuarios WHERE correo = ?',
            [correo]
        );

        if (rows.length === 0) {
            return res.status(401).json({ error: 'El usuario no existe.' });
        }

        const usuario = rows[0];

        // Verificar si está bloqueado
        if (usuario.bloqueado_hasta && new Date() < new Date(usuario.bloqueado_hasta)) {
            if (usuario.bloqueado_hasta.getFullYear() === 9999) {
                return res.status(423).json({ error: 'Tu cuenta está bloqueada permanentemente. Contacta al administrador para desbloquearla.' });
            } else {
                const minutosRestantes = Math.ceil((new Date(usuario.bloqueado_hasta) - new Date()) / (1000 * 60));
                return res.status(423).json({ error: `Tu cuenta está bloqueada temporalmente. Intenta de nuevo en ${minutosRestantes} minuto(s).` });
            }
        } else if (usuario.bloqueado_hasta && new Date() >= new Date(usuario.bloqueado_hasta) && usuario.intentos_fallidos === 5) {
            // Si el bloqueo temporal terminó y estábamos en 5 intentos, mantener el contador en 5 para empezar los 3 intentos finales
            await pool.execute(
                'UPDATE Usuarios SET bloqueado_hasta = NULL WHERE id_usuario = ?',
                [usuario.id_usuario]
            );
        }

        // Verificar si el acceso está restringido
        if (usuario.activo === 0) {
            return res.status(403).json({ error: 'Tu cuenta ha sido restringida por el administrador. Ponte en contacto con el soporte técnico.' });
        }

        // 2. VERIFICAR CONTRASEÑA
        const contrasenaValida = await bcrypt.compare(contrasena, usuario.contrasena_hash);

        if (!contrasenaValida) {
            // Incrementar contador de intentos fallidos
            const nuevosIntentos = usuario.intentos_fallidos + 1;
            let bloqueadoHasta = usuario.bloqueado_hasta;
            
            if (nuevosIntentos === 5) {
                // Bloquear temporalmente por 2 minutos después de 5 intentos
                bloqueadoHasta = new Date(Date.now() + 2 * 60 * 1000);
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = ?, bloqueado_hasta = ? WHERE id_usuario = ?',
                    [nuevosIntentos, bloqueadoHasta, usuario.id_usuario]
                );
                return res.status(423).json({ error: 'Has alcanzado 5 intentos fallidos. Tu cuenta está bloqueada temporalmente por 2 minutos.' });
            } else if (nuevosIntentos === 6) {
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = ? WHERE id_usuario = ?',
                    [nuevosIntentos, usuario.id_usuario]
                );
                return res.status(401).json({ error: 'La contraseña es incorrecta. Te quedan 2 intentos antes del bloqueo permanente.' });
            } else if (nuevosIntentos === 7) {
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = ? WHERE id_usuario = ?',
                    [nuevosIntentos, usuario.id_usuario]
                );
                return res.status(401).json({ error: 'La contraseña es incorrecta. Te queda 1 intento antes del bloqueo permanente.' });
            } else if (nuevosIntentos >= 8) {
                // Bloquear permanentemente después de 8 intentos (5 + 3)
                bloqueadoHasta = new Date('9999-12-31 23:59:59');
                await pool.execute(
                    'UPDATE Usuarios SET intentos_fallidos = 0, bloqueado_hasta = ? WHERE id_usuario = ?',
                    [bloqueadoHasta, usuario.id_usuario]
                );
                return res.status(423).json({ error: 'Tu cuenta está bloqueada permanentemente por demasiados intentos fallidos. Contacta con el administrador para poder acceder.' });
            }
            
            await pool.execute(
                'UPDATE Usuarios SET intentos_fallidos = ? WHERE id_usuario = ?',
                [nuevosIntentos, usuario.id_usuario]
            );
            return res.status(401).json({ error: 'La contraseña es incorrecta.' });
        }

        // Si la contraseña es correcta, resetear intentos fallidos y bloqueo
        await pool.execute(
            'UPDATE Usuarios SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id_usuario = ?',
            [usuario.id_usuario]
        );

        // 3. GENERAR TOKEN JWT
        const token = jwt.sign(
            { 
                usuarioId: usuario.id_usuario,
                correo: usuario.correo
            },
            JWT_SECRET,
            { expiresIn: JWT_EXPIRES_IN }
        );

        // 4. DEVOLVER TOKEN
        res.status(200).json({ 
            mensaje: 'Inicio de sesión exitoso',
            token: token,
            usuarioId: usuario.id_usuario,
            correo: usuario.correo
        });

    } catch (error) {
        console.error('Error durante el login JWT:', error);
        res.status(500).json({ error: 'Ocurrió un error en el servidor al intentar iniciar sesión.', details: error.message });
    }
});

// **********************************************
// MIDDLEWARE: Verificar Token JWT
// **********************************************

function verificarToken(req, res, next) {
    // Obtener token del header Authorization
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Format: "Bearer TOKEN"

    if (!token) {
        return res.status(401).json({ error: 'Token no proporcionado. Inicia sesión nuevamente.' });
    }

    try {
        // Verificar y decodificar el token
        const decoded = jwt.verify(token, JWT_SECRET);
        req.usuario = decoded; // Guardar info del usuario en req
        next(); // Continuar con la siguiente función
    } catch (error) {
        return res.status(403).json({ error: 'Token inválido o expirado.' });
    }
}

// **********************************************
// GET /api/verificar-sesion (Verificar si el token es válido)
// **********************************************

router.get('/verificar-sesion', verificarToken, (req, res) => {
    // Si llegó aquí, el token es válido
    res.status(200).json({ 
        mensaje: 'Sesión válida',
        usuarioId: req.usuario.usuarioId,
        correo: req.usuario.correo
    });
});

// **********************************************
// PUT /api/usuarios/:id_usuario/activo (Restringir/Permitir acceso)
// **********************************************
router.put('/usuarios/:id_usuario/activo', async (req, res) => {
    const id_usuario = parseInt(req.params.id_usuario);
    const { activo } = req.body; // 0 o 1

    if (isNaN(id_usuario)) {
        return res.status(400).json({ success: false, error: 'ID de usuario no válido.' });
    }

    if (activo !== 0 && activo !== 1) {
        return res.status(400).json({ success: false, error: 'Valor de estado "activo" no válido (debe ser 0 o 1).' });
    }

    try {
        let query, params;
        if (activo === 1) {
            // Si activamos el usuario, también reseteamos intentos fallidos y bloqueo
            query = 'UPDATE Usuarios SET activo = ?, intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id_usuario = ?';
            params = [activo, id_usuario];
        } else {
            // Si desactivamos, solo actualizamos activo
            query = 'UPDATE Usuarios SET activo = ? WHERE id_usuario = ?';
            params = [activo, id_usuario];
        }
        
        const [result] = await pool.execute(query, params);
        if (result.affectedRows === 0) {
            return res.status(404).json({ success: false, error: 'Usuario no encontrado.' });
        }
        res.status(200).json({ success: true, mensaje: 'Acceso de usuario actualizado con éxito.' });
    } catch (error) {
        console.error('Error al actualizar estado del usuario:', error);
        res.status(500).json({ success: false, error: 'Error del servidor al intentar actualizar el estado de acceso.' });
    }
});

// **********************************************
// PUT /api/usuarios/:id_usuario/desbloquear (Desbloquear cuenta por intentos fallidos)
// **********************************************
router.put('/usuarios/:id_usuario/desbloquear', async (req, res) => {
    const id_usuario = parseInt(req.params.id_usuario);

    if (isNaN(id_usuario)) {
        return res.status(400).json({ success: false, error: 'ID de usuario no válido.' });
    }

    try {
        const [result] = await pool.execute(
            'UPDATE Usuarios SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id_usuario = ?',
            [id_usuario]
        );
        if (result.affectedRows === 0) {
            return res.status(404).json({ success: false, error: 'Usuario no encontrado.' });
        }
        res.status(200).json({ success: true, mensaje: 'Cuenta desbloqueada con éxito.' });
    } catch (error) {
        console.error('Error al desbloquear usuario:', error);
        res.status(500).json({ success: false, error: 'Error del servidor al intentar desbloquear la cuenta.' });
    }
});

module.exports = router;
