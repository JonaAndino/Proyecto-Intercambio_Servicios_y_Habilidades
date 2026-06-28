const express = require('express');
const router = express.Router();

// Usamos el fetch nativo de Node.js (disponible en Node 18+)
const fetchApi = fetch;
router.post('/', async (req, res) => {
    try {
        const { text, targetLang } = req.body;

        if (!text) {
            return res.status(400).json({ error: 'El texto está vacío.' });
        }

        const apiKey = process.env.DEEPL_API_KEY || 'db4d7897-e94b-4b09-86c4-eb0eb1bd9cc8:fx';
        
        // Configurar la petición hacia los servidores de DeepL (API Free)
        const url = "https://api-free.deepl.com/v2/translate";
        
        const params = new URLSearchParams();
        params.append('text', text);
        params.append('target_lang', targetLang || 'EN');

        const response = await fetchApi(url, {
            method: 'POST',
            headers: {
                'Authorization': `DeepL-Auth-Key ${apiKey}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error de DeepL:', errorText);
            return res.status(response.status).json({ error: 'Error al conectar con el servicio de traducción.' });
        }

        const data = await response.json();
        return res.json(data);
    } catch (error) {
        console.error("Error en /api/translate:", error);
        return res.status(500).json({ error: 'Error interno del servidor en la traducción.' });
    }
});

module.exports = router;
