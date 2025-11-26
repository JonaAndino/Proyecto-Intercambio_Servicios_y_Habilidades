// routes/auth.js
import { Router } from 'express';
import bcrypt from 'bcrypt'; 
import db from '../db.js'; // Usa el pool de conexiones

const router = Router(); // ¡CRÍTICO! Definir el router usando import
const saltRounds = 10; 

// ✅ CLAVE SECRETA PARA JWT (En producción, usar variable de entorno)
const JWT_SECRET = process.env.JWT_SECRET || 'tu_clave_secreta_super_segura_2025_SkillConnect';
const JWT_EXPIRES_IN = '7d'; // Token válido por 7 días 

// ✅ CLAVE SECRETA PARA JWT (En producción, usar variable de entorno)
const JWT_SECRET = process.env.JWT_SECRET || 'tu_clave_secreta_super_segura_2025_SkillConnect';
const JWT_EXPIRES_IN = '7d'; // Token válido por 7 días 


// ******************
// POST: /api/auth/registro (REGISTRAR NUEVO USUARIO)
// ******************
router.post('/registro', async (req, res) => {
    const { correo, contrasena } = req.body; 

    if (!correo || !contrasena) {
        return res.status(400).json({ error: "Correo y contraseña son obligatorios." });
    }

    try {
        // 1. Verificar si el correo ya existe
        const [rows] = await db.query(
            'SELECT id_usuario FROM Usuarios WHERE correo = ?',
            [correo]
        );
        if (rows.length > 0) {
            return res.status(409).json({ error: "El correo ya está registrado." });
        }

        // 2. Cifrar la contraseña
        const contrasena_hash = await bcrypt.hash(contrasena, saltRounds);

        // 3. Insertar nuevo usuario
        await db.query(
            `INSERT INTO Usuarios (correo, contrasena_hash) 
             VALUES (?, ?)`,
            [correo, contrasena_hash]
        );

        res.status(201).json({ mensaje: "Registro exitoso. Usuario creado." });
        const nuevoUsuarioId = result.insertId;

        // 5. CREAR REGISTRO EN TABLA PERSONAS (Reservar espacio para el perfil)
        await pool.execute(
            'INSERT INTO Personas (id_Usuario) VALUES (?)',
            [nuevoUsuarioId]
        );

        // 6. RESPUESTA DE ÉXITO (Paso L del Diagrama)
        res.status(201).json({ 
            mensaje: 'Usuario registrado exitosamente.',
            id_usuario: nuevoUsuarioId 
// ******************
// POST: /api/auth/login (INICIO DE SESIÓN)
// ******************
router.post('/login', async (req, res) => {
    const { correo, contrasena } = req.body;

    if (!correo || !contrasena) {
        return res.status(400).json({ error: "Correo y contraseña son obligatorios." });
    }

    try {
        // 1. Buscar el usuario
        const [rows] = await db.query(
            'SELECT id_usuario, contrasena_hash FROM Usuarios WHERE correo = ?',
            [correo]
        );
        
        if (rows.length === 0) {
            return res.status(401).json({ error: "Credenciales inválidas." });
        }

        const usuario = rows[0];
        
        // 2. Comparar la contraseña
        const match = await bcrypt.compare(contrasena, usuario.contrasena_hash);

        if (!match) {
            return res.status(401).json({ error: "Credenciales inválidas." });
        }

        /// 3. Éxito: Devolver datos básicos (aquí iría la generación de tokens en un proyecto real)
        res.status(200).json({ 
            mensaje: "Inicio de sesión exitoso", 
            id_usuario: usuario.id_usuario 
        });

    } catch (error) {
        console.error("Error en el login:", error);
        res.status(500).json({ error: "Error interno del servidor durante el login." });
    }
});


export default router; // ¡CRÍTICO! Exportar el router
        });

    } catch (error) {
        console.error('Error durante el login JWT:', error);
        res.status(500).json({ error: 'Ocurrió un error en el servidor al intentar iniciar sesión.' });
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
// POST /api/login 
// **********************************************

router.post('/login', async (req, res) => {
    // 1. OBTENER DATOS DEL FRONTEND
    const { correo, contrasena } = req.body;

    // 1.1 Validación básica de campos
    if (!correo || !contrasena) {
        return res.status(400).json({ error: 'Correo y contraseña son obligatorios.' });
    }

    try {
        // 2. BUSCAR USUARIO EN LA BASE DE DATOS POR CORREO
        const [rows] = await pool.execute(
            'SELECT id_usuario, correo, contrasena_hash FROM Usuarios WHERE correo = ?',
            [correo]
        );

        if (rows.length === 0) {
            // Usuario no encontrado
            return res.status(401).json({ error: 'Credenciales inválidas.' });
        }

        const usuario = rows[0];

        // 3. VERIFICAR CONTRASEÑA CON BCRYPT
        const contrasenaValida = await bcrypt.compare(contrasena, usuario.contrasena_hash);

        if (!contrasenaValida) {
            // Contraseña incorrecta
            return res.status(401).json({ error: 'Credenciales inválidas.' });
        }

        // 4. RESPUESTA DE ÉXITO - DEVOLVER ID DE USUARIO
        res.status(200).json({ 
            mensaje: 'Inicio de sesión exitoso',
            usuarioId: usuario.id_usuario,
            correo: usuario.correo
        });

    } catch (error) {
        console.error('Error durante el login:', error);
        res.status(500).json({ error: 'Ocurrió un error en el servidor al intentar iniciar sesión.' });
    }
});

// **********************************************
// POST /api/login-jwt (CON TOKEN JWT)
// **********************************************

router.post('/login-jwt', async (req, res) => {
    const { correo, contrasena } = req.body;

    if (!correo || !contrasena) {
        return res.status(400).json({ error: 'Correo y contraseña son obligatorios.' });
    }

    try {
        // 1. BUSCAR USUARIO
        const [rows] = await pool.execute(
            'SELECT id_usuario, correo, contrasena_hash FROM Usuarios WHERE correo = ?',
            [correo]
        );

        if (rows.length === 0) {
            return res.status(401).json({ error: 'Credenciales inválidas.' });
        }

        const usuario = rows[0];

        // 2. VERIFICAR CONTRASEÑA
        const contrasenaValida = await bcrypt.compare(contrasena, usuario.contrasena_hash);

        if (!contrasenaValida) {
            return res.status(401).json({ error: 'Credenciales inválidas.' });
        }

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
        res.status(500).json({ error: 'Ocurrió un error en el servidor al intentar iniciar sesión.' });
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

module.exports = router;

