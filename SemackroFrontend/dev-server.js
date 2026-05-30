// Servidor de desarrollo SOLO para el frontend SEMACKRO
// NO usar en producción - Solo para desarrollo local
// Ejecutar: node dev-server.js

const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 5050;

// Servir archivos estáticos del directorio actual
app.use(express.static(__dirname));

// Sistema de rutas centralizado con layout principal
app.use((req, res, next) => {
    const route = req.path;

    // Excluir rutas de API y archivos estáticos
    if (route.startsWith('/api') || path.extname(route)) {
        return next();
    }

    // Mapeo de rutas a vistas (para el sistema SPA)
    const routeToView = {
        '/': 'descubrir',
        '/descubrir': 'descubrir',
        '/perfil': 'perfil',
        '/reportes': 'reportes',
        '/favoritos': 'favoritos',
        '/mis-postulaciones': 'mis-postulaciones',
        '/mis-intercambios': 'mis-intercambios',
        '/mis-solicitudes': 'mis-solicitudes',
        '/mensajes': 'mensajes',
        '/solicitudes-enviadas': 'solicitudesEnviadas',
        '/solicitudesEnviadas': 'solicitudesEnviadas',
        '/ordenes-trabajo': 'ordenesTrabajo',
        '/ordenesTrabajo': 'ordenesTrabajo',
        '/historial': 'historial',
        '/busqueda': 'busqueda',
        '/solicitud-intercambio': 'solicitud',
        '/video-llamada': 'videoLlamada'
    };

    const viewName = routeToView[route];

    if (viewName) {
        // Siempre servir Descubrir.html como layout principal
        const layoutPath = path.join(__dirname, 'Descubrir.html');
        
        fs.readFile(layoutPath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error leyendo Descubrir.html:', err);
                return next();
            }

            // Agregar script para navegar a la vista correcta al cargar
            const scriptInjection = `
                <script>
                    (function() {
                        // Esperar a que navigateTo esté disponible
                        function navigateToView() {
                            if (typeof navigateTo === 'function') {
                                navigateTo('${viewName}');
                            } else {
                                // Si navigateTo no está disponible aún, reintentar
                                setTimeout(navigateToView, 100);
                            }
                        }
                        
                        // Navegar cuando el DOM esté listo
                        if (document.readyState === 'loading') {
                            document.addEventListener('DOMContentLoaded', navigateToView);
                        } else {
                            navigateToView();
                        }
                    })();
                </script>
            `;

            // Insertar el script antes del cierre del body
            const modifiedHtml = data.replace('</body>', scriptInjection + '</body>');
            res.send(modifiedHtml);
        });
    } else {
        next();
    }
});

// Página 404 personalizada
app.use((req, res) => {
    res.status(404).sendFile(path.join(__dirname, '404.html'));
});

app.listen(port, () => {
    console.log(`🚀 Servidor de desarrollo frontend corriendo en http://localhost:${port}`);
    console.log(`📁 Sirviendo archivos de: ${__dirname}`);
    console.log(`⚠️  SOLO para desarrollo - NO usar en producción`);
    console.log(`🔗 Backend API disponible en: http://localhost:3001/api`);
    console.log(`📋 Rutas centralizadas con layout principal: /, /descubrir, /perfil, /reportes, /favoritos, /mensajes, /solicitudes-enviadas, /ordenes-trabajo, /historial, /busqueda, /solicitud-intercambio, /video-llamada`);
});
