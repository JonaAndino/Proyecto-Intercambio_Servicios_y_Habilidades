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

        // Marcar como leídos todos los mensajes de esta conversación que no fueron enviados por mí
        const [result] = await pool.query(
            `UPDATE mensajes 
             SET leido = 1 
             WHERE id_conversacion = ? 
             AND id_persona_envia != ? 
             AND leido = 0`,
            [conversacionId, personaId]
        );

        res.json({
            success: true,
            message: 'Mensajes marcados como leídos',
            mensajes_marcados: result.affectedRows
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


// =========================================================
// 5. EDITAR MENSAJE
// PUT /mensajeria/mensajes/:idMensaje
// Body: { contenido }
// =========================================================
router.put('/mensajes/:idMensaje', async (req, res) => {
    try {
        const mensajeId = req.params.idMensaje;
        const { contenido } = req.body;

        // Validación
        if (!contenido || contenido.trim().length === 0) {
            return res.status(400).json({
                success: false,
                message: 'El contenido del mensaje no puede estar vacío'
            });
        }

        // Actualizar el mensaje
        const [result] = await pool.query(
            'UPDATE mensajes SET contenido = ? WHERE id_mensaje = ?',
            [contenido.trim(), mensajeId]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: 'Mensaje no encontrado'
            });
        }

        res.json({
            success: true,
            message: 'Mensaje actualizado exitosamente'
        });

    } catch (error) {
        console.error('Error al editar mensaje:', error);
        res.status(500).json({
            success: false,
            message: 'Error al editar el mensaje',
            error: error.message
        });
    }
});


// =========================================================
// 6. ELIMINAR MENSAJE
// DELETE /mensajeria/mensajes/:idMensaje
// =========================================================
router.delete('/mensajes/:idMensaje', async (req, res) => {
    try {
        const mensajeId = req.params.idMensaje;

        // Eliminar el mensaje
        const [result] = await pool.query(
            'DELETE FROM mensajes WHERE id_mensaje = ?',
            [mensajeId]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: 'Mensaje no encontrado'
            });
        }

        res.json({
            success: true,
            message: 'Mensaje eliminado exitosamente'
        });

    } catch (error) {
        console.error('Error al eliminar mensaje:', error);
        res.status(500).json({
            success: false,
            message: 'Error al eliminar el mensaje',
            error: error.message
        });
    }
});


module.exports = router;
