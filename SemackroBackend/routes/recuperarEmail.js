const express = require('express');
const router = express.Router();
const db = require('../db');
const { enviarCorreoUsuarioRecuperado } = require('../config/email');

// ==========================================
// RUTA: Solicitar recuperación de correo (Público)
// POST /api/recuperar-email/solicitar
// ==========================================
router.post('/solicitar', async (req, res) => {
    const { nombre, identidad } = req.body;

    if (!nombre || !identidad) {
        return res.status(400).json({ 
            success: false, 
            error: 'El nombre completo y número de identidad son requeridos.' 
        });
    }

    const nombreTrim = nombre.trim();
    const identidadTrim = identidad.trim();

    try {
        // Evitar duplicados con estado "Pendiente" para el mismo DNI
        const [existe] = await db.query(
            'SELECT id_solicitud FROM solicitudes_recuperacion_email WHERE identidad_ingresada = ? AND estado = "Pendiente"',
            [identidadTrim]
        );

        if (existe && existe.length > 0) {
            return res.status(409).json({ 
                success: false, 
                error: 'Ya tienes una solicitud de recuperación pendiente de revisión. El administrador la atenderá pronto.' 
            });
        }

        // Insertar registro en la tabla soporte
        await db.query(
            'INSERT INTO solicitudes_recuperacion_email (nombre_ingresado, identidad_ingresada) VALUES (?, ?)',
            [nombreTrim, identidadTrim]
        );

        return res.status(201).json({ 
            success: true, 
            mensaje: 'Tu solicitud de recuperación ha sido enviada al administrador exitosamente.' 
        });
    } catch (error) {
        console.error('Error al registrar solicitud de recuperación de correo:', error.message);
        return res.status(500).json({ 
            success: false, 
            error: 'Error interno en el servidor al guardar la solicitud.' 
        });
    }
});

// ==========================================
// RUTA: Listar todas las solicitudes con JOINs (Administrador)
// GET /api/recuperar-email/solicitudes
// ==========================================
router.get('/solicitudes', async (req, res) => {
    try {
        // Hacemos el JOIN con Personas y Usuarios como solicitó el usuario, usando REPLACE para guiones.
        const [rows] = await db.query(`
            SELECT 
                s.id_solicitud,
                s.nombre_ingresado,
                s.identidad_ingresada,
                s.fecha_solicitud,
                s.estado,
                p.id_Perfil_Persona,
                p.nombre_Persona,
                p.apellido_Persona,
                p.identificacion_Persona,
                u.id_usuario,
                u.correo AS correo_usuario,
                u.activo AS usuario_activo
            FROM solicitudes_recuperacion_email s
            LEFT JOIN Personas p ON REPLACE(p.identificacion_Persona, '-', '') = REPLACE(s.identidad_ingresada, '-', '')
            LEFT JOIN Usuarios u ON p.id_Usuario = u.id_usuario
            ORDER BY s.fecha_solicitud DESC
        `);

        return res.status(200).json({
            success: true,
            data: rows
        });
    } catch (error) {
        console.error('Error al obtener solicitudes de recuperación de correo:', error.message);
        return res.status(500).json({ 
            success: false, 
            error: 'Error interno en el servidor al obtener las solicitudes.' 
        });
    }
});

// ==========================================
// RUTA: Actualizar estado de solicitud (Administrador)
// PUT /api/recuperar-email/solicitudes/:id
// ==========================================
router.put('/solicitudes/:id', async (req, res) => {
    const { id } = req.params;
    const { estado } = req.body;

    if (!estado) {
        return res.status(400).json({ success: false, error: 'Falta especificar el estado de la solicitud.' });
    }

    try {
        const [result] = await db.query(
            'UPDATE solicitudes_recuperacion_email SET estado = ? WHERE id_solicitud = ?',
            [estado, id]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({ success: false, error: 'La solicitud especificada no existe.' });
        }

        return res.status(200).json({ success: true, mensaje: 'Estado de la solicitud actualizado correctamente.' });
    } catch (error) {
        console.error('Error al actualizar solicitud de recuperación de correo:', error.message);
        return res.status(500).json({ success: false, error: 'Error al actualizar la solicitud en la base de datos.' });
    }
});

// ==========================================
// RUTA: Eliminar una solicitud (Administrador)
// DELETE /api/recuperar-email/solicitudes/:id
// ==========================================
router.delete('/solicitudes/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [result] = await db.query(
            'DELETE FROM solicitudes_recuperacion_email WHERE id_solicitud = ?',
            [id]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({ success: false, error: 'La solicitud especificada no existe.' });
        }

        return res.status(200).json({ success: true, mensaje: 'Solicitud de soporte eliminada correctamente.' });
    } catch (error) {
        console.error('Error al eliminar solicitud de recuperación de correo:', error.message);
        return res.status(500).json({ success: false, error: 'Error al eliminar la solicitud de la base de datos.' });
    }
});

// ==========================================
// RUTA: Enviar usuario por correo (Administrador)
// POST /api/recuperar-email/enviar-usuario
// ==========================================
router.post('/enviar-usuario', async (req, res) => {
    const { id_solicitud } = req.body;

    if (!id_solicitud) {
        return res.status(400).json({ success: false, error: 'Falta especificar el id de la solicitud.' });
    }

    try {
        // Obtener la solicitud con el DNI y los datos cruzados de la persona/usuario
        const [rows] = await db.query(`
            SELECT 
                s.id_solicitud,
                s.nombre_ingresado,
                s.identidad_ingresada,
                s.fecha_solicitud,
                s.estado,
                p.nombre_Persona,
                p.apellido_Persona,
                u.correo AS correo_usuario
            FROM solicitudes_recuperacion_email s
            LEFT JOIN Personas p ON REPLACE(p.identificacion_Persona, '-', '') = REPLACE(s.identidad_ingresada, '-', '')
            LEFT JOIN Usuarios u ON p.id_Usuario = u.id_usuario
            WHERE s.id_solicitud = ?
        `, [id_solicitud]);

        if (!rows || rows.length === 0) {
            return res.status(404).json({ success: false, error: 'La solicitud de recuperación no existe.' });
        }

        const solicitud = rows[0];

        if (!solicitud.correo_usuario) {
            return res.status(400).json({ 
                success: false, 
                error: 'No se encontró ningún correo registrado asociado al DNI de esta solicitud.' 
            });
        }

        const nombreDestinatario = (solicitud.nombre_Persona || solicitud.apellido_Persona)
            ? `${solicitud.nombre_Persona || ''} ${solicitud.apellido_Persona || ''}`.trim()
            : solicitud.nombre_ingresado;

        const emailDestinatario = String(solicitud.correo_usuario || '').trim();

        // 1. Enviar respuesta exitosa instantánea al frontend indicando que se inició el proceso
        res.status(200).json({ 
            success: true, 
            mensaje: 'El envío de correo se ha iniciado en segundo plano. La tabla se actualizará automáticamente con el estado definitivo.'
        });

        // 2. Enviar el correo en segundo plano para evitar bloqueos por lentitud o latencia de red SMTP
        setImmediate(async () => {
            const startedAt = Date.now();
            try {
                console.log(`[admin-recovery-email] Iniciando envío en segundo plano para ${emailDestinatario}`);
                const emailResult = await enviarCorreoUsuarioRecuperado(
                    emailDestinatario,
                    nombreDestinatario,
                    emailDestinatario
                );
                if (emailResult.success) {
                    console.log(`[admin-recovery-email] Enviado con éxito a ${emailDestinatario} en ${Date.now() - startedAt}ms (messageId=${emailResult.messageId})`);
                    // Actualizar a Resuelta
                    await db.query(
                        'UPDATE solicitudes_recuperacion_email SET estado = "Resuelta" WHERE id_solicitud = ?',
                        [id_solicitud]
                    );
                } else {
                    console.error(`[admin-recovery-email] Falló envío a ${emailDestinatario} en ${Date.now() - startedAt}ms: ${emailResult.error}`);
                    // Actualizar a Error al enviar
                    await db.query(
                        'UPDATE solicitudes_recuperacion_email SET estado = "Error al enviar" WHERE id_solicitud = ?',
                        [id_solicitud]
                    );
                }
            } catch (err) {
                console.error(`[admin-recovery-email] Error inesperado en segundo plano para ${emailDestinatario}:`, err.message);
                try {
                    await db.query(
                        'UPDATE solicitudes_recuperacion_email SET estado = "Error al enviar" WHERE id_solicitud = ?',
                        [id_solicitud]
                    );
                } catch (dbErr) {
                    console.error('[admin-recovery-email] Error al actualizar estado a error en base de datos:', dbErr.message);
                }
            }
        });

    } catch (error) {
        console.error('Error al procesar envío de correo de recuperación:', error.message);
        return res.status(500).json({ 
            success: false, 
            error: 'Error interno en el servidor al enviar el correo de recuperación.' 
        });
    }
});

module.exports = router;
