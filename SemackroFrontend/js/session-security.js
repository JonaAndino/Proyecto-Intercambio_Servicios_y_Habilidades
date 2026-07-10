/**
 * SEMACKRO — Seguridad de Sesión
 * ==========================================
 * - Cierre de sesión automático por inactividad (15 minutos)
 * - Persistencia segura en sessionStorage (cierre al cerrar pestaña/navegador)
 */

(function () {
    // 1. Duración máxima de inactividad en milisegundos (15 minutos = 15 * 60 * 1000)
    const TIEMPO_INACTIVIDAD = 15 * 60 * 1000; 
    let timerInactividad;

    // 2. Migración segura de localStorage a sessionStorage (para retrocompatibilidad en la pestaña abierta)
    const clavesSesion = [
        'authToken', 'token', 'usuarioId', 'correoUsuario', 
        'usuarioRolId', 'usuarioRol', 'usuarioPermisos', 'firebaseUser'
    ];

    clavesSesion.forEach(clave => {
        const valorLocal = localStorage.getItem(clave);
        if (valorLocal && !sessionStorage.getItem(clave)) {
            sessionStorage.setItem(clave, valorLocal);
        }
        // Limpiar de localStorage para forzar uso de sessionStorage y que expire al cerrar navegador
        localStorage.removeItem(clave); 
    });

    // PARCHE DE COMPATIBILIDAD MAGICA:
    // Hacemos que cualquier llamada a localStorage.getItem('usuarioId') (o similares)
    // busque automáticamente en sessionStorage, para no tener que reescribir 100 archivos js.
    const originalGetItem = Storage.prototype.getItem;
    Storage.prototype.getItem = function(key) {
        if (this === window.localStorage && clavesSesion.includes(key)) {
            const sessionVal = window.sessionStorage.getItem(key);
            if (sessionVal !== null) {
                return sessionVal;
            }
        }
        return originalGetItem.call(this, key);
    };

    // Sobrescribir helper global de permisos si existe para que busque en sessionStorage
    if (window.Permisos) {
        window.Permisos._obtenerPermisos = function() {
            try {
                return JSON.parse(sessionStorage.getItem('usuarioPermisos') || '[]');
            } catch {
                return [];
            }
        };
        window.Permisos.esAdmin = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) {
                return sessionStorage.getItem('usuarioRolId') === '1';
            }
            return permisos.includes('VER_METRICAS')
                && permisos.includes('MODERAR_USUARIOS')
                && permisos.includes('GESTIONAR_CONFIGURACION');
        };
        window.Permisos.puedeVerReportes = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1';
            return permisos.includes('VER_METRICAS');
        };
        window.Permisos.puedeModerar = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1';
            return permisos.includes('MODERAR_USUARIOS');
        };
        window.Permisos.puedeConfigurar = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1';
            return permisos.includes('GESTIONAR_CONFIGURACION');
        };
        window.Permisos.puedeIntercambiar = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return true;
            return permisos.includes('ACEPTAR_INTERCAMBIOS');
        };
        window.Permisos.puedeVerHistorial = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return true;
            return permisos.includes('VER_HISTORIAL_PERSONAL');
        };
        window.Permisos.puedeVerDirectorio = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1';
            return permisos.includes('VER_DIRECTORIO');
        };
        window.Permisos.esAdminOPersonalAutorizado = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1';
            return permisos.includes('VER_METRICAS')
                || permisos.includes('MODERAR_USUARIOS')
                || permisos.includes('GESTIONAR_CONFIGURACION')
                || permisos.includes('VER_DIRECTORIO')
                || permisos.includes('VER_SOLICITUDES_VERIFICACION');
        };
        window.Permisos.puedeVerSolicitudesVerificacion = function() {
            const permisos = this._obtenerPermisos();
            if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1';
            return permisos.includes('VER_SOLICITUDES_VERIFICACION');
        };
    }

    // 3. Función centralizada de cierre de sesión
    function cerrarSesionInactividad() {
        console.log('[SEGURIDAD] Cerrando sesión por inactividad.');
        
        // Limpiar sessionStorage y localStorage
        clavesSesion.forEach(clave => {
            sessionStorage.removeItem(clave);
            localStorage.removeItem(clave);
        });

        // Almacenar flag temporal para notificar al login
        localStorage.setItem('sesion_expirada_mensaje', 'Tu sesión ha expirado por inactividad de 15 minutos.');

        // Redirigir
        window.location.href = 'login.html';
    }

    // 4. Reinicio de timer ante interacción
    function reiniciarTimerInactividad() {
        clearTimeout(timerInactividad);
        // Si el usuario no está logueado, no iniciar el timer
        if (!sessionStorage.getItem('usuarioId') && !localStorage.getItem('usuarioId')) return;
        timerInactividad = setTimeout(cerrarSesionInactividad, TIEMPO_INACTIVIDAD);
    }

    // 5. Escuchar eventos comunes de interacción del usuario
    const eventosActividad = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    
    eventosActividad.forEach(evento => {
        document.addEventListener(evento, reiniciarTimerInactividad, true);
    });

    // Iniciar timer en carga
    reiniciarTimerInactividad();

    // 6. Aplicar restricciones dinámicas en la interfaz (Sidebar)
    document.addEventListener("DOMContentLoaded", () => {
        if (window.Permisos) {
            const permisos = window.Permisos._obtenerPermisos();
            // Si hay permisos cargados, ocultamos los items de navegación que no estén en la lista
            if (permisos.length > 0) {
                document.querySelectorAll('.sidebar-item[data-view]').forEach(item => {
                    const viewName = item.getAttribute('data-view');
                    if (viewName && !permisos.includes(viewName)) {
                        item.style.display = 'none';
                    }
                });
            }
        }
    });
})();
