const express = require('express');
const router = express.Router();

// Importar configuración centralizada de la base de datos
const db = require('../db');

// ----------------------------------------------------
// ENDPOINT: Obtener todas las categorías (GET /categorias)
// ----------------------------------------------------
router.get('/', async (req, res) => {
    try {
        const [resultado] = await db.execute('CALL sp_Categorias_ObtenerTodo()');
        const categorias = resultado[0];
        
        res.json({
            success: true,
            data: categorias
        });
    } catch (error) {
        console.error('Error al obtener categorías:', error.message);
        res.status(500).json({ 
            success: false,
            error: 'Error del servidor al obtener las categorías'
        });
    }
});

// ----------------------------------------------------
// ENDPOINT: Obtener categoría por ID (GET /categorias/:id)
// ----------------------------------------------------
router.get('/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    
    if (isNaN(id)) {
        return res.status(400).json({ 
            success: false,
            message: 'ID no válido' 
        });
    }

    try {
        const [resultado] = await db.execute('CALL sp_Categorias_ObtenerPorId(?)', [id]);
        const categoria = resultado[0][0];
        
        if (!categoria) {
            return res.status(404).json({ 
                success: false,
                message: 'Categoría no encontrada' 
            });
        }
        
        res.json({
            success: true,
            data: categoria
        });
    } catch (error) {
        console.error(`Error al obtener categoría con ID ${id}:`, error.message);
        res.status(500).json({ 
            success: false,
            error: 'Error del servidor al obtener la categoría'
        });
    }
});

// ----------------------------------------------------
// ENDPOINT: Agregar una categoría (POST /categorias)
// ----------------------------------------------------
router.post('/', async (req, res) => {
    const { nombre } = req.body;
    
    if (!nombre || !nombre.trim()) {
        return res.status(400).json({ 
            success: false,
            message: 'El nombre de la categoría es requerido' 
        });
    }

    try {
        await db.execute(
            'INSERT INTO Categorias_Habilidades_Servicios (nombre_categoria_Habilidad) VALUES (?)',
            [nombre.trim()]
        );
        
        res.json({
            success: true,
            message: 'Categoría agregada correctamente'
        });
    } catch (error) {
        console.error('Error al agregar categoría:', error.message);
        res.status(500).json({ 
            success: false,
            error: 'Error del servidor al agregar la categoría'
        });
    }
});

// ----------------------------------------------------
// ENDPOINT: Actualizar una categoría (PUT /categorias/:id)
// ----------------------------------------------------
router.put('/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    const { nombre } = req.body;
    
    if (isNaN(id)) {
        return res.status(400).json({ 
            success: false,
            message: 'ID no válido' 
        });
    }

    if (!nombre || !nombre.trim()) {
        return res.status(400).json({ 
            success: false,
            message: 'El nombre de la categoría es requerido' 
        });
    }

    try {
        await db.execute(
            'UPDATE Categorias_Habilidades_Servicios SET nombre_categoria_Habilidad = ? WHERE id_categoria_Habilidad_Servicio = ?',
            [nombre.trim(), id]
        );
        
        res.json({
            success: true,
            message: 'Categoría actualizada correctamente'
        });
    } catch (error) {
        console.error('Error al actualizar categoría:', error.message);
        res.status(500).json({ 
            success: false,
            error: 'Error del servidor al actualizar la categoría'
        });
    }
});

// ----------------------------------------------------
// ENDPOINT: Eliminar una categoría (DELETE /categorias/:id)
// ----------------------------------------------------
router.delete('/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    
    if (isNaN(id)) {
        return res.status(400).json({ 
            success: false,
            message: 'ID no válido' 
        });
    }

    try {
        await db.execute(
            'DELETE FROM Categorias_Habilidades_Servicios WHERE id_categoria_Habilidad_Servicio = ?',
            [id]
        );
        
        res.json({
            success: true,
            message: 'Categoría eliminada correctamente'
        });
    } catch (error) {
        console.error('Error al eliminar categoría:', error.message);
        res.status(500).json({ 
            success: false,
            error: 'Error del servidor al eliminar la categoría'
        });
    }
});

module.exports = router;
