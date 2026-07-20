import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_mapeo = """const MAPEO_AVANZADO = {
                // MENU DE NAVEGACION
                'descubrir': { master: 'Menú de Navegación', sub: 'Descubrir', nombre: 'Acceso a Descubrir', icon: 'mdi:compass-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },
                'perfil': { master: 'Menú de Navegación', sub: 'Mi perfil', nombre: 'Acceso a Perfil', icon: 'mdi:account-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },
                'ordenesTrabajo': { master: 'Menú de Navegación', sub: 'Postulaciones / Trabajos', nombre: 'Acceso a Órdenes de Trabajo', icon: 'mdi:briefcase-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },
                'mensajes': { master: 'Menú de Navegación', sub: 'Mensajes', nombre: 'Acceso a Mensajes', icon: 'mdi:message-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },
                'solicitudesEnviadas': { master: 'Menú de Navegación', sub: 'Solicitudes de trabajo', nombre: 'Acceso a Solicitudes', icon: 'mdi:file-document-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },
                'favoritos': { master: 'Menú de Navegación', sub: 'Mis favoritos', nombre: 'Acceso a Favoritos', icon: 'mdi:heart-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },
                'historial': { master: 'Menú de Navegación', sub: 'Historial global', nombre: 'Acceso a Historial', icon: 'mdi:history', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },
                'reportes': { master: 'Menú de Navegación', sub: 'Reportes', nombre: 'Acceso a Reportes', icon: 'mdi:chart-bar', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500 rounded-full' },

                // ADMINISTRADOR
                // -> 1. PANEL DE ADMINISTRACIÓN
                'VER_METRICAS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Métricas', nombre: 'Ver tabla de métricas', icon: 'mdi:chart-pie', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600 rounded-md' },
                'VER_HISTORIAL_PERSONAL': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Historial', nombre: 'Ver historial de actividades', icon: 'mdi:history', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600 rounded-md' },
                
                'VER_REPORTES_USUARIOS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Usuarios Reportados', nombre: 'Ver usuarios reportados', icon: 'mdi:alert-circle-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600 rounded-md' },
                'BLOQUEAR_REPORTADOS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Usuarios Reportados', nombre: 'Bloquear usuarios reportados', icon: 'mdi:account-cancel-outline', badgeText: 'BLOQUEAR', badgeColor: 'bg-red-50 text-red-500 rounded-md' },
                
                'VER_SOLICITUDES_VERIFICACION': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Solicitudes de Verificación', nombre: 'Ver solicitudes de verificación', icon: 'mdi:check-decagram-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600 rounded-md' },
                'ACEPTAR_INTERCAMBIOS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Solicitudes de Verificación', nombre: 'Aceptar y gestionar intercambios', icon: 'mdi:handshake-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600 rounded-md' },
                
                'VER_DIRECTORIO': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Directorio General', nombre: 'Ver listado del directorio', icon: 'mdi:account-group-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600 rounded-md' },
                'CREAR_CUENTAS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Directorio General', nombre: 'Crear nuevas cuentas', icon: 'mdi:account-plus-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-500 rounded-md' },
                'EDITAR_USUARIOS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Directorio General', nombre: 'Editar perfiles de usuarios', icon: 'mdi:account-edit-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500 rounded-md' },
                'MODERAR_USUARIOS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Directorio General', nombre: 'Moderar usuarios (Admin)', icon: 'mdi:shield-account-outline', badgeText: 'BLOQUEAR', badgeColor: 'bg-red-50 text-red-500 rounded-md' },
                
                // -> 2. CONFIGURACIONES
                'GESTIONAR_CONFIGURACION': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Gestionar configuración general', icon: 'mdi:cog-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' },
                'configGenerales:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Configuraciones Generales', icon: 'mdi:cogs', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' },
                
                'modalidades:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Modalidades de Intercambio', nombre: 'Modalidades de Intercambio', icon: 'mdi:swap-horizontal', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' },
                
                'categorias:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Categorías de Habilidades', nombre: 'Categorías y Tipos', icon: 'mdi:shape-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' },
                
                'variables:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Variables de Entorno', nombre: 'Variables de Impacto', icon: 'mdi:chart-line', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' },
                
                'motivosBloqueo:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Motivos de Bloqueo', nombre: 'Motivos de Bloqueo', icon: 'mdi:block-helper', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' },
                
                'ASIGNAR_ROLES_PERMISOS': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Asignar permisos a usuarios', icon: 'mdi:shield-key-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' },
                'rolesPermisos:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Gestión y creación de Roles', icon: 'mdi:badge-account-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 rounded-md' }
            };"""

pattern = r'const MAPEO_AVANZADO = \{.*?^\s*\};'
if re.search(pattern, content, re.MULTILINE | re.DOTALL):
    content = re.sub(pattern, new_mapeo, content, flags=re.MULTILINE | re.DOTALL)

# Now fix the fallback logic in both modals

old_fallback = r"""if \(!map\) \{
                        const crud = determinarCrud\(p\.clave, p\.nombre\);
                        map = \{ 
                            master: 'Administrador', 
                            sub: 'Configuraciones', 
                            nombre: p\.nombre, 
                            icon: crud\.icon, 
                            badgeText: crud\.text, 
                            badgeColor: crud\.color 
                        \};
                    \}"""

new_fallback = """if (!map) {
                        const crud = determinarCrud(p.clave, p.nombre);
                        const sname = p.nombre.toLowerCase();
                        let ssub = 'Ajustes Globales';
                        if (sname.includes('modalidad')) ssub = 'Modalidades de Intercambio';
                        else if (sname.includes('categor') || sname.includes('habilidad')) ssub = 'Categorías de Habilidades';
                        else if (sname.includes('variab') || sname.includes('entorno')) ssub = 'Variables de Entorno';
                        else if (sname.includes('motiv') || sname.includes('bloqueo')) ssub = 'Motivos de Bloqueo';
                        else if (sname.includes('rol') || sname.includes('permis')) ssub = 'Roles y Permisos';
                        else if (sname.includes('usuari') || sname.includes('cuenta')) ssub = 'Directorio General';
                        
                        map = { 
                            master: 'Administrador', 
                            sub: 'Configuraciones', 
                            subsub: ssub,
                            nombre: p.nombre, 
                            icon: crud.icon, 
                            badgeText: crud.text, 
                            badgeColor: crud.color 
                        };
                    }"""

content = re.sub(old_fallback, new_fallback, content)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated mapping successfully")
