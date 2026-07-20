import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Expand MAPEO_AVANZADO to include all specific CRUD mappings explicitly
old_config = """                // -> 2. CONFIGURACIONES
                'GESTIONAR_CONFIGURACION': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Gestionar configuración general', icon: 'mdi:cog-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                'configGenerales:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Configuraciones Generales', icon: 'mdi:cogs', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                
                'modalidades:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Modalidades de Intercambio', nombre: 'Modalidades de Intercambio', icon: 'mdi:swap-horizontal', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                
                'categorias:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Categorías de Habilidades', nombre: 'Categorías y Tipos', icon: 'mdi:shape-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                
                'variables:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Variables de Entorno', nombre: 'Variables de Impacto', icon: 'mdi:chart-line', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                
                'motivosBloqueo:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Motivos de Bloqueo', nombre: 'Motivos de Bloqueo', icon: 'mdi:block-helper', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                
                'ASIGNAR_ROLES_PERMISOS': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Asignar permisos a usuarios', icon: 'mdi:shield-key-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                'rolesPermisos:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Gestión y creación de Roles', icon: 'mdi:badge-account-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' }
            };"""

new_config = """                // -> 2. CONFIGURACIONES
                // AJUSTES GLOBALES
                'GESTIONAR_CONFIGURACION': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Gestionar configuración general', icon: 'mdi:cog-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                'configGenerales:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Ver Ajustes Globales', icon: 'mdi:eye-outline', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' },
                'configGenerales:editar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Editar Ajustes Globales', icon: 'mdi:pencil-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500 border border-amber-200 rounded-md' },
                
                // MODALIDADES
                'modalidades:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Modalidades de Intercambio', nombre: 'Ver Modalidades de Intercambio', icon: 'mdi:eye-outline', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' },
                'modalidades:crear': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Modalidades de Intercambio', nombre: 'Crear Modalidades de Intercambio', icon: 'mdi:plus-circle-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-500 border border-emerald-200 rounded-md' },
                'modalidades:editar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Modalidades de Intercambio', nombre: 'Editar Modalidades de Intercambio', icon: 'mdi:pencil-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500 border border-amber-200 rounded-md' },
                'modalidades:eliminar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Modalidades de Intercambio', nombre: 'Eliminar Modalidades de Intercambio', icon: 'mdi:delete-outline', badgeText: 'ELIMINAR', badgeColor: 'bg-red-50 text-red-500 border border-red-200 rounded-md' },
                
                // CATEGORIAS
                'categorias:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Categorías de Habilidades', nombre: 'Ver Categorías de Habilidades', icon: 'mdi:eye-outline', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' },
                'categorias:crear': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Categorías de Habilidades', nombre: 'Crear Categorías de Habilidades', icon: 'mdi:plus-circle-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-500 border border-emerald-200 rounded-md' },
                'categorias:editar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Categorías de Habilidades', nombre: 'Editar Categorías de Habilidades', icon: 'mdi:pencil-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500 border border-amber-200 rounded-md' },
                'categorias:eliminar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Categorías de Habilidades', nombre: 'Eliminar Categorías de Habilidades', icon: 'mdi:delete-outline', badgeText: 'ELIMINAR', badgeColor: 'bg-red-50 text-red-500 border border-red-200 rounded-md' },
                
                // VARIABLES
                'variables:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Variables de Entorno', nombre: 'Ver Variables de Entorno', icon: 'mdi:eye-outline', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' },
                'variables:crear': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Variables de Entorno', nombre: 'Crear Variables de Entorno', icon: 'mdi:plus-circle-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-500 border border-emerald-200 rounded-md' },
                'variables:editar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Variables de Entorno', nombre: 'Editar Variables de Entorno', icon: 'mdi:pencil-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500 border border-amber-200 rounded-md' },
                'variables:eliminar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Variables de Entorno', nombre: 'Eliminar Variables de Entorno', icon: 'mdi:delete-outline', badgeText: 'ELIMINAR', badgeColor: 'bg-red-50 text-red-500 border border-red-200 rounded-md' },
                
                // MOTIVOS
                'motivosBloqueo:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Motivos de Bloqueo', nombre: 'Ver Motivos de Bloqueo', icon: 'mdi:eye-outline', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' },
                'motivosBloqueo:crear': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Motivos de Bloqueo', nombre: 'Crear Motivos de Bloqueo', icon: 'mdi:plus-circle-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-500 border border-emerald-200 rounded-md' },
                'motivosBloqueo:editar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Motivos de Bloqueo', nombre: 'Editar Motivos de Bloqueo', icon: 'mdi:pencil-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500 border border-amber-200 rounded-md' },
                'motivosBloqueo:eliminar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Motivos de Bloqueo', nombre: 'Eliminar Motivos de Bloqueo', icon: 'mdi:delete-outline', badgeText: 'ELIMINAR', badgeColor: 'bg-red-50 text-red-500 border border-red-200 rounded-md' },
                
                // ROLES Y PERMISOS
                'ASIGNAR_ROLES_PERMISOS': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Asignar permisos a usuarios', icon: 'mdi:shield-key-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500 border border-purple-200 rounded-md' },
                'rolesPermisos:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Ver Roles y Permisos', icon: 'mdi:eye-outline', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' },
                'rolesPermisos:crear': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Crear Roles y Permisos', icon: 'mdi:plus-circle-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-500 border border-emerald-200 rounded-md' },
                'rolesPermisos:editar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Editar Roles y Permisos', icon: 'mdi:pencil-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500 border border-amber-200 rounded-md' },
                'rolesPermisos:eliminar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Eliminar Roles y Permisos', icon: 'mdi:delete-outline', badgeText: 'ELIMINAR', badgeColor: 'bg-red-50 text-red-500 border border-red-200 rounded-md' }
            };"""

if old_config in content:
    content = content.replace(old_config, new_config)
else:
    print("WARNING: Could not find old_config to replace!")

# 2. Modify the fallback to put everything else into "Otros Permisos" 
old_fallback = """                        let ssub = 'Ajustes Globales';
                        if (sname.includes('modalidad')) ssub = 'Modalidades de Intercambio';
                        else if (sname.includes('categor') || sname.includes('habilidad')) ssub = 'Categorías de Habilidades';
                        else if (sname.includes('variab') || sname.includes('entorno')) ssub = 'Variables de Entorno';
                        else if (sname.includes('motiv') || sname.includes('bloqueo')) ssub = 'Motivos de Bloqueo';
                        else if (sname.includes('rol') || sname.includes('permis')) ssub = 'Roles y Permisos';
                        else if (sname.includes('usuari') || sname.includes('cuenta')) ssub = 'Directorio General';
                        
                        let finalSub = 'Configuraciones';
                        if (ssub === 'Directorio General' || ssub === 'Usuarios Reportados' || ssub === 'Métricas' || ssub === 'Solicitudes de Verificación') {
                            finalSub = 'Panel de Administración';
                        }"""

new_fallback = """                        let finalSub = 'Configuraciones';
                        let ssub = 'Otros Permisos';
                        
                        // Keep mapping Directorio General correctly via fallback just in case
                        if (sname.includes('usuari') || sname.includes('cuenta')) {
                            ssub = 'Directorio General';
                            finalSub = 'Panel de Administración';
                        }"""

if old_fallback in content:
    content = content.replace(old_fallback, new_fallback)
else:
    print("WARNING: Could not find old_fallback to replace!")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated config mappings and disabled aggressive fallback")
