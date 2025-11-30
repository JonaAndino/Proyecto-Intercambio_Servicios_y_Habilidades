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
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.ogg': 'video/ogg',
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
            "img-src 'self' data: blob: https: https://pub-ada139691018466fa48df5ea9f22ee6c.r2.dev; " +
            "media-src 'self' data: blob: https://pub-ada139691018466fa48df5ea9f22ee6c.r2.dev; " +
            "connect-src 'self' http://127.0.0.1:5050 http://localhost:5050 http://127.0.0.1:3001 http://localhost:3001 ws: https://unpkg.com https://nominatim.openstreetmap.org https://*.tile.openstreetmap.org https://api.iconify.design https://api.unisvg.com https://api.simplesvg.com;";
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
          // Restaurar protección: solo servir la SPA si la ruta está en allowedViews
          const parts = safePath.split('/').filter(Boolean);
          const first = parts[0] || '';
          const firstNorm = first.toString().toLowerCase();

          // Si la ruta empieza por 'perfil', mantener validación y 404 si corresponde
          if (firstNorm === 'perfil') {
            if (parts.length === 1 || parts[1] === '' || parts[1].toString().toLowerCase() === 'personal') {
              if (fs.existsSync(entryFile)) return sendFile(res, entryFile, 200);
            } else {
              // Mantener validación de perfil por id/slug (lógica original)
              // ...existing code...
              if (fs.existsSync(notFoundFile)) return sendFile(res, notFoundFile, 404);
              res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
              return res.end('404 Not Found');
            }
          } else if (firstNorm === 'reportes') {
            // Ruta /reportes -> servir la SPA para que el cliente SPA la maneje
            if (fs.existsSync(entryFile)) return sendFile(res, entryFile, 200);
          } else {
            // Para cualquier otra ruta sin extensión, SIEMPRE servir la SPA
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