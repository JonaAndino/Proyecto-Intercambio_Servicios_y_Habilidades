// routes/Mensajeria.js
const express = require('express');
const router = express.Router();
const pool = require('../db');

// =========================================================
// 1. OBTENER CONVERSACIONES DE UNA PERSONA
// GET /mensajeria/conversaciones/:idPersona
// =========================================================
router.get('/conversaciones/:idPersona', async (req, res) => {
    try {
        const personaId = req.params.idPersona;

        const [results] = await pool.query(
            'CALL sp_ObtenerConversacionesPorPersona(?)',
            [personaId]
        );

        const conversaciones = results[0];

        res.json({
            success: true,
            count: conversaciones.length,
            data: conversaciones
        });

    } catch (error) {
        console.error('Error al obtener conversaciones:', error);
        res.status(500).json({
            success: false,
            message: 'Error al obtener conversaciones',
            error: error.message
        });
    }
});


// =========================================================
// 2. OBTENER MENSAJES DE UNA CONVERSACIÓN
// GET /mensajeria/conversacion/:idConversacion/mensajes
// Query param: personaId (para marcar tipo enviado/recibido)
// =========================================================
router.get('/conversacion/:idConversacion/mensajes', async (req, res) => {
    try {
        const conversacionId = req.params.idConversacion;
        const personaId = req.query.personaId;

        if (!personaId) {
            return res.status(400).json({
                success: false,
                message: 'Se requiere personaId como query parameter'
            });
        }

        const [results] = await pool.query(
            'CALL sp_ObtenerMensajesConversacion(?, ?)',
            [conversacionId, personaId]
        );

        const mensajes = results[0];

        res.json({
            success: true,
            count: mensajes.length,
            data: mensajes
        });

    } catch (error) {
        console.error('Error al obtener mensajes:', error);
        res.status(500).json({
            success: false,
            message: 'Error al obtener mensajes',
            error: error.message
        });
    }
});


// =========================================================
// 3. ENVIAR MENSAJE
// POST /mensajeria/enviar
// Body: { conversacionId, personaEnviaId, contenido }
// =========================================================
router.post('/enviar', async (req, res) => {
    try {
        const { conversacionId, personaEnviaId, contenido } = req.body;

        // Validación
        if (!conversacionId || !personaEnviaId || !contenido) {
            return res.status(400).json({
                success: false,
                message: 'Se requieren conversacionId, personaEnviaId y contenido'
            });
        }

        if (contenido.trim().length === 0) {
            return res.status(400).json({
                success: false,
                message: 'El mensaje no puede estar vacío'
            });
        }

        const [results] = await pool.query(
            'CALL sp_EnviarMensaje(?, ?, ?)',
            [conversacionId, personaEnviaId, contenido.trim()]
        );

        const mensaje = results[0][0];

        res.status(201).json({
            success: true,
            message: 'Mensaje enviado exitosamente',
            data: mensaje
        });

    } catch (error) {
        console.error('Error al enviar mensaje:', error);
        res.status(500).json({
            success: false,
            message: 'Error al enviar el mensaje',
            error: error.message
        });
    }
});


// =========================================================
// 4. MARCAR MENSAJES COMO LEÍDOS
// PUT /mensajeria/conversacion/:idConversacion/marcar-leidos
// Body: { personaId }
// =========================================================
router.put('/conversacion/:idConversacion/marcar-leidos', async (req, res) => {
    try {
        const conversacionId = req.params.idConversacion;
        const { personaId } = req.body;

        if (!personaId) {
            return res.status(400).json({
                success: false,
                message: 'Se requiere personaId en el body'
            });
        }

        const [results] = await pool.query(
            'CALL sp_MarcarMensajesComoLeidos(?, ?)',
            [conversacionId, personaId]
        );

        const resultado = results[0][0];

        res.json({
            success: true,
            message: 'Mensajes marcados como leídos',
            mensajes_marcados: resultado.mensajes_marcados
        });

    } catch (error) {
        console.error('Error al marcar mensajes como leídos:', error);
        res.status(500).json({
            success: false,
            message: 'Error al marcar mensajes como leídos',
            error: error.message
        });
    }
});


module.exports = router;
