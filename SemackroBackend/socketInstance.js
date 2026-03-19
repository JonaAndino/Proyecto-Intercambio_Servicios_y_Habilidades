// socketInstance.js
// Singleton para compartir la instancia de Socket.io entre rutas
let _io = null;

module.exports = {
    setIo(io) { _io = io; },
    getIo() { return _io; }
};
