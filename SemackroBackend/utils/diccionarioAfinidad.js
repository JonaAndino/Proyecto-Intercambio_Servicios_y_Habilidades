/**
 * Diccionario de afinidad semántica para Postulaciones / Órdenes de trabajo.
 * Agrupa términos, habilidades y profesiones en "Categorías/Tags".
 * Si un usuario tiene una habilidad, se le inyectan todos los términos de su categoría
 * para mejorar los matches con órdenes de trabajo.
 */

const diccionario = {
    // --------------------------------------
    // TECNOLOGÍA Y DESARROLLO DE SOFTWARE
    // --------------------------------------
    "qa_testing": [
        "qa", "testing", "pruebas", "tester", "calidad de software", "automatización de pruebas", 
        "cypress", "selenium", "jest", "pruebas unitarias", "pruebas de software"
    ],
    "desarrollo_web": [
        "web", "frontend", "backend", "fullstack", "desarrollo web", "javascript", "html", "css", 
        "react", "angular", "vue", "node", "php", "laravel", "django"
    ],
    "bases_de_datos": [
        "base de datos", "bases de datos", "database", "bd", "sql", "mysql", "postgresql", 
        "oracle", "sql server", "nosql", "mongodb", "administrador de base de datos", "dba"
    ],
    "desarrollo_movil": [
        "movil", "móvil", "mobile", "app", "aplicación", "ios", "android", "flutter", 
        "react native", "kotlin", "swift"
    ],
    "diseno_ux_ui": [
        "diseño", "ui", "ux", "interfaz", "experiencia de usuario", "figma", "adobe xd", 
        "sketch", "diseñador", "diseño web"
    ],
    "soporte_redes": [
        "soporte", "mantenimiento", "redes", "infraestructura", "servidores", "linux", 
        "windows server", "cisco", "tecnico en sistemas", "técnico en computación"
    ],

    // --------------------------------------
    // CONSTRUCCIÓN, ARQUITECTURA Y OFICIOS
    // --------------------------------------
    "arquitectura_construccion": [
        "arquitectura", "arquitecto", "construcción", "planos", "obra", "albañil", 
        "albañilería", "maestro de obra", "diseño de interiores", "autocad", "revit", "civil"
    ],
    "electricidad": [
        "electricidad", "electricista", "cableado", "instalaciones eléctricas", 
        "tableros", "circuitos", "energía"
    ],
    "plomeria": [
        "plomería", "plomero", "fontanería", "fontanero", "tuberías", "agua", "fugas", "drenaje"
    ],
    "carpinteria": [
        "carpintería", "carpintero", "muebles", "madera", "ebanistería", "ebanista"
    ],
    "limpieza_mantenimiento": [
        "limpieza", "aseo", "mantenimiento", "jardinería", "jardinero", "conserje"
    ],

    // --------------------------------------
    // NEGOCIOS Y ADMINISTRACIÓN
    // --------------------------------------
    "marketing_ventas": [
        "marketing", "mercadeo", "ventas", "vendedor", "publicidad", "redes sociales", 
        "community manager", "seo", "sem", "comercial"
    ],
    "contabilidad_finanzas": [
        "contabilidad", "contador", "finanzas", "impuestos", "auditoría", "auditor", 
        "nómina", "administración financiera", "libros contables"
    ],
    "asistencia_administrativa": [
        "asistente", "secretaria", "administración", "oficinista", "recepcionista", 
        "archivo", "atención al cliente"
    ]
};

/**
 * Función que recibe un arreglo de habilidades de un usuario y devuelve
 * un arreglo expandido (sin duplicados) con todos los términos afines.
 * @param {string[]} habilidadesUsuario - Ej: ["Pruebas de software", "MySQL"]
 * @returns {string[]} - Ej: ["qa", "testing", "pruebas", "sql", "mysql", "bases de datos"...]
 */
function expandirHabilidades(habilidadesUsuario) {
    if (!habilidadesUsuario || habilidadesUsuario.length === 0) return [];
    
    const terminosEncontrados = new Set();

    // Normalizar habilidades entrantes
    const habilidadesNormalizadas = habilidadesUsuario.map(h => h.toLowerCase().trim());

    // Agregar las propias habilidades originales (por si no están en el diccionario)
    habilidadesNormalizadas.forEach(h => terminosEncontrados.add(h));

    // Revisar el diccionario
    for (const [categoria, terminos] of Object.entries(diccionario)) {
        // Chequear si alguna de las habilidades del usuario coincide parcial o totalmente
        // con algún término de esta categoría
        const coincide = habilidadesNormalizadas.some(habilidad => {
            return terminos.some(termino => 
                termino.includes(habilidad) || habilidad.includes(termino)
            );
        });

        if (coincide) {
            // Si el usuario es afín a esta categoría, agregamos todos los términos de la categoría
            terminos.forEach(t => terminosEncontrados.add(t.toLowerCase().trim()));
        }
    }

    return Array.from(terminosEncontrados);
}

module.exports = {
    diccionario,
    expandirHabilidades
};
