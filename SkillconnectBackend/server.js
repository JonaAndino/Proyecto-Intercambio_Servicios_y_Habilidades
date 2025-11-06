// server.js

// 1️⃣ Dependencias principales
import express from "express";
import cors from 'cors';
import db from './db.js'; // usa el pool de conexiones de tu db.js

import calificacionesRouter from './routes/calificaciones.js';
import notificacionesRouter from './routes/notificaciones.js';
import authRouter from './routes/auth.js';

// 3️⃣ Configurar la app
const app = express();
app.use(cors({
    origin: '*', // Permite peticiones desde cualquier origen (Incluyendo tu HTML local)
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(cors());
app.use(express.json());

app.use('/api/calificaciones', calificacionesRouter); 
app.use('/api/notificaciones', notificacionesRouter); 
app.use('/api/auth', authRouter);

// 4️⃣ Probar conexión a la base de datos
db.query("SELECT 1")
  .then(() => console.log(" Base de datos conectada correctamente."))
  .catch((err) => console.error(" Error al conectar con la base de datos:", err));


// 6️⃣ Ruta base para probar el servidor
app.get("/", (req, res) => {
  res.send("🌟 API de SkillConnect funcionando correctamente");
});

/// 7️⃣ Iniciar servidor
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log( `Servidor corriendo en http://localhost:${PORT}`);




});