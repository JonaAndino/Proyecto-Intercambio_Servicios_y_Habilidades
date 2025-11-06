const calificacionesRouter = requiere ('./routes/calificaciones');
const notificaciones = requiere ('./routes/notificaciones');
//import calificacionesRoutes from "./routes/calificaciones.js";

app.use("/calificaciones", calificacionesRoutes);
app.use("/notificaciones", notificacionesRoutes);