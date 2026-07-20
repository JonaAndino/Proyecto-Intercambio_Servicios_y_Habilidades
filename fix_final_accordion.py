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


roles_code = """window.abrirModalEditarPermisos = function(idRol) {
            idRolEditandoPermisos = idRol;
            const rol = todosLosRolesCargados.find(r => r.id_rol === idRol);
            if (!rol) return;
            
            // Inicializar estado de permisos
            window.permisosSeleccionados = new Set(rol.permisos || []);
            window.terminoBusquedaPermisos = '';
            
            // ACORDEONES ABIERTOS POR DEFECTO
            window.acordeonesAbiertos = { 
                'Panel de Administración': true, 
                'Directorio de Usuarios': true,
                'Solicitudes de Verificación': true,
                'Menú de Navegación': true,
                'Otros Permisos': true
            };

            const MAPEO_AVANZADO = {
                'VER_METRICAS': { grupo: 'Panel de Administración', nombre: 'Ver panel de métricas y reportes', icon: 'mdi:chart-pie', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-700' },
                'MODERAR_USUARIOS': { grupo: 'Directorio de Usuarios', nombre: 'Bloquear y moderar usuarios de la comunidad', icon: 'mdi:shield-account-outline', badgeText: 'ELIMINAR', badgeColor: 'bg-red-50 text-red-600' },
                'GESTIONAR_CONFIGURACION': { grupo: 'Panel de Administración', nombre: 'Gestionar configuración general del sistema', icon: 'mdi:cog-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-600' },
                'ACEPTAR_INTERCAMBIOS': { grupo: 'Panel de Administración', nombre: 'Aceptar y gestionar intercambios', icon: 'mdi:handshake-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-700' },
                'VER_HISTORIAL_PERSONAL': { grupo: 'Panel de Administración', nombre: 'Ver historial de actividades', icon: 'mdi:history', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-700' },
                'VER_DIRECTORIO': { grupo: 'Directorio de Usuarios', nombre: 'Ver listado y tabla del directorio general', icon: 'mdi:folder-account-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-700' },
                'CREAR_CUENTAS': { grupo: 'Directorio de Usuarios', nombre: 'Crear y enrolar nuevas cuentas de usuario', icon: 'mdi:account-plus-outline', badgeText: 'CREAR', badgeColor: 'bg-emerald-50 text-emerald-600' },
                'EDITAR_USUARIOS': { grupo: 'Directorio de Usuarios', nombre: 'Editar perfiles y datos de usuarios', icon: 'mdi:account-edit-outline', badgeText: 'EDITAR', badgeColor: 'bg-amber-50 text-amber-600' },
                'ASIGNAR_ROLES_PERMISOS': { grupo: 'Directorio de Usuarios', nombre: 'Asignar roles y permisos a usuarios', icon: 'mdi:shield-key-outline', badgeText: 'ADMIN', badgeColor: 'bg-purple-50 text-purple-600' },
                'VER_SOLICITUDES_VERIFICACION': { grupo: 'Solicitudes de Verificación', nombre: 'Ver y validar solicitudes de verificación', icon: 'mdi:check-decagram-outline', badgeText: 'VER', badgeColor: 'bg-slate-100 text-slate-700' },
                
                'descubrir': { grupo: 'Menú de Navegación', nombre: 'Acceso a Descubrir', icon: 'mdi:compass-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' },
                'perfil': { grupo: 'Menú de Navegación', nombre: 'Acceso a Perfil', icon: 'mdi:account-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' },
                'ordenesTrabajo': { grupo: 'Menú de Navegación', nombre: 'Acceso a Órdenes de Trabajo', icon: 'mdi:briefcase-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' },
                'mensajes': { grupo: 'Menú de Navegación', nombre: 'Acceso a Mensajes', icon: 'mdi:message-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' },
                'solicitudesEnviadas': { grupo: 'Menú de Navegación', nombre: 'Acceso a Solicitudes', icon: 'mdi:file-document-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' },
                'favoritos': { grupo: 'Menú de Navegación', nombre: 'Acceso a Favoritos', icon: 'mdi:heart-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' },
                'historial': { grupo: 'Menú de Navegación', nombre: 'Acceso a Historial', icon: 'mdi:history', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' },
                'reportes': { grupo: 'Menú de Navegación', nombre: 'Acceso a Reportes', icon: 'mdi:chart-bar', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600' }
            };

            window.renderizarModalPermisos = () => {
                
                // Agrupar permisos
                const grupos = {};
                
                todosLosPermisosDisponibles.forEach(p => {
                    const map = MAPEO_AVANZADO[p.clave] || { grupo: 'Otros Permisos', nombre: p.nombre, icon: 'mdi:checkbox-marked-circle-outline', badgeText: 'PERMISO', badgeColor: 'bg-slate-100 text-slate-700' };
                    
                    if (window.terminoBusquedaPermisos && 
                        !map.nombre.toLowerCase().includes(window.terminoBusquedaPermisos.toLowerCase()) && 
                        !p.clave.toLowerCase().includes(window.terminoBusquedaPermisos.toLowerCase())) {
                        return;
                    }
                    
                    if (!grupos[map.grupo]) grupos[map.grupo] = { permisos: [] };
                    grupos[map.grupo].permisos.push({ ...p, ...map });
                });

                let totalSeleccionados = window.permisosSeleccionados.size;

                let htmlGrupos = '';
                
                // Orden deseado de los grupos:
                const ordenGrupos = ['Panel de Administración', 'Directorio de Usuarios', 'Solicitudes de Verificación', 'Menú de Navegación', 'Otros Permisos'];
                const gruposOrdenados = Object.keys(grupos).sort((a, b) => {
                    let idxA = ordenGrupos.indexOf(a);
                    let idxB = ordenGrupos.indexOf(b);
                    if (idxA === -1) idxA = 99;
                    if (idxB === -1) idxB = 99;
                    return idxA - idxB;
                });

                for (const nombreGrupo of gruposOrdenados) {
                    const data = grupos[nombreGrupo];
                    const cantTotal = data.permisos.length;
                    if (cantTotal === 0) continue;
                    
                    const seleccionadosGrupo = data.permisos.filter(p => window.permisosSeleccionados.has(p.clave)).length;
                    const isOpen = window.acordeonesAbiertos[nombreGrupo];

                    const htmlPermisos = data.permisos.map(p => {
                        const activo = window.permisosSeleccionados.has(p.clave);
                        
                        return `
                            <div class="flex items-center justify-between py-4 px-6 hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0">
                                <div class="flex items-center gap-4 flex-1">
                                    <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 shrink-0">
                                        <span class="iconify text-lg" data-icon="${p.icon}"></span>
                                    </div>
                                    <span class="text-[15px] font-bold text-slate-700">${escapeHtml(p.nombre)}</span>
                                </div>
                                <div class="flex items-center gap-6 shrink-0">
                                    <span class="px-3 py-1 rounded-md text-[11px] font-bold tracking-wide ${p.badgeColor}">${p.badgeText}</span>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" value="${p.clave}" ${activo ? 'checked' : ''} onchange="togglePermisoRol('${p.clave}', this.checked)" class="sr-only peer">
                                        <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                                    </label>
                                </div>
                            </div>
                        `;
                    }).join('');

                    // The exact header matching the screenshot
                    htmlGrupos += `
                        <div class="mb-4 rounded-xl bg-slate-50 border border-slate-100 overflow-hidden">
                            <div class="flex items-center justify-between px-6 py-4 cursor-pointer" onclick="toggleAcordeonPermisos('${nombreGrupo}')">
                                <div class="flex items-center gap-3">
                                    <h4 class="font-bold text-slate-700 text-lg">${nombreGrupo}</h4>
                                </div>
                                <div class="flex items-center gap-6">
                                    <span class="text-xs font-bold text-slate-500">${seleccionadosGrupo}/${cantTotal}</span>
                                    <div class="flex items-center gap-2 text-xs font-bold text-slate-500" onclick="event.stopPropagation()">
                                        <button onclick="seleccionarTodoGrupo('${nombreGrupo}', true)" class="hover:text-slate-800 transition-colors">Todo</button>
                                        <span class="text-slate-300">Nada</span>
                                    </div>
                                    <span class="iconify text-slate-400 text-xl transition-transform ${isOpen ? 'rotate-180' : ''}" data-icon="mdi:chevron-down"></span>
                                </div>
                            </div>
                            <div class="transition-all ${isOpen ? 'block' : 'hidden'} bg-white">
                                ${htmlPermisos}
                            </div>
                        </div>
                    `;
                }

                document.getElementById('permisosCheckboxesContainer').innerHTML = `
                    <div class="flex flex-col gap-4">
                        <div class="flex items-center justify-between gap-4 mb-4">
                            <div class="relative flex-1">
                                <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-slate-400">
                                    <span class="iconify text-xl" data-icon="mdi:magnify"></span>
                                </span>
                                <input type="text" placeholder="Buscar permiso..." value="${escapeHtml(window.terminoBusquedaPermisos)}" oninput="buscarPermisosEnModal(this.value)" class="w-full pl-12 pr-4 py-3 bg-white border border-slate-200 rounded-2xl text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors">
                            </div>
                            <div class="flex items-center gap-3 px-4 py-2 text-xs font-bold text-slate-500 border border-slate-200 rounded-full bg-white">
                                <button onclick="seleccionarTodoGlobal(true)" class="hover:text-slate-800 transition-colors">Todo</button>
                                <span class="w-px h-3 bg-slate-300"></span>
                                <button onclick="seleccionarTodoGlobal(false)" class="hover:text-slate-800 transition-colors">Nada</button>
                            </div>
                            <div class="flex items-center gap-2 px-4 py-2 border border-emerald-200 bg-white text-emerald-600 rounded-full text-xs font-bold">
                                <span class="iconify text-lg" data-icon="mdi:check"></span>
                                <span>${totalSeleccionados} seleccionados</span>
                            </div>
                        </div>
                        <div>
                            ${htmlGrupos}
                        </div>
                    </div>
                `;
            };

            window.togglePermisoRol = (clave, isChecked) => {
                if (isChecked) window.permisosSeleccionados.add(clave);
                else window.permisosSeleccionados.delete(clave);
                window.renderizarModalPermisos();
            };

            window.toggleAcordeonPermisos = (grupo) => {
                window.acordeonesAbiertos[grupo] = !window.acordeonesAbiertos[grupo];
                window.renderizarModalPermisos();
            };

            window.buscarPermisosEnModal = (val) => {
                window.terminoBusquedaPermisos = val;
                if (val) {
                    Object.keys(window.acordeonesAbiertos).forEach(k => window.acordeonesAbiertos[k] = true);
                }
                window.renderizarModalPermisos();
            };

            window.seleccionarTodoGrupo = (grupo, seleccionar) => {
                todosLosPermisosDisponibles.forEach(p => {
                    const MAPEO_AVANZADO = {
                        'VER_METRICAS': { grupo: 'Panel de Administración' },
                        'MODERAR_USUARIOS': { grupo: 'Directorio de Usuarios' },
                        'GESTIONAR_CONFIGURACION': { grupo: 'Panel de Administración' },
                        'ACEPTAR_INTERCAMBIOS': { grupo: 'Panel de Administración' },
                        'VER_HISTORIAL_PERSONAL': { grupo: 'Panel de Administración' },
                        'VER_DIRECTORIO': { grupo: 'Directorio de Usuarios' },
                        'CREAR_CUENTAS': { grupo: 'Directorio de Usuarios' },
                        'EDITAR_USUARIOS': { grupo: 'Directorio de Usuarios' },
                        'ASIGNAR_ROLES_PERMISOS': { grupo: 'Directorio de Usuarios' },
                        'VER_SOLICITUDES_VERIFICACION': { grupo: 'Solicitudes de Verificación' },
                        'descubrir': { grupo: 'Menú de Navegación' },
                        'perfil': { grupo: 'Menú de Navegación' },
                        'ordenesTrabajo': { grupo: 'Menú de Navegación' },
                        'mensajes': { grupo: 'Menú de Navegación' },
                        'solicitudesEnviadas': { grupo: 'Menú de Navegación' },
                        'favoritos': { grupo: 'Menú de Navegación' },
                        'historial': { grupo: 'Menú de Navegación' },
                        'reportes': { grupo: 'Menú de Navegación' }
                    };
                    const map = MAPEO_AVANZADO[p.clave] || { grupo: 'Otros Permisos' };
                    if (map.grupo === grupo) {
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
                        cargarRoles();
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
                <div id="permisosCard" class="relative bg-white rounded-3xl w-full max-w-[900px] max-h-[90vh] shadow-[0_20px_60px_rgb(0,0,0,0.2)] border border-slate-100 flex flex-col overflow-hidden z-[9999] transition-all m-auto">
                    <div class="flex items-center justify-between p-6 border-b border-slate-100 shrink-0 bg-white">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-600">
                                <span class="iconify text-2xl" data-icon="mdi:shield-key-outline"></span>
                            </div>
                            <div>
                                <h3 id="permisosRoleNombre" class="text-xl font-black text-slate-800 tracking-tight">Asignar permisos al rol: ${rol.nombre_rol}</h3>
                                <p class="text-sm text-slate-400 mt-1 font-medium">Gestiona los accesos y privilegios de este rol.</p>
                            </div>
                        </div>
                        <button onclick="cerrarModalEditarPermisos()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-50 hover:bg-slate-100 text-slate-400 transition-colors cursor-pointer" aria-label="Cerrar modal">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    <div class="p-8 overflow-y-auto flex-1 custom-scrollbar" id="permisosCheckboxesContainer">
                        <!-- Se llena dinámicamente -->
                    </div>
                    <div class="px-8 py-5 bg-white border-t border-slate-100 flex justify-end gap-3 shrink-0">
                        <button type="button" onclick="cerrarModalEditarPermisos()" class="px-6 py-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-sm font-bold transition-all cursor-pointer">Cancelar</button>
                        <button type="button" onclick="guardarPermisosRol()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold transition-all cursor-pointer shadow-md shadow-blue-500/20">
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

content = replace_function(content, "abrirModalEditarPermisos", roles_code)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Roles Modal visually updated to perfectly match screenshots!")
