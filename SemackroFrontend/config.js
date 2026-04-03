// Configuración global de URLs
// Cuando se accede vía ngrok, usa el mismo origen → el servidor proxy reenvía al backend.
// Así el navegador nunca llama a localhost directamente → sin advertencias Chrome.
(function() {
    const hostname = window.location.hostname;
    const origin   = window.location.origin;  // e.g. https://xxxx.ngrok-free.dev
    const isLocal  = hostname === 'localhost' || hostname === '127.0.0.1';

    let backendUrl, apiBase;

    if (isLocal) {
        // Desarrollo local: acceso directo a localhost
        backendUrl = 'http://localhost:3001';
        apiBase    = 'http://localhost:3001/api';
        console.log('🏠 Entorno LOCAL — backend directo en localhost:3001');
    } else {
        // Ngrok u otro host: usar mismo origen → proxy interno del frontend
        backendUrl = origin;
        apiBase    = `${origin}/api`;
        console.log('🌐 Entorno REMOTO — usando proxy en:', origin);
    }

    window.APP_CONFIG = {
        BACKEND_URL: backendUrl,
        API_BASE:    apiBase,
        HF_API_URL:  'https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2'
    };

    // Compatibilidad con código existente
    window.BACKEND_URL = window.APP_CONFIG.BACKEND_URL;
    window.API_BASE    = window.APP_CONFIG.API_BASE;
    window.HF_API_URL  = window.APP_CONFIG.HF_API_URL;

    // safeFetch — ya no se necesita targetAddressSpace porque no hay requests a localhost
    window.safeFetch = (url, options) => fetch(url, options);

    console.log('📡 Backend URL:', window.BACKEND_URL);
})();

