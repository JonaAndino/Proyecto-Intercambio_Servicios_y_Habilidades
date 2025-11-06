// server.js

// 0. Configuración del Entorno (DEBE IR PRIMERO)
require('dotenv').config(); 

// 1. Importaciones de Librerías
const express = require('express');
const cors = require('cors'); 
// Asegúrate de que esta línea exista si usas las rutas de autenticación
const authRoutes = require('./routes/auth'); 

const app = express();
app.use(cors({
    // El frontend ahora corre en el puerto 5500 gracias a Live Server
    origin: 'http://127.0.0.1:5500' 
}));

app.use(cors());
app.use(express.json());

// 4. Configurar la URL base para las rutas de autenticación
app.use('/api', authRoutes);

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