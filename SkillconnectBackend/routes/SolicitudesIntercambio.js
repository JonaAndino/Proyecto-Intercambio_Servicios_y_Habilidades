// routes/SolicitudesIntercambio.js
const express = require('express');
const router = express.Router();
const pool = require('../db');

// =========================================================
// 1. ENVIAR SOLICITUD DE INTERCAMBIO
// POST /solicitudes-intercambio/enviar
// Body: { solicitanteId, receptorId }
// =========================================================
router.post('/enviar', async (req, res) => {
    try {
        const { solicitanteId, receptorId } = req.body;

        // Validación básica
        if (!solicitanteId || !receptorId) {
            return res.status(400).json({
                success: false,
                message: 'Se requieren solicitanteId y receptorId'
            });
        }

        // Evitar auto-solicitud
        if (solicitanteId === receptorId) {
            return res.status(400).json({
                success: false,
                message: 'No puedes enviarte una solicitud a ti mismo'
            });
        }

        // Verificar si ya existe una solicitud pendiente entre estos usuarios
        const [solicitudesExistentes] = await pool.query(
            `SELECT id_solicitud, estado 
             FROM solicitudes_intercambio 
             WHERE ((id_persona_solicitante = ? AND id_persona_receptor = ?) 
                OR (id_persona_solicitante = ? AND id_persona_receptor = ?))
             AND estado IN ('Pendiente', 'Aceptada')`,
            [solicitanteId, receptorId, receptorId, solicitanteId]
        );

        if (solicitudesExistentes.length > 0) {
            const solicitud = solicitudesExistentes[0];
            if (solicitud.estado === 'Aceptada') {
                return res.status(400).json({
                    success: false,
                    message: 'Ya tienes una conexión establecida con este usuario'
                });
            } else {
                return res.status(400).json({
                    success: false,
                    message: 'Ya existe una solicitud pendiente con este usuario'
                });
            }
        }

        // Llamar al stored procedure para insertar la solicitud
        await pool.query(
            'CALL sp_InsertarSolicitud(?, ?)',
            [solicitanteId, receptorId]
        );

        res.status(201).json({
            success: true,
            message: 'Solicitud de intercambio enviada exitosamente'
        });

    } catch (error) {
        console.error('Error al enviar solicitud:', error);
        res.status(500).json({
            success: false,
            message: 'Error al enviar la solicitud',
            error: error.message
        });
    }
});


// =========================================================
// 2. ACEPTAR SOLICITUD
// PUT /solicitudes-intercambio/:id/aceptar
// =========================================================
router.put('/:id/aceptar', async (req, res) => {
    try {
        const solicitudId = req.params.id;

        // Primero obtener datos de la solicitud
        const [solicitudData] = await pool.query(
            'SELECT id_persona_solicitante, id_persona_receptor FROM solicitudes_intercambio WHERE id_solicitud = ?',
            [solicitudId]
        );

        if (!solicitudData || solicitudData.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'Solicitud no encontrada'
            });
        }

        const { id_persona_solicitante, id_persona_receptor } = solicitudData[0];

        // Actualizar estado a 'Aceptada'
        await pool.query(
            'CALL sp_ActualizarEstadoSolicitud(?, ?)',
            [solicitudId, 'Aceptada']
        );

        // Crear conversación automáticamente
        const [conversacionResult] = await pool.query(
            'CALL sp_CrearConversacion(?, ?, ?)',
            [id_persona_solicitante, id_persona_receptor, solicitudId]
        );

        const conversacion = conversacionResult[0][0];

        res.json({
            success: true,
            message: 'Solicitud aceptada exitosamente',
            conversacion: {
                id_conversacion: conversacion.id_conversacion,
                fecha_creacion: conversacion.fecha_creacion
            }
        });

    } catch (error) {
        console.error('Error al aceptar solicitud:', error);
        res.status(500).json({
            success: false,
            message: 'Error al aceptar la solicitud',
            error: error.message
        });
    }
});


// =========================================================
// 3. RECHAZAR SOLICITUD
// PUT /solicitudes-intercambio/:id/rechazar
// =========================================================
router.put('/:id/rechazar', async (req, res) => {
    try {
        const solicitudId = req.params.id;

        // Actualizar estado a 'Rechazada'
        await pool.query(
            'CALL sp_ActualizarEstadoSolicitud(?, ?)',
            [solicitudId, 'Rechazada']
        );

        res.json({
            success: true,
            message: 'Solicitud rechazada'
        });

    } catch (error) {
        console.error('Error al rechazar solicitud:', error);
        res.status(500).json({
            success: false,
            message: 'Error al rechazar la solicitud',
            error: error.message
        });
    }
});


// =========================================================
// 4. CANCELAR SOLICITUD (por el solicitante)
// PUT /solicitudes-intercambio/:id/cancelar
// =========================================================
router.put('/:id/cancelar', async (req, res) => {
    try {
        const solicitudId = req.params.id;

        // Actualizar estado a 'Cancelada'
        await pool.query(
            'CALL sp_ActualizarEstadoSolicitud(?, ?)',
            [solicitudId, 'Cancelada']
        );

        res.json({
            success: true,
            message: 'Solicitud cancelada exitosamente'
        });

    } catch (error) {
        console.error('Error al cancelar solicitud:', error);
        res.status(500).json({
            success: false,
            message: 'Error al cancelar la solicitud',
            error: error.message
        });
    }
});


// =========================================================
// 5. ELIMINAR SOLICITUD
// DELETE /solicitudes-intercambio/:id
// =========================================================
router.delete('/:id', async (req, res) => {
    try {
        const solicitudId = req.params.id;

        await pool.query(
            'CALL sp_EliminarSolicitud(?)',
            [solicitudId]
        );

        res.json({
            success: true,
            message: 'Solicitud eliminada exitosamente'
        });

    } catch (error) {
        console.error('Error al eliminar solicitud:', error);
        res.status(500).json({
            success: false,
            message: 'Error al eliminar la solicitud',
            error: error.message
        });
    }
});


// =========================================================
// 6. OBTENER TODAS LAS SOLICITUDES DE UN USUARIO
// GET /solicitudes-intercambio/usuario/:id
// Retorna solicitudes enviadas Y recibidas
// =========================================================
router.get('/usuario/:id', async (req, res) => {
    try {
        const personaId = req.params.id;

        const [results] = await pool.query(
            'CALL sp_ObtenerSolicitudesPorPersona(?)',
            [personaId]
        );

        // Los stored procedures devuelven un array de arrays
        const solicitudes = results[0];

        res.json({
            success: true,
            data: solicitudes
        });

    } catch (error) {
        console.error('Error al obtener solicitudes:', error);
        res.status(500).json({
            success: false,
            message: 'Error al obtener las solicitudes',
            error: error.message
        });
    }
});


// =========================================================
// 7. OBTENER SOLICITUDES RECIBIDAS PENDIENTES
// GET /solicitudes-intercambio/recibidas/:id
// Solo las solicitudes que el usuario ha RECIBIDO y están PENDIENTES
// =========================================================
router.get('/recibidas/:id', async (req, res) => {
    try {
        const personaId = req.params.id;

        const [results] = await pool.query(
            'CALL sp_ObtenerSolicitudesPorPersona(?)',
            [personaId]
        );

        const todasSolicitudes = results[0];

        // Filtrar solo las recibidas y pendientes
        const solicitudesRecibidas = todasSolicitudes.filter(
            s => s.id_receptor === parseInt(personaId) && s.estado === 'Pendiente'
        );

        res.json({
            success: true,
            count: solicitudesRecibidas.length,
            data: solicitudesRecibidas
        });

    } catch (error) {
        console.error('Error al obtener solicitudes recibidas:', error);
        res.status(500).json({
            success: false,
            message: 'Error al obtener solicitudes recibidas',
            error: error.message
        });
    }
});


// =========================================================
// 8. OBTENER SOLICITUDES ENVIADAS PENDIENTES
// GET /solicitudes-intercambio/enviadas/:id
// Solo las solicitudes que el usuario ha ENVIADO y están PENDIENTES
// =========================================================
router.get('/enviadas/:id', async (req, res) => {
    try {
        const personaId = req.params.id;

        const [results] = await pool.query(
            'CALL sp_ObtenerSolicitudesPorPersona(?)',
            [personaId]
        );

        const todasSolicitudes = results[0];

        // Filtrar solo las enviadas y pendientes
        const solicitudesEnviadas = todasSolicitudes.filter(
            s => s.id_solicitante === parseInt(personaId) && s.estado === 'Pendiente'
        );

        res.json({
            success: true,
            count: solicitudesEnviadas.length,
            data: solicitudesEnviadas
        });

    } catch (error) {
        console.error('Error al obtener solicitudes enviadas:', error);
        res.status(500).json({
            success: false,
            message: 'Error al obtener solicitudes enviadas',
            error: error.message
        });
    }
});


module.exports = router;
