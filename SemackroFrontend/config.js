// Configuración global de URLs — PRODUCCIÓN
(function() {
    const API_BASE_URL = 'https://tu-backend.railway.app'; // Reemplazar con tu URL de Railway/Render

    window.APP_CONFIG = {
        BACKEND_URL: API_BASE_URL,
        API_BASE:    `${API_BASE_URL}/api`,
        HF_API_URL:  'https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2'
    };

    window.BACKEND_URL = window.APP_CONFIG.BACKEND_URL;
    window.API_BASE    = window.APP_CONFIG.API_BASE;
    window.HF_API_URL  = window.APP_CONFIG.HF_API_URL;
    window.safeFetch = (url, options) => fetch(url, options);
})();
