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

const app = express();
// Obtiene el puerto del .env o usa 3001 por defecto
const port = process.env.PORT || 3001; 

// 2. Middleware de CORS (Permite al frontend hablar con el backend)
app.use(cors({
    // Permitir múltiples orígenes para desarrollo
    origin: ['http://127.0.0.1:5500', 'http://localhost:5500', 'http://127.0.0.1:5050', 'http://localhost:3000'],
    credentials: true
}));

// 3. Middleware para procesar JSON (SOLO UNA VEZ)
app.use(express.json()); 

// 4. Configurar sesiones para Passport
app.use(session({
    secret: process.env.SESSION_SECRET || 'tu_secreto_de_sesion_super_seguro_2025',
    resave: false,
    saveUninitialized: false,
    cookie: { 
        secure: false, // En producción debe ser true con HTTPS
        maxAge: 24 * 60 * 60 * 1000 // 24 horas
    }
}));

// 5. Inicializar Passport
app.use(passport.initialize());
app.use(passport.session());

// 6. Configurar las rutas
app.use('/api', authRoutes);
app.use('/api/auth', authGoogleRoutes); // Rutas de Google OAuth
app.use('/api',loginRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/personas', personasRoutes);
    const respuestasReseniaRoutes = require('./routes/Respuestas_Resenia');
    const notificacionesRoutes = require('./routes/notificaciones_reseñas');
app.use('/api/habilidades', habilidadesRoutes);
app.use('/api/direcciones', direccionesRoutes);
app.use('/api/categorias', categoriasRoutes);
app.use('/api/geolocalizacion', geolocalizacionRoutes);
app.use('/api/solicitudes-intercambio', solicitudesRoutes);
app.use('/api/mensajeria', mensajeriaRoutes);
app.use('/api/password', recuperarPasswordRoutes); // Rutas de recuperación de contraseña
app.use('/api/favoritos', favoritosRoutes); // Rutas de favoritos
app.use('/api/intercambios', intercambiosRoutes); // Rutas de intercambios finalizados y calificaciones

// Rutas de verificación de usuarios
app.use('/api/verificacion-usuarios', verificacionUsuariosRoutes);
// Rutas para reportes de usuarios (crear/listar/actualizar/eliminar)
app.use('/api/reportes', reportesUsuariosRoutes);

// Prueba básica de que el servidor Express funciona
app.get('/', (req, res) => {
    res.send('Servidor Skill Connect Activo!');
});

// Servir archivos estáticos del frontend (SkillconnectFrontend)
// Colocamos un middleware que añade una cabecera Content-Security-Policy
    app.use('/api/respuestas-resenia', respuestasReseniaRoutes); // Rutas de respuestas a reseñas
app.use('/api/notificaciones', notificacionesRoutes); // Rutas de notificaciones (notificaciones_reseñas)
// razonable para desarrollo antes de servir los archivos estáticos, porque
// algunos servidores/entornos envían por defecto "default-src 'none'" y eso
// bloquea fuentes externas (Google Fonts) y hojas de estilo.
const frontendPath = path.join(__dirname, '..', 'SkillconnectFrontend');

// Middleware para establecer CSP (relajada para desarrollo). Ajusta según
// seguridad en producción.
app.use('/SkillconnectFrontend', (req, res, next) => {
    // Política de ejemplo: permite recursos propios, fuentes/estilos de Google
    // y datos en-linea para facilitar desarrollo local.
    const csp = "default-src 'self' data:; " +
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; " +
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
                "font-src 'self' https://fonts.gstatic.com data:; " +
                "img-src 'self' data: https:; " +
                "connect-src 'self' http://127.0.0.1:5050 http://localhost:5050 ws:;";
    res.setHeader('Content-Security-Policy', csp);
    next();
});

// Servir estáticos (index por defecto)
app.use('/SkillconnectFrontend', express.static(frontendPath, { index: 'index.html' }));

// Si la petición comienza con /SkillconnectFrontend y no se encontró un archivo,
// devolvemos la página 404 personalizada del frontend.
app.use('/SkillconnectFrontend', (req, res) => {
    res.status(404).sendFile(path.join(frontendPath, '404.html'));
});

// 5. Iniciar el servidor
app.listen(port, () => {
    // Asegúrate de que el db.js se importe y ejecute su conexión de prueba
    require('./db');
    console.log(`Servidor escuchando en http://localhost:${port}`);
});