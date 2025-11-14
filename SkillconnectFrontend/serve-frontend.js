// Pequeño servidor estático sin dependencias externas
// Uso: desde PowerShell en la carpeta SkillconnectFrontend:
// $env:PORT = "5050"; node serve-frontend.js

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 5050;
const PUBLIC_DIR = __dirname; // sirve archivos desde esta carpeta
// Entrada SPA preferida: si existe `Descubrir.html` la usamos como entry, sino `index.html`
const SPA_ENTRY = fs.existsSync(path.join(PUBLIC_DIR, 'Descubrir.html')) ? 'Descubrir.html' : 'index.html';

const mime = {
  '.html': 'text/html; charset=UTF-8',
  '.css': 'text/css; charset=UTF-8',
  '.js': 'application/javascript; charset=UTF-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
};

function sendFile(res, filePath, statusCode = 200) {
  const ext = path.extname(filePath).toLowerCase();
  const type = mime[ext] || 'application/octet-stream';
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=UTF-8' });
      return res.end('Error interno al leer archivo');
    }
    res.writeHead(statusCode, { 'Content-Type': type });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  try {
    // Cabecera CSP permisiva para DESARROLLO local (ajustar en producción)
   const csp = "default-src 'self' data:; " +
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https: https://unpkg.com https://cdnjs.cloudflare.com; " +
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com https://cdnjs.cloudflare.com; " +
            "font-src 'self' https://fonts.gstatic.com data:; " +
            "img-src 'self' data: https:; " +
            "connect-src 'self' http://127.0.0.1:3001 http://localhost:3001 ws: https://unpkg.com https://nominatim.openstreetmap.org https://*.tile.openstreetmap.org;";
    res.setHeader('Content-Security-Policy', csp);

    const decoded = decodeURIComponent(req.url.split('?')[0]);
    // Normalizar y prevenir traversal
    let safePath = path.normalize(decoded).replace(/^\/+/, '');
    // Si la petición tiene segmentos después de index.html (index.html/xxx)
    // tratamos como no encontrado y servimos 404.html
    if (/index\.html\/.+/.test(decoded)) {
      const notFound = path.join(PUBLIC_DIR, '404.html');
      if (fs.existsSync(notFound)) return sendFile(res, notFound, 404);
    }

    if (safePath === '') safePath = SPA_ENTRY;
    const filePath = path.join(PUBLIC_DIR, safePath);

    // Evitar salir del directorio público
    if (!filePath.startsWith(PUBLIC_DIR)) {
      res.writeHead(400, { 'Content-Type': 'text/plain; charset=UTF-8' });
      return res.end('Petición no válida');
    }

    fs.stat(filePath, (err, stats) => {
      if (!err && stats.isFile()) {
        return sendFile(res, filePath, 200);
      }

      // Determinar fallback para SPA: si la ruta solicitada no tiene extensión
      // (p.ej. /home, /perfil) devolvemos la entrada SPA (p.ej. Descubrir.html o index.html)
      const ext = path.extname(safePath);
      const entryFile = path.join(PUBLIC_DIR, SPA_ENTRY);
      const notFoundFile = path.join(PUBLIC_DIR, '404.html');

      if (!ext) {
        // Sólo permitir servir la SPA para rutas conocidas (sidebar views)
        const parts = safePath.split('/').filter(Boolean);
        const first = parts[0] || '';

        const allowedViews = new Set(['', 'home', 'descubrir', 'perfil', 'mensajes', 'solicitudesEnviadas', 'favoritos', 'configuracion', 'busqueda', 'solicitud']);

        // Normalizar nombre para comparación (lowercase)
        const firstNorm = first.toString().toLowerCase();

        // Helper para consultar al backend si un perfil existe
        function checkPersonaExists(idOrSlug, cb) {
          const backend = 'http://127.0.0.1:3001/api';
          // Si es numérico, pedir persona por id
          if (/^\d+$/.test(idOrSlug)) {
            const getUrl = `${backend}/personas/${idOrSlug}`;
            http.get(getUrl, (bres) => {
              let body = '';
              bres.on('data', chunk => body += chunk);
              bres.on('end', () => {
                try {
                  const json = JSON.parse(body);
                  if (bres.statusCode === 200 && (json.success || json.id_Perfil_Persona || json.data)) return cb(true);
                } catch (e) {}
                return cb(false);
              });
            }).on('error', () => cb(false)).setTimeout(2000, () => cb(false));
            return;
          }

          // Si es slug, pedir lista de personas y buscar coincidencia
          const listUrl = `${backend}/personas`;
          http.get(listUrl, (bres) => {
            let body = '';
            bres.on('data', chunk => body += chunk);
            bres.on('end', () => {
              try {
                const json = JSON.parse(body);
                if (bres.statusCode === 200 && json.success && Array.isArray(json.data)) {
                  const slug = idOrSlug.toString().toLowerCase();
                  const found = json.data.find(p => {
                    const username = (p.nombre_Persona || '').toString().toLowerCase();
                    if (username === slug) return true;
                    const full = ((p.nombre_Persona || '') + ' ' + (p.apellido_Persona || '')).toLowerCase();
                    const fullSlug = full.replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
                    return fullSlug === slug;
                  });
                  return cb(Boolean(found));
                }
              } catch (e) {
                // fallthrough
              }
              return cb(false);
            });
          }).on('error', () => cb(false)).setTimeout(3000, () => cb(false));
        }

        // Si es ruta perfil con segmento, validamos existencia del perfil
        if (firstNorm === 'perfil') {
          // /perfil  o /perfil/personal  -> permitir
          if (parts.length === 1 || parts[1] === '' || parts[1].toString().toLowerCase() === 'personal') {
            if (fs.existsSync(entryFile)) return sendFile(res, entryFile, 200);
          } else {
            const idOrSlug = parts[1];
            // consultamos al backend
            return checkPersonaExists(idOrSlug, (exists) => {
              if (exists && fs.existsSync(entryFile)) return sendFile(res, entryFile, 200);
              if (fs.existsSync(notFoundFile)) return sendFile(res, notFoundFile, 404);
              res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
              return res.end('404 Not Found');
            });
          }
        }

        // Permitir rutas conocidas del sidebar
        if (allowedViews.has(firstNorm)) {
          if (fs.existsSync(entryFile)) return sendFile(res, entryFile, 200);
        }
      }

      // No es una ruta SPA autorizada o no existe entryFile: devolver 404.html si existe
      if (fs.existsSync(notFoundFile)) {
        return sendFile(res, notFoundFile, 404);
      }

      // Si no hay 404.html, devolver texto simple
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
      res.end('404 Not Found');
    });
  } catch (e) {
    res.writeHead(500, { 'Content-Type': 'text/plain; charset=UTF-8' });
    res.end('Error del servidor');
  }
});

server.listen(PORT, () => {
  console.log(`Servidor estático escuchando en http://127.0.0.1:${PORT}/index.html`);
  console.log(`Sirviendo carpeta: ${PUBLIC_DIR}`);
});
