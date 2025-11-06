// server.js

// 0. Configuración del Entorno (DEBE IR PRIMERO)
require('dotenv').config(); 

// 1. Importaciones de Librerías
const express = require('express');
const cors = require('cors'); 
const session = require('express-session');
const passport = require('./config/passport');

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
app.use('/api/habilidades', habilidadesRoutes);
app.use('/api/direcciones', direccionesRoutes);
app.use('/api/categorias', categoriasRoutes);
app.use('/api/geolocalizacion', geolocalizacionRoutes);
app.use('/api/solicitudes-intercambio', solicitudesRoutes);
app.use('/api/mensajeria', mensajeriaRoutes);
app.use('/api/password', recuperarPasswordRoutes); // Rutas de recuperación de contraseña

// Prueba básica de que el servidor Express funciona
app.get('/', (req, res) => {
    res.send('Servidor Skill Connect Activo!');
});

// 5. Iniciar el servidor
app.listen(port, () => {
    // Asegúrate de que el db.js se importe y ejecute su conexión de prueba
    require('./db');
    console.log(`Servidor escuchando en http://localhost:${port}`);
});