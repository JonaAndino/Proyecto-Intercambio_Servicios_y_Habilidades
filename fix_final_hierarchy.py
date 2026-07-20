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

# Common code
common_setup = """
            window.terminoBusquedaPermisos = window.terminoBusquedaPermisos || '';
            window.acordeonesMasterAbiertos = window.acordeonesMasterAbiertos || { 
                'Menú de Navegación': true, 
                'Administrador': true 
            };
            window.acordeonesSubAbiertos = window.acordeonesSubAbiertos || {};

            const MAPEO_AVANZADO = {
                // MENU DE NAVEGACION
                'descubrir': { master: 'Menú de Navegación', sub: 'Descubrir', nombre: 'Acceso a Descubrir', icon: 'mdi:compass-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },
                'perfil': { master: 'Menú de Navegación', sub: 'Mi perfil', nombre: 'Acceso a Perfil', icon: 'mdi:account-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },
                'ordenesTrabajo': { master: 'Menú de Navegación', sub: 'Postulaciones / Trabajos', nombre: 'Acceso a Órdenes de Trabajo', icon: 'mdi:briefcase-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },
                'mensajes': { master: 'Menú de Navegación', sub: 'Mensajes', nombre: 'Acceso a Mensajes', icon: 'mdi:message-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },
                'solicitudesEnviadas': { master: 'Menú de Navegación', sub: 'Solicitudes de trabajo', nombre: 'Acceso a Solicitudes', icon: 'mdi:file-document-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },
                'favoritos': { master: 'Menú de Navegación', sub: 'Mis favoritos', nombre: 'Acceso a Favoritos', icon: 'mdi:heart-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },
                'historial': { master: 'Menú de Navegación', sub: 'Historial global', nombre: 'Acceso a Historial', icon: 'mdi:history', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },
                'reportes': { master: 'Menú de Navegación', sub: 'Reportes', nombre: 'Acceso a Reportes', icon: 'mdi:chart-bar', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-500' },

                // ADMINISTRADOR
                // Panel de Métricas / Reportes
                'VER_METRICAS': { master: 'Administrador', sub: 'Panel de Administración', nombre: 'Ver panel de métricas y reportes', icon: 'mdi:chart-pie', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600' },
                'VER_HISTORIAL_PERSONAL': { master: 'Administrador', sub: 'Panel de Administración', nombre: 'Ver historial de actividades globales', icon: 'mdi:history', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600' },
                
                // Directorio de Usuarios
                'VER_DIRECTORIO': { master: 'Administrador', sub: 'Directorio de Usuarios', nombre: 'Ver listado y tabla del directorio general', icon: 'mdi:account-group-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600' },
                'CREAR_CUENTAS': { master: 'Administrador', sub: 'Directorio de Usuarios', nombre: 'Crear y enrolar nuevas cuentas de usuario', icon: 'mdi:account-plus-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-500' },
                'EDITAR_USUARIOS': { master: 'Administrador', sub: 'Directorio de Usuarios', nombre: 'Editar perfiles y datos de usuarios', icon: 'mdi:account-edit-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-500' },
                'MODERAR_USUARIOS': { master: 'Administrador', sub: 'Directorio de Usuarios', nombre: 'Moderar usuarios (Admin General)', icon: 'mdi:shield-account-outline', badgeText: 'BLOQUEAR', badgeColor: 'bg-red-50 text-red-500' },
                'VER_REPORTES_USUARIOS': { master: 'Administrador', sub: 'Directorio de Usuarios', nombre: 'Ver y gestionar usuarios reportados', icon: 'mdi:alert-circle-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600' },
                'BLOQUEAR_REPORTADOS': { master: 'Administrador', sub: 'Directorio de Usuarios', nombre: 'Bloquear usuarios reportados', icon: 'mdi:account-cancel-outline', badgeText: 'BLOQUEAR', badgeColor: 'bg-red-50 text-red-500' },
                
                // Configuraciones del Sistema
                'GESTIONAR_CONFIGURACION': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Gestionar configuración general del sistema', icon: 'mdi:cog-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                'ASIGNAR_ROLES_PERMISOS': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Asignar roles y permisos a usuarios', icon: 'mdi:shield-key-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                'configGenerales:ver': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Configuraciones Generales', icon: 'mdi:cogs', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                'modalidades:ver': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Modalidades de Intercambio', icon: 'mdi:swap-horizontal', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                'categorias:ver': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Categorías y Tipos', icon: 'mdi:shape-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                'variables:ver': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Variables de Impacto', icon: 'mdi:chart-line', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                'motivosBloqueo:ver': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Motivos de Bloqueo', icon: 'mdi:block-helper', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                'rolesPermisos:ver': { master: 'Administrador', sub: 'Configuraciones del Sistema', nombre: 'Gestión de Roles', icon: 'mdi:badge-account-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-500' },
                
                // Solicitudes y Verificación
                'VER_SOLICITUDES_VERIFICACION': { master: 'Administrador', sub: 'Solicitudes y Verificación', nombre: 'Ver y validar solicitudes de verificación', icon: 'mdi:check-decagram-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600' },
                'ACEPTAR_INTERCAMBIOS': { master: 'Administrador', sub: 'Solicitudes y Verificación', nombre: 'Aceptar y gestionar intercambios', icon: 'mdi:handshake-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-600' }
            };

            const ICONOS_MASTER = {
                'Menú de Navegación': 'mdi:compass-outline',
                'Administrador': 'mdi:shield-crown-outline'
            };
"""

roles_code = """window.abrirModalEditarPermisos = function(idRol) {
            idRolEditandoPermisos = idRol;
            const rol = todosLosRolesCargados.find(r => r.id_rol === idRol);
            if (!rol) return;
            
            window.permisosSeleccionados = new Set(rol.permisos || []);
            """ + common_setup + """

            window.renderizarModalPermisos = () => {
                const jerarquia = { 'Menú de Navegación': {}, 'Administrador': {} }; // SOLAMENTE ESTOS DOS
                
                todosLosPermisosDisponibles.forEach(p => {
                    // Si no está mapeado, se asume que es una configuración del administrador
                    const map = MAPEO_AVANZADO[p.clave] || { master: 'Administrador', sub: 'Otras Configuraciones', nombre: p.nombre, icon: 'mdi:checkbox-marked-circle-outline', badgeText: 'PERMISO', badgeColor: 'bg-slate-100 text-slate-600' };
                    
                    if (window.terminoBusquedaPermisos && 
                        !map.nombre.toLowerCase().includes(window.terminoBusquedaPermisos.toLowerCase()) && 
                        !p.clave.toLowerCase().includes(window.terminoBusquedaPermisos.toLowerCase())) {
                        return;
                    }
                    
                    // Asegurar que el master sea uno de los dos permitidos
                    let finalMaster = map.master;
                    if (finalMaster !== 'Menú de Navegación' && finalMaster !== 'Administrador') {
                        finalMaster = 'Administrador';
                    }
                    
                    if (!jerarquia[finalMaster][map.sub]) jerarquia[finalMaster][map.sub] = [];
                    jerarquia[finalMaster][map.sub].push({ ...p, ...map });
                });

                let totalSeleccionados = window.permisosSeleccionados.size;
                let htmlMaster = '';
                
                for (const masterName of Object.keys(jerarquia)) {
                    const subs = jerarquia[masterName];
                    if (Object.keys(subs).length === 0) continue;
                    
                    let cantTotalMaster = 0;
                    let cantSelMaster = 0;
                    let htmlSubs = '';

                    for (const subName of Object.keys(subs)) {
                        const permisosSub = subs[subName];
                        if (permisosSub.length === 0) continue;
                        
                        cantTotalMaster += permisosSub.length;
                        const selSub = permisosSub.filter(p => window.permisosSeleccionados.has(p.clave)).length;
                        cantSelMaster += selSub;
                        
                        const subKey = masterName + '_' + subName;
                        if (window.acordeonesSubAbiertos[subKey] === undefined) {
                            window.acordeonesSubAbiertos[subKey] = false;
                        }
                        const isSubOpen = window.acordeonesSubAbiertos[subKey];
                        const hasActiveSub = selSub > 0;

                        const htmlPermisos = permisosSub.map(p => {
                            const activo = window.permisosSeleccionados.has(p.clave);
                            return `
                                <div class="flex items-center justify-between py-4 px-8 hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0">
                                    <div class="flex items-center gap-4 flex-1">
                                        <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 shrink-0">
                                            <span class="iconify text-lg" data-icon="${p.icon}"></span>
                                        </div>
                                        <input type="text" value="${escapeHtml(p.nombre)}" onclick="event.stopPropagation()" onchange="guardarNombrePermisoGlobal('${p.clave}', this.value)" class="bg-transparent border-none p-0 focus:ring-0 text-[14px] font-bold text-slate-700 hover:text-blue-600 focus:text-blue-600 transition-colors w-full cursor-text" />
                                    </div>
                                    <div class="flex items-center gap-6 shrink-0 ml-4">
                                        <span class="w-[90px] py-1.5 rounded-full text-[10px] font-extrabold tracking-wider uppercase text-center flex-shrink-0 ${p.badgeColor}">${p.badgeText}</span>
                                        <label class="relative inline-flex items-center cursor-pointer">
                                            <input type="checkbox" value="${p.clave}" ${activo ? 'checked' : ''} onchange="togglePermisoRol('${p.clave}', this.checked)" class="sr-only peer">
                                            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                                        </label>
                                    </div>
                                </div>
                            `;
                        }).join('');

                        htmlSubs += `
                            <div class="bg-white border-b border-slate-100 last:border-0 overflow-hidden transition-all">
                                <div class="flex items-center justify-between px-8 py-5 cursor-pointer hover:bg-slate-50 transition-colors" onclick="toggleAcordeonSub('${subKey}')">
                                    <div class="flex items-center gap-3">
                                        <h5 class="font-bold text-slate-600 text-[14.5px]">${subName}</h5>
                                        ${hasActiveSub && !isSubOpen ? '<div class="w-2 h-2 rounded-full bg-emerald-500 shadow-sm"></div>' : ''}
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <span class="iconify text-slate-400 text-xl transition-transform ${isSubOpen ? 'rotate-180 text-slate-600' : ''}" data-icon="mdi:chevron-down"></span>
                                    </div>
                                </div>
                                <div class="transition-all ${isSubOpen ? 'block' : 'hidden'} bg-white border-t border-slate-50">
                                    ${htmlPermisos}
                                </div>
                            </div>
                        `;
                    }

                    const isMasterOpen = window.acordeonesMasterAbiertos[masterName];
                    const iconMaster = ICONOS_MASTER[masterName] || 'mdi:shield-star-outline';

                    htmlMaster += `
                        <div class="mb-4 rounded-2xl bg-slate-50 border border-slate-200 overflow-hidden transition-all">
                            <div class="flex items-center justify-between px-6 py-4 cursor-pointer transition-colors hover:bg-slate-100/50" onclick="toggleAcordeonMaster('${masterName}')">
                                <div class="flex items-center gap-4">
                                    <div class="w-9 h-9 rounded-xl bg-white shadow-sm flex items-center justify-center text-slate-600 shrink-0">
                                        <span class="iconify text-lg" data-icon="${iconMaster}"></span>
                                    </div>
                                    <h4 class="font-bold text-slate-700 text-[15px]">${masterName}</h4>
                                </div>
                                <div class="flex items-center gap-4">
                                    <span class="text-blue-500 text-[11px] font-bold">${cantSelMaster}/${cantTotalMaster}</span>
                                    <div class="flex items-center gap-2 text-[11px] font-bold text-slate-500" onclick="event.stopPropagation()">
                                        <button type="button" onclick="seleccionarTodoMaster('${masterName}', true)" class="hover:text-slate-800 text-slate-700 transition-colors">Todo</button>
                                        <span class="text-slate-200">|</span>
                                        <button type="button" onclick="seleccionarTodoMaster('${masterName}', false)" class="hover:text-slate-800 text-slate-400 transition-colors">Nada</button>
                                    </div>
                                    <span class="iconify text-slate-400 text-xl transition-transform ${isMasterOpen ? 'rotate-180 text-slate-600' : ''}" data-icon="mdi:chevron-down"></span>
                                </div>
                            </div>
                            <div class="transition-all ${isMasterOpen ? 'block' : 'hidden'} bg-white">
                                <div class="flex flex-col">
                                    ${htmlSubs}
                                </div>
                            </div>
                        </div>
                    `;
                }

                document.getElementById('permisosCheckboxesContainer').innerHTML = `
                    <div class="flex flex-col gap-4">
                        <div class="flex items-center gap-3 mb-2">
                            <!-- Buscar -->
                            <div class="relative flex-1 bg-white border border-slate-200 rounded-2xl shadow-sm">
                                <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-slate-400">
                                    <span class="iconify text-lg" data-icon="mdi:magnify"></span>
                                </span>
                                <input type="text" placeholder="Buscar permiso..." value="${escapeHtml(window.terminoBusquedaPermisos)}" oninput="buscarPermisosEnModal(this.value)" class="w-full pl-11 pr-4 py-3 bg-transparent border-none text-[14px] font-medium focus:outline-none focus:ring-0 text-slate-700 placeholder-slate-400">
                            </div>
                            <!-- Todo | Nada -->
                            <div class="flex items-center gap-3 px-5 py-3 bg-white border border-slate-200 rounded-2xl text-[13px] font-bold text-slate-600 shadow-sm shrink-0">
                                <button type="button" onclick="seleccionarTodoGlobal(true)" class="hover:text-slate-900 transition-colors text-slate-700">Todo</button>
                                <span class="text-slate-200">|</span>
                                <button type="button" onclick="seleccionarTodoGlobal(false)" class="hover:text-slate-900 transition-colors text-slate-400">Nada</button>
                            </div>
                            <!-- Seleccionados -->
                            <div class="flex items-center gap-2 px-5 py-3 border border-slate-200 bg-white rounded-2xl text-[13px] font-bold whitespace-nowrap shadow-sm shrink-0">
                                <span class="iconify text-emerald-500 text-base" data-icon="mdi:check-all"></span>
                                <span class="text-slate-700">${totalSeleccionados} seleccionados</span>
                            </div>
                        </div>
                        <div>
                            ${htmlMaster}
                        </div>
                    </div>
                `;
            };

            window.togglePermisoRol = (clave, isChecked) => {
                if (isChecked) window.permisosSeleccionados.add(clave);
                else window.permisosSeleccionados.delete(clave);
                window.renderizarModalPermisos();
            };

            window.toggleAcordeonMaster = (grupo) => {
                window.acordeonesMasterAbiertos[grupo] = !window.acordeonesMasterAbiertos[grupo];
                window.renderizarModalPermisos();
            };
            
            window.toggleAcordeonSub = (subKey) => {
                window.acordeonesSubAbiertos[subKey] = !window.acordeonesSubAbiertos[subKey];
                window.renderizarModalPermisos();
            };

            window.buscarPermisosEnModal = (val) => {
                window.terminoBusquedaPermisos = val;
                if (val) {
                    Object.keys(window.acordeonesMasterAbiertos).forEach(k => window.acordeonesMasterAbiertos[k] = true);
                    Object.keys(window.acordeonesSubAbiertos).forEach(k => window.acordeonesSubAbiertos[k] = true);
                }
                window.renderizarModalPermisos();
            };

            window.seleccionarTodoMaster = (masterName, seleccionar) => {
                todosLosPermisosDisponibles.forEach(p => {
                    const map = MAPEO_AVANZADO[p.clave] || { master: 'Administrador' };
                    let finalMaster = map.master;
                    if (finalMaster !== 'Menú de Navegación' && finalMaster !== 'Administrador') {
                        finalMaster = 'Administrador';
                    }
                    if (finalMaster === masterName) {
                        if (seleccionar) window.permisosSeleccionados.add(p.clave);
                        else window.permisosSeleccionados.delete(p.clave);
                    }
                });
                window.renderizarModalPermisos();
            };

            window.seleccionarTodoGlobal = (seleccionar) => {
                if (seleccionar) {
                    todosLosPermisosDisponibles.forEach(p => window.permisosSeleccionados.add(p.clave));
                } else {
                    window.permisosSeleccionados.clear();
                }
                window.renderizarModalPermisos();
            };

            window.guardarPermisosRol = async function() {
                const arrPermisos = Array.from(window.permisosSeleccionados);
                try {
                    const formData = new FormData();
                    formData.append('permisos', JSON.stringify(arrPermisos));
                    
                    const res = await fetch(`${window.APP_CONFIG.BACKEND_URL}/api/configuraciones/roles/${idRolEditandoPermisos}/permisos`, {
                        method: 'PUT',
                        body: formData
                    });
                    
                    if (res.ok) {
                        const idx = todosLosRolesCargados.findIndex(r => r.id_rol === idRolEditandoPermisos);
                        if (idx !== -1) {
                            todosLosRolesCargados[idx].permisos = arrPermisos;
                        }
                        cerrarModalEditarPermisos();
                        if(typeof cargarYRenderizarRolesConfig === "function") cargarYRenderizarRolesConfig(); else if(typeof cargarRoles === "function") cargarRoles();
                        mostrarToastPersonalizado('Roles', 'Permisos actualizados correctamente', 'success');
                    } else {
                        throw new Error('Error en servidor');
                    }
                } catch (err) {
                    console.error('Error al guardar permisos del rol:', err);
                    mostrarToastPersonalizado('Error', 'No se pudieron guardar los permisos', 'error');
                }
            };

            const modalRoot = document.getElementById('permisosModalRoot');
            modalRoot.innerHTML = `
                <div id="permisosBackdrop" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-[9998]" onclick="cerrarModalEditarPermisos()"></div>
                <div id="permisosCard" class="relative bg-white rounded-[32px] w-full max-w-[950px] max-h-[90vh] shadow-[0_20px_60px_rgb(0,0,0,0.15)] flex flex-col overflow-hidden z-[9999] transition-all m-auto">
                    <div class="flex items-center justify-between px-8 py-6 shrink-0">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-500 shadow-sm">
                                <span class="iconify text-2xl" data-icon="mdi:shield-key-outline"></span>
                            </div>
                            <div>
                                <h3 id="permisosRoleNombre" class="text-xl font-extrabold text-slate-800 tracking-tight">Asignar permisos al rol: ${rol.nombre_rol}</h3>
                                <p class="text-[13px] text-slate-400 mt-1 font-medium">Gestiona los accesos y privilegios de este rol.</p>
                            </div>
                        </div>
                        <button type="button" onclick="cerrarModalEditarPermisos()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-50 hover:bg-slate-100 text-slate-500 transition-colors cursor-pointer" aria-label="Cerrar modal">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    <div class="px-8 pb-4 overflow-y-auto flex-1 custom-scrollbar" id="permisosCheckboxesContainer">
                        <!-- Se llena dinámicamente -->
                    </div>
                    <div class="px-8 py-6 bg-white flex justify-end gap-3 shrink-0">
                        <button type="button" onclick="cerrarModalEditarPermisos()" class="px-6 py-2.5 rounded-2xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-sm font-bold transition-all cursor-pointer">Cancelar</button>
                        <button type="button" onclick="guardarPermisosRol()" class="px-6 py-2.5 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold transition-all cursor-pointer shadow-md shadow-blue-500/20">
                            Guardar Permisos
                        </button>
                    </div>
                </div>
            `;

            window.renderizarModalPermisos();
            modalRoot.style.display = 'flex';
            setTimeout(() => { document.getElementById('permisosCard').classList.add('scale-100', 'opacity-100'); }, 10);
        }
"""

indiv_code = """window.abrirModalPermisosIndividuales = async function(idUsuario, nombre, idRol) {
            idUsuarioEditandoPermisos = idUsuario;
            
            window.terminoBusquedaPermisosIndiv = window.terminoBusquedaPermisosIndiv || '';
            window.acordeonesMasterAbiertosIndiv = window.acordeonesMasterAbiertosIndiv || { 
                'Menú de Navegación': true, 
                'Administrador': true 
            };
            window.acordeonesSubAbiertosIndiv = window.acordeonesSubAbiertosIndiv || {};

            const modalRoot = document.getElementById('permisosIndivModalRoot');
            modalRoot.innerHTML = `
                <div id="permisosIndivBackdrop" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-[9998]" onclick="cerrarModalPermisosIndividuales()"></div>
                <div id="permisosIndivCard" class="relative bg-white rounded-[32px] w-full max-w-[950px] max-h-[90vh] shadow-[0_20px_60px_rgb(0,0,0,0.15)] flex flex-col overflow-hidden z-[9999] transition-all m-auto">
                    <div class="flex items-center justify-between px-8 py-6 shrink-0">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-500 shadow-sm">
                                <span class="iconify text-2xl" data-icon="mdi:shield-account"></span>
                            </div>
                            <div>
                                <h3 id="permisosIndivNombre" class="text-xl font-extrabold text-slate-800 tracking-tight">Permisos de Usuario: ${nombre}</h3>
                                <p class="text-[13px] text-slate-400 mt-1 font-medium">Gestiona permisos personalizados para este usuario.</p>
                            </div>
                        </div>
                        <button type="button" onclick="cerrarModalPermisosIndividuales()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-50 hover:bg-slate-100 text-slate-500 transition-colors cursor-pointer" aria-label="Cerrar modal">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    <div class="px-8 pb-4 overflow-y-auto flex-1 custom-scrollbar" id="permisosIndivCheckboxesContainer">
                        <div class="flex flex-col items-center justify-center gap-3 py-10">
                            <span class="iconify text-4xl animate-spin text-blue-500" data-icon="mdi:loading"></span> 
                        </div>
                    </div>
                    <div class="px-8 py-6 bg-white flex justify-end gap-3 shrink-0">
                        <button type="button" onclick="cerrarModalPermisosIndividuales()" class="px-6 py-2.5 rounded-2xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-sm font-bold transition-all cursor-pointer">Cancelar</button>
                        <button type="button" onclick="guardarPermisosIndividuales()" class="px-6 py-2.5 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold transition-all cursor-pointer shadow-md shadow-blue-500/20">
                            Guardar Excepciones
                        </button>
                    </div>
                </div>
            `;

            modalRoot.style.display = 'flex';
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
                window.excepcionesCargadas = [];
                if (resExc.ok) {
                    const jsonExc = await resExc.json();
                    if (jsonExc.success) window.excepcionesCargadas = jsonExc.data;
                }

                window.rolCargadoParaIndiv = todosLosRolesCargados.find(r => r.id_rol === idRol) || { permisos: [] };

                window.toggleExcepcionPermiso = (clave, isChecked) => {
                    const idx = window.excepcionesCargadas.findIndex(e => e.link === clave);
                    if (isChecked) {
                        if (idx !== -1) window.excepcionesCargadas[idx].concedido = true;
                        else window.excepcionesCargadas.push({ link: clave, concedido: true });
                    } else {
                        if (idx !== -1) window.excepcionesCargadas[idx].concedido = false;
                        else window.excepcionesCargadas.push({ link: clave, concedido: false });
                    }
                    window.renderizarModalPermisosIndiv();
                };

                window.renderizarModalPermisosIndiv = () => {
                    const jerarquia = { 'Menú de Navegación': {}, 'Administrador': {} }; // SOLAMENTE DOS
                    
                    todosLosPermisosDisponibles.forEach(p => {
                        const map = MAPEO_AVANZADO[p.clave] || { master: 'Administrador', sub: 'Otras Configuraciones', nombre: p.nombre, icon: 'mdi:checkbox-marked-circle-outline', badgeText: 'PERMISO', badgeColor: 'bg-slate-100 text-slate-600' };
                        
                        if (window.terminoBusquedaPermisosIndiv && 
                            !map.nombre.toLowerCase().includes(window.terminoBusquedaPermisosIndiv.toLowerCase()) && 
                            !p.clave.toLowerCase().includes(window.terminoBusquedaPermisosIndiv.toLowerCase())) {
                            return;
                        }
                        
                        let finalMaster = map.master;
                        if (finalMaster !== 'Menú de Navegación' && finalMaster !== 'Administrador') {
                            finalMaster = 'Administrador';
                        }
                        
                        if (!jerarquia[finalMaster][map.sub]) jerarquia[finalMaster][map.sub] = [];
                        jerarquia[finalMaster][map.sub].push({ ...p, ...map });
                    });

                    let totalSeleccionados = window.excepcionesCargadas.filter(e => e.concedido).length;
                    let htmlMaster = '';
                    
                    for (const masterName of Object.keys(jerarquia)) {
                        const subs = jerarquia[masterName];
                        if (Object.keys(subs).length === 0) continue;
                        
                        let cantTotalMaster = 0;
                        let cantSelMaster = 0;
                        let htmlSubs = '';

                        for (const subName of Object.keys(subs)) {
                            const permisosSub = subs[subName];
                            if (permisosSub.length === 0) continue;
                            
                            cantTotalMaster += permisosSub.length;
                            const concedidosSub = permisosSub.filter(p => {
                                const exc = window.excepcionesCargadas.find(e => e.link === p.clave);
                                const rolLoTiene = window.rolCargadoParaIndiv.permisos && window.rolCargadoParaIndiv.permisos.includes(p.clave);
                                return exc ? exc.concedido : rolLoTiene;
                            }).length;
                            cantSelMaster += concedidosSub;
                            
                            const subKey = masterName + '_' + subName;
                            if (window.acordeonesSubAbiertosIndiv[subKey] === undefined) {
                                window.acordeonesSubAbiertosIndiv[subKey] = false;
                            }
                            const isSubOpen = window.acordeonesSubAbiertosIndiv[subKey];
                            const hasActiveSub = concedidosSub > 0;

                            const htmlPermisos = permisosSub.map(p => {
                                const exc = window.excepcionesCargadas.find(e => e.link === p.clave);
                                const rolLoTiene = window.rolCargadoParaIndiv.permisos && window.rolCargadoParaIndiv.permisos.includes(p.clave);
                                let activo = rolLoTiene;
                                if (exc) activo = exc.concedido;

                                return `
                                    <div class="flex items-center justify-between py-4 px-8 hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0">
                                        <div class="flex items-center gap-4 flex-1">
                                            <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 shrink-0">
                                                <span class="iconify text-lg" data-icon="${p.icon}"></span>
                                            </div>
                                            <input type="text" value="${escapeHtml(p.nombre)}" onclick="event.stopPropagation()" onchange="guardarNombrePermisoGlobal('${p.clave}', this.value)" class="bg-transparent border-none p-0 focus:ring-0 text-[14px] font-bold text-slate-700 hover:text-blue-600 focus:text-blue-600 transition-colors w-full cursor-text" />
                                        </div>
                                        <div class="flex items-center gap-6 shrink-0 ml-4">
                                            <span class="w-[90px] py-1.5 rounded-full text-[10px] font-extrabold tracking-wider uppercase text-center flex-shrink-0 ${p.badgeColor}">${p.badgeText}</span>
                                            <label class="relative inline-flex items-center cursor-pointer">
                                                <input type="checkbox" value="${p.clave}" ${activo ? 'checked' : ''} onchange="window.toggleExcepcionPermiso('${p.clave}', this.checked)" class="sr-only peer">
                                                <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                                            </label>
                                        </div>
                                    </div>
                                `;
                            }).join('');

                            htmlSubs += `
                                <div class="bg-white border-b border-slate-100 last:border-0 overflow-hidden transition-all">
                                    <div class="flex items-center justify-between px-8 py-5 cursor-pointer hover:bg-slate-50 transition-colors" onclick="window.acordeonesSubAbiertosIndiv['${subKey}'] = !window.acordeonesSubAbiertosIndiv['${subKey}']; window.renderizarModalPermisosIndiv();">
                                        <div class="flex items-center gap-3">
                                            <h5 class="font-bold text-slate-600 text-[14.5px]">${subName}</h5>
                                            ${hasActiveSub && !isSubOpen ? '<div class="w-2 h-2 rounded-full bg-emerald-500 shadow-sm"></div>' : ''}
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <span class="iconify text-slate-400 text-xl transition-transform ${isSubOpen ? 'rotate-180 text-slate-600' : ''}" data-icon="mdi:chevron-down"></span>
                                        </div>
                                    </div>
                                    <div class="transition-all ${isSubOpen ? 'block' : 'hidden'} bg-white border-t border-slate-50">
                                        ${htmlPermisos}
                                    </div>
                                </div>
                            `;
                        }

                        const isMasterOpen = window.acordeonesMasterAbiertosIndiv[masterName];
                        const iconMaster = ICONOS_MASTER[masterName] || 'mdi:shield-star-outline';

                        htmlMaster += `
                            <div class="mb-4 rounded-2xl bg-slate-50 border border-slate-200 overflow-hidden transition-all">
                                <div class="flex items-center justify-between px-6 py-4 cursor-pointer transition-colors hover:bg-slate-100/50" onclick="window.acordeonesMasterAbiertosIndiv['${masterName}'] = !window.acordeonesMasterAbiertosIndiv['${masterName}']; window.renderizarModalPermisosIndiv();">
                                    <div class="flex items-center gap-4">
                                        <div class="w-9 h-9 rounded-xl bg-white shadow-sm flex items-center justify-center text-slate-600 shrink-0">
                                            <span class="iconify text-lg" data-icon="${iconMaster}"></span>
                                        </div>
                                        <h4 class="font-bold text-slate-700 text-[15px]">${masterName}</h4>
                                    </div>
                                    <div class="flex items-center gap-4">
                                        <span class="text-blue-500 text-[11px] font-bold">${cantSelMaster}/${cantTotalMaster}</span>
                                        <div class="flex items-center gap-2 text-[11px] font-bold text-slate-500" onclick="event.stopPropagation()">
                                            <button type="button" onclick="window.excepcionesCargadas.forEach(e => e.concedido = true); window.renderizarModalPermisosIndiv();" class="hover:text-slate-800 text-slate-700 transition-colors">Todo</button>
                                            <span class="text-slate-200">|</span>
                                            <button type="button" onclick="window.excepcionesCargadas.forEach(e => e.concedido = false); window.renderizarModalPermisosIndiv();" class="hover:text-slate-800 text-slate-400 transition-colors">Nada</button>
                                        </div>
                                        <span class="iconify text-slate-400 text-xl transition-transform ${isMasterOpen ? 'rotate-180 text-slate-600' : ''}" data-icon="mdi:chevron-down"></span>
                                    </div>
                                </div>
                                <div class="transition-all ${isMasterOpen ? 'block' : 'hidden'} bg-white">
                                    <div class="flex flex-col">
                                        ${htmlSubs}
                                    </div>
                                </div>
                            </div>
                        `;
                    }

                    document.getElementById('permisosIndivCheckboxesContainer').innerHTML = `
                        <div class="flex flex-col gap-4">
                            <div class="flex items-center gap-3 mb-2">
                                <!-- Buscar -->
                                <div class="relative flex-1 bg-white border border-slate-200 rounded-2xl shadow-sm">
                                    <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-slate-400">
                                        <span class="iconify text-lg" data-icon="mdi:magnify"></span>
                                    </span>
                                    <input type="text" placeholder="Buscar permiso..." value="${escapeHtml(window.terminoBusquedaPermisosIndiv)}" oninput="window.terminoBusquedaPermisosIndiv = this.value; if(this.value){Object.keys(window.acordeonesMasterAbiertosIndiv).forEach(k => window.acordeonesMasterAbiertosIndiv[k] = true); Object.keys(window.acordeonesSubAbiertosIndiv).forEach(k => window.acordeonesSubAbiertosIndiv[k] = true);} window.renderizarModalPermisosIndiv();" class="w-full pl-11 pr-4 py-3 bg-transparent border-none text-[14px] font-medium focus:outline-none focus:ring-0 text-slate-700 placeholder-slate-400">
                                </div>
                                <!-- Todo | Nada -->
                                <div class="flex items-center gap-3 px-5 py-3 bg-white border border-slate-200 rounded-2xl text-[13px] font-bold text-slate-600 shadow-sm shrink-0">
                                    <button type="button" onclick="window.excepcionesCargadas.forEach(e => e.concedido = true); window.renderizarModalPermisosIndiv();" class="hover:text-slate-900 transition-colors text-slate-700">Todo</button>
                                    <span class="text-slate-200">|</span>
                                    <button type="button" onclick="window.excepcionesCargadas.forEach(e => e.concedido = false); window.renderizarModalPermisosIndiv();" class="hover:text-slate-900 transition-colors text-slate-400">Nada</button>
                                </div>
                                <!-- Seleccionados -->
                                <div class="flex items-center gap-2 px-5 py-3 border border-slate-200 bg-white rounded-2xl text-[13px] font-bold whitespace-nowrap shadow-sm shrink-0">
                                    <span class="iconify text-emerald-500 text-base" data-icon="mdi:check-all"></span>
                                    <span class="text-slate-700">${totalSeleccionados} excepciones</span>
                                </div>
                            </div>
                            <div>
                                ${htmlMaster}
                            </div>
                        </div>
                    `;
                };

                window.renderizarModalPermisosIndiv();

            } catch (err) {
                console.error('[abrirModalPermisosIndividuales]', err);
                const container = document.getElementById('permisosIndivCheckboxesContainer');
                if(container) container.innerHTML = '<div class="p-4 text-center text-sm text-red-500 flex flex-col items-center gap-2"><span class="iconify text-3xl" data-icon="mdi:alert-circle-outline"></span> Error al cargar los permisos del usuario.</div>';
            }
        }
"""

content = replace_function(content, "abrirModalEditarPermisos", roles_code)
content = replace_function(content, "abrirModalPermisosIndividuales", indiv_code)

# Add backdrop fix (gray semitransparent instead of totally transparent, since the previous screenshot had a slight dimming).
# Actually, the user said earlier "el modal no cierra aparte que no tiene que tener fondo gris debe ser trasparente 100%"
# I will keep the background transparent 100% since they explicitly requested it earlier.
content = content.replace('bg-slate-900/40 backdrop-blur-sm', 'bg-transparent')

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Roles Modal EXACT styling applied based on latest screenshot AND ONLY TWO MASTER ACCORDIONS!")
