// server.js

// 0. Configuración del Entorno (DEBE IR PRIMERO)
require('dotenv').config(); 

// 1. Importaciones de Librerías
const express = require('express');
const cors = require('cors'); 
const session = require('express-session');
const passport = require('./config/passport');
const path = require('path');

// Importar rutas
const authRoutes = require('./routes/auth');
const authGoogleRoutes = require('./routes/authGoogle');
const loginRoutes = require('./routes/Login');
const uploadRoutes = require('./routes/upload');
const personasRoutes = require('./routes/Personas');
const habilidadesRoutes = require('./routes/HabilidadesYServicios_Persona');
const direccionesRoutes = require('./routes/Direcciones');
const categoriasRoutes = require('./routes/CategoriasGeneralesHabilidades');
const geolocalizacionRoutes = require('./routes/Geolocalizacion');
const solicitudesRoutes = require('./routes/SolicitudesIntercambio');
const mensajeriaRoutes = require('./routes/Mensajeria');
const recuperarPasswordRoutes = require('./routes/recuperarPassword');
const favoritosRoutes = require('./routes/favoritos');
const intercambiosRoutes = require('./routes/intercambios');
const verificacionUsuariosRoutes = require('./routes/verificacionUsuarios');
const reportesUsuariosRoutes = require('./routes/ReportesUsuarios');
const respuestasReseniaRoutes = require('./routes/Respuestas_Resenia');
const notificacionesRoutes = require('./routes/notificaciones_reseñas');

// 2. Crear instancia de Express
const app = express();

// 3. Definir el puerto (CRÍTICO - FALTABA ESTO)
const port = process.env.PORT || 3001;

// 4. Configurar CORS
app.use(cors({
    // Permitir múltiples orígenes para desarrollo
    origin: ['http://127.0.0.1:5500', 'http://localhost:5500', 'http://127.0.0.1:5050', 'http://localhost:3000', 'http://localhost:3001'],
    credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 5. Configurar sesiones para Passport
app.use(session({
    secret: process.env.SESSION_SECRET || 'tu_secreto_de_sesion_super_seguro_2025',
    resave: false,
    saveUninitialized: false,
    cookie: { 
        secure: false, // En producción debe ser true con HTTPS
        maxAge: 24 * 60 * 60 * 1000 // 24 horas
    }
}));

// 6. Inicializar Passport
app.use(passport.initialize());
app.use(passport.session());

// 7. Configurar las rutas
app.use('/api', authRoutes);
app.use('/api/auth', authGoogleRoutes); // Rutas de Google OAuth
app.use('/api', loginRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/personas', personasRoutes);
app.use('/api/habilidades', habilidadesRoutes);
app.use('/api/direcciones', direccionesRoutes);
app.use('/api/categorias', categoriasRoutes);
app.use('/api/geolocalizacion', geolocalizacionRoutes);
app.use('/api/solicitudes-intercambio', solicitudesRoutes);
app.use('/api/mensajeria', mensajeriaRoutes);
app.use('/api/password', recuperarPasswordRoutes); // Rutas de recuperación de contraseña
app.use('/api/favoritos', favoritosRoutes); // Rutas de favoritos
app.use('/api/intercambios', intercambiosRoutes); // Rutas de intercambios finalizados y calificaciones
app.use('/api/verificacion-usuarios', verificacionUsuariosRoutes); // Rutas de verificación de usuarios
app.use('/api/reportes', reportesUsuariosRoutes); // Rutas para reportes de usuarios
app.use('/api/respuestas-resenia', respuestasReseniaRoutes); // Rutas de respuestas a reseñas
app.use('/api/notificaciones', notificacionesRoutes); // Rutas de notificaciones

// 8. Prueba básica de que el servidor Express funciona
app.get('/', (req, res) => {
    res.send('Servidor Skill Connect Activo! 🚀');
});

// 9. Servir archivos estáticos del frontend (SkillconnectFrontend)
const frontendPath = path.join(__dirname, '..', 'SkillconnectFrontend');

// Middleware para establecer CSP (relajada para desarrollo)
app.use('/SkillconnectFrontend', (req, res, next) => {
    // Política de ejemplo: permite recursos propios, fuentes/estilos de Google
    // CSP relajada para desarrollo: permitimos recursos propios y datos,
    // especificamos `img-src` y `media-src` para permitir reproducción desde
    // Cloudflare R2 (si está configurado en R2_PUBLIC_URL) y previews `blob:`/`data:`.
    let r2Host = process.env.R2_PUBLIC_URL || 'https:';
    try { r2Host = new URL(r2Host).origin; } catch (e) { /* dejar r2Host tal cual si no es URL */ }

    const csp = "default-src 'self' data:; " +
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; " +
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
                "font-src 'self' https://fonts.gstatic.com data:; " +
                "img-src 'self' data: blob: https: " + r2Host + "; " +
                "media-src 'self' data: blob: " + r2Host + "; " +
                "connect-src 'self' http://127.0.0.1:5050 http://localhost:5050 http://127.0.0.1:3001 http://localhost:3001 ws: https://cdn.jsdelivr.net;";
    res.setHeader('Content-Security-Policy', csp);
    next();
});

// Servir estáticos (index por defecto)
app.use('/SkillconnectFrontend', express.static(frontendPath, { index: 'index.html' }));

// Si la petición comienza con /SkillconnectFrontend y no se encontró un archivo,
// devolvemos la página 404 personalizada del frontend
app.use('/SkillconnectFrontend', (req, res) => {
    res.status(404).sendFile(path.join(frontendPath, '404.html'));
});

// 10. Manejo de errores global
app.use((err, req, res, next) => {
    console.error('Error del servidor:', err);
    res.status(err.status || 500).json({ 
        error: err.message || 'Error interno del servidor' 
    });
});

// 11. Iniciar el servidor
app.listen(port, () => {
    // Asegúrate de que el db.js se importe y ejecute su conexión de prueba
    require('./db');
    console.log(`✅ Servidor escuchando en http://localhost:${port}`);
    console.log(`🔗 Frontend disponible en http://localhost:${port}/SkillconnectFrontend`);
});