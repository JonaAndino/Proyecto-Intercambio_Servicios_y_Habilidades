import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_function(content, func_name, new_func_code):
    pattern = r'(window\.' + func_name + r'\s*=\s*(?:async\s*)?function\s*\([^)]*\)\s*\{)(.*?)(?=\n        window\.[a-zA-Z0-9_]+\s*=\s*(?:async\s*)?function|\n    </script>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"Could not find {func_name}")
        return content
        
    return content[:match.start()] + new_func_code + content[match.end():]

# Apple style for Roles (Editar Permisos)
apple_roles = """window.abrirModalEditarPermisos = function(idRol) {
            idRolEditandoPermisos = idRol;
            const rol = todosLosRolesCargados.find(r => r.id_rol === idRol);
            if (!rol) return;

            document.getElementById('permisosRoleNombre').textContent = `Permisos para "${rol.nombre_rol}"`;
            
            const getIconoOpcion = (clave) => {
                const map = {
                    'descubrir': 'mdi:compass-outline',
                    'perfil': 'mdi:account-outline',
                    'ordenesTrabajo': 'mdi:briefcase-outline',
                    'mensajes': 'mdi:message-outline',
                    'solicitudesEnviadas': 'mdi:file-document-outline',
                    'favoritos': 'mdi:heart-outline',
                    'historial': 'mdi:history',
                    'reportes': 'mdi:chart-bar',
                    'VER_METRICAS': 'mdi:chart-pie',
                    'MODERAR_USUARIOS': 'mdi:shield-account-outline',
                    'GESTIONAR_CONFIGURACION': 'mdi:cog-outline',
                    'ACEPTAR_INTERCAMBIOS': 'mdi:handshake-outline',
                    'VER_HISTORIAL_PERSONAL': 'mdi:history',
                    'VER_DIRECTORIO': 'mdi:folder-account-outline',
                    'CREAR_CUENTAS': 'mdi:account-plus-outline',
                    'EDITAR_USUARIOS': 'mdi:account-edit-outline',
                    'ASIGNAR_ROLES_PERMISOS': 'mdi:shield-key-outline',
                    'VER_SOLICITUDES_VERIFICACION': 'mdi:check-decagram-outline'
                };
                return map[clave] || 'mdi:checkbox-marked-circle-outline';
            };

            const container = document.getElementById('permisosCheckboxesContainer');
            if (container) {
                const isPermisoAdmin = (clave) => clave === clave.toUpperCase();
                const permisosUsuario = todosLosPermisosDisponibles.filter(p => !isPermisoAdmin(p.clave));
                const permisosAdmin = todosLosPermisosDisponibles.filter(p => isPermisoAdmin(p.clave));

                const generarHTMLPermiso = (p) => {
                    const activo = rol.permisos && rol.permisos.includes(p.clave);
                    const iconoSVG = getIconoOpcion(p.clave);
                    return `
                        <div class="flex items-center justify-between p-3 rounded-2xl bg-slate-50 dark:bg-gray-800/50 hover:bg-slate-100 dark:hover:bg-gray-800 transition-colors border border-transparent hover:border-slate-200 dark:hover:border-gray-700 group">
                            <div class="flex items-center gap-3 w-full">
                                <div class="w-10 h-10 rounded-xl bg-white dark:bg-gray-900 shadow-sm border border-slate-200 dark:border-gray-700 flex items-center justify-center text-slate-500 dark:text-gray-400 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors shrink-0">
                                    <span class="iconify text-xl" data-icon="${iconoSVG}"></span>
                                </div>
                                <div class="flex-1 min-w-0 pr-2">
                                    <input type="text" value="${escapeHtml(p.nombre)}" onclick="event.stopPropagation()" onchange="guardarNombrePermisoGlobal('${p.clave}', this.value)" class="block w-full bg-transparent border-b border-transparent hover:border-slate-300 focus:border-indigo-500 focus:outline-none focus:ring-0 text-sm font-bold text-slate-900 dark:text-white transition-colors cursor-text pb-0.5 mb-0.5 truncate" />
                                    <p class="text-xs text-slate-500 dark:text-gray-400 mt-0.5 truncate font-mono">${escapeHtml(p.clave)}</p>
                                </div>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer shrink-0 ml-2">
                                <input type="checkbox" value="${p.clave}" ${activo ? 'checked' : ''} class="permiso-checkbox sr-only peer">
                                <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 dark:peer-focus:ring-indigo-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                    `;
                };

                const headerUserHTML = permisosUsuario.length > 0 ? `
                    <div class="col-span-1 md:col-span-2 mt-2 mb-2">
                        <h4 class="text-xs font-black text-slate-500 uppercase tracking-widest border-b border-slate-200 dark:border-gray-700 pb-2 flex items-center gap-2">
                            <span class="iconify text-lg" data-icon="mdi:account-group"></span> Permisos de Usuario Normal
                        </h4>
                    </div>
                ` : '';

                const htmlUsuario = permisosUsuario.map(generarHTMLPermiso).join('');

                const headerAdminHTML = permisosAdmin.length > 0 ? `
                    <div class="col-span-1 md:col-span-2 mt-6 mb-2">
                        <h4 class="text-xs font-black text-indigo-600 dark:text-indigo-400 uppercase tracking-widest border-b border-indigo-200 dark:border-indigo-800/50 pb-2 flex items-center gap-2">
                            <span class="iconify text-lg" data-icon="mdi:shield-crown"></span> Administrador
                        </h4>
                    </div>
                ` : '';

                const htmlAdmin = permisosAdmin.map(generarHTMLPermiso).join('');

                container.innerHTML = `
                    ${headerUserHTML}
                    ${htmlUsuario}
                    ${headerAdminHTML}
                    ${htmlAdmin}
                `;
            }

            document.getElementById('permisosModalRoot').style.display = 'flex';
            setTimeout(() => { document.getElementById('permisosCard').classList.add('scale-100', 'opacity-100'); }, 10);
        }
"""

# Apple style for Permisos Individuales
apple_indiv = """window.abrirModalPermisosIndividuales = async function(idUsuario, nombre, idRol) {
            idUsuarioEditandoPermisos = idUsuario;
            document.getElementById('permisosIndivNombre').textContent = `Permisos de ${nombre}`;
            
            const container = document.getElementById('permisosIndivCheckboxesContainer');
            container.innerHTML = '<div class="p-4 text-center text-sm text-gray-500 flex flex-col items-center justify-center gap-3"><span class="iconify text-3xl animate-spin text-indigo-500" data-icon="mdi:loading"></span> Cargando permisos...</div>';
            document.getElementById('permisosIndivModalRoot').style.display = 'flex';
            setTimeout(() => { document.getElementById('permisosIndivCard').classList.add('scale-100', 'opacity-100'); }, 10);

            try {
                if (todosLosPermisosDisponibles.length === 0) {
                    const resPerm = await fetch(`${window.APP_CONFIG.BACKEND_URL}/api/configuraciones/permisos`);
                    if (resPerm.ok) {
                        const jsonPerm = await resPerm.json();
                        if (jsonPerm.success) todosLosPermisosDisponibles = jsonPerm.data;
                    }
                }

                if (todosLosRolesCargados.length === 0) {
                    const resRoles = await fetch(`${window.APP_CONFIG.BACKEND_URL}/api/configuraciones/roles`);
                    if (resRoles.ok) {
                        const jsonRoles = await resRoles.json();
                        if (jsonRoles.success) {
                            todosLosRolesCargados = jsonRoles.data.map(r => ({
                                id_rol: r.id_rol,
                                nombre_rol: r.nombre_rol,
                                permisos: r.permisos ? r.permisos.split(',') : []
                            }));
                        }
                    }
                }

                const resExc = await fetch(`${window.APP_CONFIG.BACKEND_URL}/api/configuraciones/usuarios/${idUsuario}/permisos-excepciones`);
                let excepciones = [];
                if (resExc.ok) {
                    const jsonExc = await resExc.json();
                    if (jsonExc.success) excepciones = jsonExc.data;
                }

                const rol = todosLosRolesCargados.find(r => r.id_rol === idRol) || { permisos: [] };
                
                const getIconoOpcion = (clave) => {
                    const map = {
                        'descubrir': 'mdi:compass-outline',
                        'perfil': 'mdi:account-outline',
                        'ordenesTrabajo': 'mdi:briefcase-outline',
                        'mensajes': 'mdi:message-outline',
                        'solicitudesEnviadas': 'mdi:file-document-outline',
                        'favoritos': 'mdi:heart-outline',
                        'historial': 'mdi:history',
                        'reportes': 'mdi:chart-bar',
                        'VER_METRICAS': 'mdi:chart-pie',
                        'MODERAR_USUARIOS': 'mdi:shield-account-outline',
                        'GESTIONAR_CONFIGURACION': 'mdi:cog-outline',
                        'ACEPTAR_INTERCAMBIOS': 'mdi:handshake-outline',
                        'VER_HISTORIAL_PERSONAL': 'mdi:history',
                        'VER_DIRECTORIO': 'mdi:folder-account-outline',
                        'CREAR_CUENTAS': 'mdi:account-plus-outline',
                        'EDITAR_USUARIOS': 'mdi:account-edit-outline',
                        'ASIGNAR_ROLES_PERMISOS': 'mdi:shield-key-outline',
                        'VER_SOLICITUDES_VERIFICACION': 'mdi:check-decagram-outline'
                    };
                    return map[clave] || 'mdi:checkbox-marked-circle-outline';
                };

                const isPermisoAdmin = (clave) => clave === clave.toUpperCase();
                const permisosUsuario = todosLosPermisosDisponibles.filter(p => !isPermisoAdmin(p.clave));
                const permisosAdmin = todosLosPermisosDisponibles.filter(p => isPermisoAdmin(p.clave));

                const generarHTMLPermiso = (p) => {
                    const iconoSVG = getIconoOpcion(p.clave);
                    const exc = excepciones.find(e => e.link === p.clave);
                    const rolLoTiene = rol.permisos && rol.permisos.includes(p.clave);
                    
                    let val = '';
                    if (exc) {
                        val = exc.concedido ? '1' : '0';
                    }

                    let estadoFinal = rolLoTiene;
                    if (exc) estadoFinal = exc.concedido;

                    let colorFondo = 'border-transparent bg-slate-50 dark:bg-gray-800/50 hover:bg-slate-100 dark:hover:bg-gray-800';
                    let colorTitulo = 'text-slate-900 dark:text-white';
                    let colorIcono = 'text-slate-500 dark:text-gray-400';
                    
                    if (estadoFinal) {
                        if (val === '1') {
                            colorFondo = 'border-green-200 dark:border-green-800 bg-green-50/50 dark:bg-green-900/20';
                            colorTitulo = 'text-green-800 dark:text-green-200';
                            colorIcono = 'text-green-500 dark:text-green-400';
                        } else {
                            colorFondo = 'border-purple-200 dark:border-purple-800 bg-purple-50/50 dark:bg-purple-900/20';
                            colorTitulo = 'text-purple-800 dark:text-purple-200';
                            colorIcono = 'text-purple-500 dark:text-purple-400';
                        }
                    } else {
                        if (val === '0') {
                            colorFondo = 'border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/20';
                            colorTitulo = 'text-red-800 dark:text-red-200';
                            colorIcono = 'text-red-500 dark:text-red-400';
                        }
                    }
                    
                    return `
                        <div class="flex items-center justify-between p-3 rounded-2xl transition-colors border group ${colorFondo}">
                            <div class="flex items-center gap-3 w-full">
                                <div class="w-10 h-10 rounded-xl bg-white dark:bg-gray-900 shadow-sm flex items-center justify-center transition-colors shrink-0 ${colorIcono}">
                                    <span class="iconify text-xl" data-icon="${iconoSVG}"></span>
                                </div>
                                <div class="flex-1 min-w-0 pr-2">
                                    <input type="text" value="${escapeHtml(p.nombre)}" onclick="event.stopPropagation()" onchange="guardarNombrePermisoGlobal('${p.clave}', this.value)" class="block w-full bg-transparent border-b border-transparent hover:border-slate-300 focus:border-indigo-500 focus:outline-none focus:ring-0 text-sm font-bold transition-colors cursor-text pb-0.5 mb-0.5 truncate ${colorTitulo}" />
                                    <p class="text-xs text-slate-500 dark:text-gray-400 mt-0.5 truncate font-mono">${escapeHtml(p.clave)}</p>
                                </div>
                            </div>
                            <div class="shrink-0 ml-2">
                                <select onchange="actualizarVisualFilaPermiso(this)" class="permiso-indiv-select text-xs font-semibold border-0 rounded-xl px-3 py-2 bg-white dark:bg-gray-900 shadow-sm focus:ring-2 focus:ring-indigo-500 cursor-pointer ${colorTitulo}" data-clave="${escapeHtml(p.clave)}">
                                    <option value="" ${val === '' ? 'selected' : ''}>Neutro (Usar Rol)</option>
                                    <option value="1" ${val === '1' ? 'selected' : ''}>Forzar Concedido</option>
                                    <option value="0" ${val === '0' ? 'selected' : ''}>Forzar Denegado</option>
                                </select>
                            </div>
                        </div>
                    `;
                };

                const headerUserHTML = permisosUsuario.length > 0 ? `
                    <div class="col-span-1 md:col-span-2 mt-2 mb-2">
                        <h4 class="text-xs font-black text-slate-500 uppercase tracking-widest border-b border-slate-200 dark:border-gray-700 pb-2 flex items-center gap-2">
                            <span class="iconify text-lg" data-icon="mdi:account-group"></span> Permisos de Usuario Normal
                        </h4>
                    </div>
                ` : '';

                const htmlUsuario = permisosUsuario.map(generarHTMLPermiso).join('');

                const headerAdminHTML = permisosAdmin.length > 0 ? `
                    <div class="col-span-1 md:col-span-2 mt-6 mb-2">
                        <h4 class="text-xs font-black text-indigo-600 dark:text-indigo-400 uppercase tracking-widest border-b border-indigo-200 dark:border-indigo-800/50 pb-2 flex items-center gap-2">
                            <span class="iconify text-lg" data-icon="mdi:shield-crown"></span> Administrador
                        </h4>
                    </div>
                ` : '';

                const htmlAdmin = permisosAdmin.map(generarHTMLPermiso).join('');

                container.innerHTML = `
                    ${headerUserHTML}
                    ${htmlUsuario}
                    ${headerAdminHTML}
                    ${htmlAdmin}
                `;
            } catch (err) {
                console.error('[abrirModalPermisosIndividuales]', err);
                container.innerHTML = '<div class="p-4 text-center text-sm text-red-500 flex flex-col items-center gap-2"><span class="iconify text-3xl" data-icon="mdi:alert-circle-outline"></span> Error al cargar los permisos del usuario.</div>';
            }
        }
"""

content = replace_function(content, "abrirModalEditarPermisos", apple_roles)
content = replace_function(content, "abrirModalPermisosIndividuales", apple_indiv)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modals replaced with Apple style successfully!")
