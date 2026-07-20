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
            window.acordeonesAbiertos = { 'Administrador': false, 'Menú de Navegación': false };

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

            window.renderizarModalPermisos = () => {
                const isPermisoAdmin = (clave) => clave === clave.toUpperCase();
                
                // Agrupar
                const grupos = {
                    'Administrador': { icon: 'mdi:shield-star-outline', permisos: [] },
                    'Menú de Navegación': { icon: 'mdi:compass-outline', permisos: [] }
                };

                todosLosPermisosDisponibles.forEach(p => {
                    // Filtrar por búsqueda
                    if (window.terminoBusquedaPermisos && 
                        !p.nombre.toLowerCase().includes(window.terminoBusquedaPermisos.toLowerCase()) && 
                        !p.clave.toLowerCase().includes(window.terminoBusquedaPermisos.toLowerCase())) {
                        return;
                    }
                    
                    if (isPermisoAdmin(p.clave)) {
                        grupos['Administrador'].permisos.push(p);
                    } else {
                        grupos['Menú de Navegación'].permisos.push(p);
                    }
                });

                let totalSeleccionados = window.permisosSeleccionados.size;

                let htmlGrupos = '';
                for (const [nombreGrupo, data] of Object.entries(grupos)) {
                    const cantTotal = data.permisos.length;
                    if (cantTotal === 0) continue;
                    
                    const seleccionadosGrupo = data.permisos.filter(p => window.permisosSeleccionados.has(p.clave)).length;
                    const isOpen = window.acordeonesAbiertos[nombreGrupo];

                    const htmlPermisos = data.permisos.map(p => {
                        const activo = window.permisosSeleccionados.has(p.clave);
                        const iconoSVG = getIconoOpcion(p.clave);
                        return `
                            <div class="flex items-center justify-between p-3 rounded-2xl bg-white dark:bg-gray-800/50 hover:bg-slate-50 dark:hover:bg-gray-800 transition-colors border border-transparent hover:border-slate-200 dark:hover:border-gray-700 group mb-2 mx-2 shadow-sm">
                                <div class="flex items-center gap-3 w-full">
                                    <div class="w-10 h-10 rounded-xl bg-slate-50 dark:bg-gray-900 shadow-sm border border-slate-100 dark:border-gray-700 flex items-center justify-center text-slate-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors shrink-0">
                                        <span class="iconify text-xl" data-icon="${iconoSVG}"></span>
                                    </div>
                                    <div class="flex-1 min-w-0 pr-2">
                                        <input type="text" value="${escapeHtml(p.nombre)}" onclick="event.stopPropagation()" onchange="guardarNombrePermisoGlobal('${p.clave}', this.value)" class="block w-full bg-transparent border-b border-transparent hover:border-slate-300 focus:border-blue-500 focus:outline-none focus:ring-0 text-sm font-bold text-slate-900 dark:text-white transition-colors cursor-text pb-0.5 mb-0.5 truncate" />
                                        <p class="text-[11px] text-slate-400 dark:text-gray-500 mt-0.5 truncate font-mono">${escapeHtml(p.clave)}</p>
                                    </div>
                                </div>
                                <label class="relative inline-flex items-center cursor-pointer shrink-0 ml-2">
                                    <input type="checkbox" value="${p.clave}" ${activo ? 'checked' : ''} onchange="togglePermisoRol('${p.clave}', this.checked)" class="sr-only peer">
                                    <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                                </label>
                            </div>
                        `;
                    }).join('');

                    htmlGrupos += `
                        <div class="mb-3 rounded-2xl bg-slate-50 dark:bg-gray-800/40 border border-slate-100 dark:border-gray-700 overflow-hidden">
                            <div class="flex items-center justify-between p-4 cursor-pointer hover:bg-slate-100 dark:hover:bg-gray-800/60 transition-colors" onclick="toggleAcordeonPermisos('${nombreGrupo}')">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-white dark:bg-gray-700 flex items-center justify-center text-slate-700 dark:text-gray-200 shadow-sm">
                                        <span class="iconify" data-icon="${data.icon}"></span>
                                    </div>
                                    <h4 class="font-bold text-sm text-slate-800 dark:text-gray-100">${nombreGrupo}</h4>
                                </div>
                                <div class="flex items-center gap-4">
                                    <span class="px-2.5 py-0.5 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-bold">${seleccionadosGrupo}/${cantTotal}</span>
                                    <div class="flex items-center gap-1 text-[11px] font-bold text-slate-500 dark:text-gray-400 bg-white dark:bg-gray-900 rounded-lg p-1 border border-slate-200 dark:border-gray-700" onclick="event.stopPropagation()">
                                        <button onclick="seleccionarTodoGrupo('${nombreGrupo}', true)" class="px-2 py-1 rounded-md hover:bg-slate-100 dark:hover:bg-gray-800 transition-colors">Todo</button>
                                        <span class="w-px h-3 bg-slate-200 dark:bg-gray-700"></span>
                                        <button onclick="seleccionarTodoGrupo('${nombreGrupo}', false)" class="px-2 py-1 rounded-md hover:bg-slate-100 dark:hover:bg-gray-800 transition-colors">Nada</button>
                                    </div>
                                    <span class="iconify text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}" data-icon="mdi:chevron-down"></span>
                                </div>
                            </div>
                            <div class="transition-all ${isOpen ? 'block' : 'hidden'} pb-2">
                                ${htmlPermisos}
                            </div>
                        </div>
                    `;
                }

                document.getElementById('permisosCheckboxesContainer').innerHTML = `
                    <div class="flex flex-col gap-4">
                        <div class="flex items-center justify-between gap-4 bg-white dark:bg-gray-900 sticky top-0 z-10 pb-2">
                            <div class="relative flex-1">
                                <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                                    <span class="iconify" data-icon="mdi:magnify"></span>
                                </span>
                                <input type="text" id="busquedaPermisosModal" placeholder="Buscar permiso..." value="${escapeHtml(window.terminoBusquedaPermisos)}" oninput="buscarPermisosEnModal(this.value)" class="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-gray-800 border border-slate-200 dark:border-gray-700 rounded-xl text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors">
                            </div>
                            <div class="flex items-center gap-1 text-[11px] font-bold text-slate-500 dark:text-gray-400 border border-slate-200 dark:border-gray-700 rounded-xl p-1 bg-white dark:bg-gray-800">
                                <button onclick="seleccionarTodoGlobal(true)" class="px-3 py-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-gray-700 transition-colors">Todo</button>
                                <span class="w-px h-4 bg-slate-200 dark:bg-gray-700"></span>
                                <button onclick="seleccionarTodoGlobal(false)" class="px-3 py-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-gray-700 transition-colors">Nada</button>
                            </div>
                            <div class="flex items-center gap-1.5 px-3 py-2 bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 border border-green-200 dark:border-green-800/50 rounded-xl text-[11px] font-bold">
                                <span class="iconify text-sm" data-icon="mdi:check-all"></span>
                                <span>${totalSeleccionados} seleccionados</span>
                            </div>
                        </div>
                        <div class="mt-2">
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
                // Si busca algo, abrir todos los acordeones temporalmente para ver resultados
                if (val) {
                    window.acordeonesAbiertos = { 'Administrador': true, 'Menú de Navegación': true };
                }
                window.renderizarModalPermisos();
            };

            window.seleccionarTodoGrupo = (grupo, seleccionar) => {
                const isPermisoAdmin = (clave) => clave === clave.toUpperCase();
                todosLosPermisosDisponibles.forEach(p => {
                    const esDeEsteGrupo = (grupo === 'Administrador' && isPermisoAdmin(p.clave)) || (grupo === 'Menú de Navegación' && !isPermisoAdmin(p.clave));
                    if (esDeEsteGrupo) {
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

            // Reemplazar la función de guardado para que lea del Set
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

            // Estructura principal del modal wrapper (Reemplazar la vieja)
            const modalRoot = document.getElementById('permisosModalRoot');
            modalRoot.innerHTML = `
                <div id="permisosBackdrop" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-[9998]" onclick="cerrarModalEditarPermisos()"></div>
                <div id="permisosCard" class="relative bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] shadow-[0_20px_60px_rgb(0,0,0,0.2)] border border-slate-100 dark:border-gray-800 flex flex-col overflow-hidden z-[9999] transition-all m-auto">
                    <div class="flex items-center justify-between p-5 border-b border-slate-100 dark:border-gray-800 shrink-0 bg-white dark:bg-gray-900">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-blue-50 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-800/50">
                                <span class="iconify text-2xl" data-icon="mdi:shield-key-outline"></span>
                            </div>
                            <div>
                                <h3 id="permisosRoleNombre" class="text-xl font-black text-slate-900 dark:text-white tracking-tight">Asignar permisos al rol: ${rol.nombre_rol}</h3>
                                <p class="text-[13px] text-slate-500 dark:text-gray-400 mt-0.5 font-medium">Gestiona los accesos y privilegios de este rol.</p>
                            </div>
                        </div>
                        <button onclick="cerrarModalEditarPermisos()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 hover:bg-slate-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-slate-500 dark:text-gray-400 transition-colors cursor-pointer" aria-label="Cerrar modal">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    <div class="p-6 overflow-y-auto flex-1 custom-scrollbar" id="permisosCheckboxesContainer">
                        <!-- Se llena dinámicamente -->
                    </div>
                    <div class="p-5 bg-white dark:bg-gray-900 border-t border-slate-100 dark:border-gray-800 flex justify-end gap-3 shrink-0">
                        <button type="button" onclick="cerrarModalEditarPermisos()" class="px-6 py-2.5 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:bg-slate-50 dark:hover:bg-gray-800 text-slate-700 dark:text-gray-300 text-sm font-bold transition-all cursor-pointer shadow-sm">Cancelar</button>
                        <button type="button" onclick="guardarPermisosRol()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-sm font-bold shadow-md shadow-blue-600/20 transition-all flex items-center gap-2 cursor-pointer">
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

print("Accordion modal built successfully!")
