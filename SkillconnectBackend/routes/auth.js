// routes/auth.js
import { Router } from 'express';
import bcrypt from 'bcrypt'; 
import db from '../db.js'; // Usa el pool de conexiones

const router = Router(); // ¡CRÍTICO! Definir el router usando import
const saltRounds = 10; 

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

    } catch (error) {
        console.error("Error en el registro:", error);
        res.status(500).json({ error: "Error interno del servidor durante el registro." });
    }
});

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