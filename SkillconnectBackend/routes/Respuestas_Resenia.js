const express = require('express');
const router = express.Router();
const db = require('../db');

// Endpoint: Insertar respuesta
router.post('/insertar', async (req, res) => {
	const { id_calificacion, id_usuario, respuesta } = req.body;
	console.debug('POST /api/respuestas-resenia/insertar body:', req.body);
	if (!id_calificacion || !id_usuario || !respuesta) {
		return res.status(400).json({ success: false, message: 'Faltan datos requeridos.' });
	}
	try {
		await db.query('CALL InsertarRespuestaResena(?, ?, ?)', [id_calificacion, id_usuario, respuesta]);
		res.json({ success: true, message: 'Respuesta insertada correctamente.' });
	} catch (err) {
		console.error('Error en InsertarRespuestaResena:', err);
		res.status(500).json({ success: false, message: 'Error al insertar respuesta.', error: err.message || err });
	}
});

// Endpoint: Obtener respuestas por reseña
router.get('/por-resena/:id_calificacion', async (req, res) => {
	const { id_calificacion } = req.params;
	console.debug('GET /api/respuestas-resenia/por-resena params:', req.params);
	try {
		const result = await db.query('CALL ObtenerRespuestasPorResena(?)', [id_calificacion]);
		console.debug('Resultado ObtenerRespuestasPorResena:', result);
		// MySQL CALL returns an array; try to find the rows
		let rows = [];
		if (Array.isArray(result)) {
			// If stored procedure returns multiple result sets
			rows = result[0] || [];
		} else if (result && result[0]) {
			rows = result[0];
		}
		res.json({ success: true, data: rows });
	} catch (err) {
		console.error('Error en ObtenerRespuestasPorResena:', err);
		res.status(500).json({ success: false, message: 'Error al obtener respuestas.', error: err.message || err });
	}
});

// Endpoint: Eliminar (ocultar) respuesta
router.delete('/eliminar/:id_respuesta', async (req, res) => {
	const { id_respuesta } = req.params;
	console.debug('DELETE /api/respuestas-resenia/eliminar id_respuesta=', id_respuesta);
	try {
		await db.query('CALL EliminarRespuestaResena(?)', [id_respuesta]);
		res.json({ success: true, message: 'Respuesta eliminada correctamente.' });
	} catch (err) {
		console.error('Error en EliminarRespuestaResena:', err);
		res.status(500).json({ success: false, message: 'Error al eliminar respuesta.', error: err.message || err });
	}
});

module.exports = router;
