/**
 * SEMACKRO — Helper global de permisos
 * ======================================
 * Reemplaza las verificaciones hardcodeadas de id_rol por
 * verificaciones basadas en claves de permisos dinámicos.
 *
 * Uso: window.Permisos.tienePermiso('VER_METRICAS')
 *      window.Permisos.esAdmin()
 */
window.Permisos = {
    /**
     * Obtiene la lista de permisos cacheada.
     * @returns {string[]} Array de claves de permisos (ej: ['VER_METRICAS', 'MODERAR_USUARIOS'])
     */
    _obtenerPermisos() {
        try {
            return JSON.parse(sessionStorage.getItem('usuarioPermisos') || localStorage.getItem('usuarioPermisos') || '[]');
        } catch {
            return [];
        }
    },

    /**
     * Verifica si el usuario tiene un permiso específico.
     * @param {string} clave — Clave del permiso (ej: 'VER_METRICAS')
     * @returns {boolean}
     */
    tienePermiso(clave) {
        return this._obtenerPermisos().includes(clave);
    },

    /**
     * Verifica si el usuario tiene TODOS los permisos administrativos clave.
     * Fallback: si no hay permisos en localStorage/sessionStorage, revisa id_rol === '1'.
     * @returns {boolean}
     */
    esAdmin() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) {
            return sessionStorage.getItem('usuarioRolId') === '1' || localStorage.getItem('usuarioRolId') === '1';
        }
        return permisos.includes('VER_METRICAS')
            && permisos.includes('MODERAR_USUARIOS')
            && permisos.includes('GESTIONAR_CONFIGURACION');
    },

    /** ¿Puede ver reportes y métricas de uso? */
    puedeVerReportes() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1' || localStorage.getItem('usuarioRolId') === '1';
        return permisos.includes('VER_METRICAS');
    },

    /** ¿Puede bloquear y moderar usuarios? */
    puedeModerar() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1' || localStorage.getItem('usuarioRolId') === '1';
        return permisos.includes('MODERAR_USUARIOS');
    },

    /** ¿Puede editar configuraciones y tablas maestras? */
    puedeConfigurar() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1' || localStorage.getItem('usuarioRolId') === '1';
        return permisos.includes('GESTIONAR_CONFIGURACION');
    },

    /** ¿Puede solicitar y concretar intercambios? */
    puedeIntercambiar() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) return true; // Todos pueden por defecto
        return permisos.includes('ACEPTAR_INTERCAMBIOS');
    },

    /** ¿Puede ver historial personal? */
    puedeVerHistorial() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) return true; // Todos pueden por defecto
        return permisos.includes('VER_HISTORIAL_PERSONAL');
    },

    /** ¿Puede ver el Directorio General? */
    puedeVerDirectorio() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1' || localStorage.getItem('usuarioRolId') === '1';
        return permisos.includes('VER_DIRECTORIO');
    },

    /** Determina si tiene acceso a cualquier sección del panel de administración */
    esAdminOPersonalAutorizado() {
        const permisos = this._obtenerPermisos();
        if (permisos.length === 0) return sessionStorage.getItem('usuarioRolId') === '1' || localStorage.getItem('usuarioRolId') === '1';
        return permisos.includes('VER_METRICAS')
            || permisos.includes('MODERAR_USUARIOS')
            || permisos.includes('GESTIONAR_CONFIGURACION')
            || permisos.includes('VER_DIRECTORIO');
    }
};
