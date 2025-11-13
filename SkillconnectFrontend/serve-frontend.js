// Pequeño servidor estático sin dependencias externas
// Uso: desde PowerShell en la carpeta SkillconnectFrontend:
// $env:PORT = "5050"; node serve-frontend.js

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 5050;
const PUBLIC_DIR = __dirname; // sirve archivos desde esta carpeta

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
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; " +
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
                "font-src 'self' https://fonts.gstatic.com data:; " +
                "img-src 'self' data: https:; " +
                "connect-src 'self' http://127.0.0.1:3001 http://localhost:3001 ws:;";
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

    if (safePath === '') safePath = 'index.html';
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

      // No existe el recurso solicitado: devolver 404.html si existe
      const notFoundFile = path.join(PUBLIC_DIR, '404.html');
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
