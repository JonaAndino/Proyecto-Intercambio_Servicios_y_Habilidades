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


indiv_code = """window.abrirModalPermisosIndividuales = async function(idUsuario, nombre, idRol) {
            idUsuarioEditandoPermisos = idUsuario;
            
            // Inicializar estado de permisos
            window.terminoBusquedaPermisosIndiv = '';
            window.acordeonesAbiertosIndiv = { 'Administrador': false, 'Menú de Navegación': false };
            
            const modalRoot = document.getElementById('permisosIndivModalRoot');
            modalRoot.innerHTML = `
                <div id="permisosIndivBackdrop" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-[9998]" onclick="cerrarModalPermisosIndividuales()"></div>
                <div id="permisosIndivCard" class="relative bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] shadow-[0_20px_60px_rgb(0,0,0,0.2)] border border-slate-100 dark:border-gray-800 flex flex-col overflow-hidden z-[9999] transition-all m-auto">
                    <div class="flex items-center justify-between p-5 border-b border-slate-100 dark:border-gray-800 shrink-0 bg-white dark:bg-gray-900">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-indigo-50 dark:bg-indigo-900/30 rounded-2xl flex items-center justify-center text-indigo-600 dark:text-indigo-400 border border-indigo-100 dark:border-indigo-800/50">
                                <span class="iconify text-2xl" data-icon="mdi:shield-account"></span>
                            </div>
                            <div>
                                <h3 id="permisosIndivNombre" class="text-xl font-black text-slate-900 dark:text-white tracking-tight">Permisos de Usuario: ${nombre}</h3>
                                <p class="text-[13px] text-slate-500 dark:text-gray-400 mt-0.5 font-medium">Habilita (concedido) o deshabilita (denegado) excepciones de accesos individualmente.</p>
                            </div>
                        </div>
                        <button onclick="cerrarModalPermisosIndividuales()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 hover:bg-slate-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-slate-500 dark:text-gray-400 transition-colors cursor-pointer" aria-label="Cerrar modal">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    <div class="p-6 overflow-y-auto flex-1 custom-scrollbar" id="permisosIndivCheckboxesContainer">
                        <div class="flex flex-col items-center justify-center gap-3 py-10">
                            <span class="iconify text-4xl animate-spin text-indigo-500" data-icon="mdi:loading"></span> 
                            <span class="text-slate-500 font-medium">Cargando permisos...</span>
                        </div>
                    </div>
                    <div class="p-5 bg-white dark:bg-gray-900 border-t border-slate-100 dark:border-gray-800 flex justify-end gap-3 shrink-0">
                        <button type="button" onclick="cerrarModalPermisosIndividuales()" class="px-6 py-2.5 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:bg-slate-50 dark:hover:bg-gray-800 text-slate-700 dark:text-gray-300 text-sm font-bold transition-all cursor-pointer shadow-sm">Cancelar</button>
                        <button type="button" onclick="guardarPermisosIndividuales()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-sm font-bold shadow-md shadow-blue-600/20 transition-all flex items-center gap-2 cursor-pointer">
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

                window.actualizarExcepcionTemporal = (clave, val) => {
                    const idx = window.excepcionesCargadas.findIndex(e => e.link === clave);
                    if (val === '') {
                        if (idx !== -1) window.excepcionesCargadas.splice(idx, 1);
                    } else {
                        const concedido = val === '1';
                        if (idx !== -1) window.excepcionesCargadas[idx].concedido = concedido;
                        else window.excepcionesCargadas.push({ link: clave, concedido: concedido });
                    }
                    window.renderizarModalPermisosIndiv();
                };

                window.renderizarModalPermisosIndiv = () => {
                    const isPermisoAdmin = (clave) => clave === clave.toUpperCase();
                    
                    const grupos = {
                        'Administrador': { icon: 'mdi:shield-star-outline', permisos: [] },
                        'Menú de Navegación': { icon: 'mdi:compass-outline', permisos: [] }
                    };

                    todosLosPermisosDisponibles.forEach(p => {
                        if (window.terminoBusquedaPermisosIndiv && 
                            !p.nombre.toLowerCase().includes(window.terminoBusquedaPermisosIndiv.toLowerCase()) && 
                            !p.clave.toLowerCase().includes(window.terminoBusquedaPermisosIndiv.toLowerCase())) {
                            return;
                        }
                        
                        if (isPermisoAdmin(p.clave)) {
                            grupos['Administrador'].permisos.push(p);
                        } else {
                            grupos['Menú de Navegación'].permisos.push(p);
                        }
                    });

                    let totalSeleccionados = window.excepcionesCargadas.length;

                    let htmlGrupos = '';
                    for (const [nombreGrupo, data] of Object.entries(grupos)) {
                        const cantTotal = data.permisos.length;
                        if (cantTotal === 0) continue;
                        
                        const excepcionesGrupo = data.permisos.filter(p => window.excepcionesCargadas.find(e => e.link === p.clave)).length;
                        const isOpen = window.acordeonesAbiertosIndiv[nombreGrupo];

                        const htmlPermisos = data.permisos.map(p => {
                            const iconoSVG = getIconoOpcion(p.clave);
                            const exc = window.excepcionesCargadas.find(e => e.link === p.clave);
                            const rolLoTiene = window.rolCargadoParaIndiv.permisos && window.rolCargadoParaIndiv.permisos.includes(p.clave);
                            
                            let val = '';
                            if (exc) val = exc.concedido ? '1' : '0';

                            let estadoFinal = rolLoTiene;
                            if (exc) estadoFinal = exc.concedido;

                            let colorFondo = 'border-transparent bg-white dark:bg-gray-800 hover:bg-slate-50 dark:hover:bg-gray-800/80 shadow-sm';
                            let colorIcono = 'text-slate-500 dark:text-gray-400 bg-slate-50 dark:bg-gray-900 border border-slate-100 dark:border-gray-700';
                            
                            if (estadoFinal) {
                                if (val === '1') {
                                    colorFondo = 'border-green-200 dark:border-green-800 bg-green-50/30 dark:bg-green-900/10 shadow-sm';
                                    colorIcono = 'text-green-500 dark:text-green-400 bg-green-50 dark:bg-green-900/30 border-green-100 dark:border-green-800/50';
                                } else {
                                    colorFondo = 'border-blue-200 dark:border-blue-800 bg-blue-50/30 dark:bg-blue-900/10 shadow-sm';
                                    colorIcono = 'text-blue-500 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 border-blue-100 dark:border-blue-800/50';
                                }
                            } else {
                                if (val === '0') {
                                    colorFondo = 'border-red-200 dark:border-red-800 bg-red-50/30 dark:bg-red-900/10 shadow-sm';
                                    colorIcono = 'text-red-500 dark:text-red-400 bg-red-50 dark:bg-red-900/30 border-red-100 dark:border-red-800/50';
                                }
                            }

                            return `
                                <div class="flex items-center justify-between p-3 rounded-2xl transition-colors border group mb-2 mx-2 ${colorFondo}">
                                    <div class="flex items-center gap-3 w-full">
                                        <div class="w-10 h-10 rounded-xl flex items-center justify-center transition-colors shrink-0 ${colorIcono}">
                                            <span class="iconify text-xl" data-icon="${iconoSVG}"></span>
                                        </div>
                                        <div class="flex-1 min-w-0 pr-2">
                                            <input type="text" value="${escapeHtml(p.nombre)}" onclick="event.stopPropagation()" onchange="guardarNombrePermisoGlobal('${p.clave}', this.value)" class="block w-full bg-transparent border-b border-transparent hover:border-slate-300 focus:border-blue-500 focus:outline-none focus:ring-0 text-sm font-bold text-slate-900 dark:text-white transition-colors cursor-text pb-0.5 mb-0.5 truncate" />
                                            <p class="text-[11px] text-slate-500 dark:text-gray-400 mt-0.5 truncate font-mono">${escapeHtml(p.clave)}</p>
                                        </div>
                                    </div>
                                    <div class="shrink-0 ml-2">
                                        <select onchange="window.actualizarExcepcionTemporal('${p.clave}', this.value)" class="text-[11px] font-bold border border-slate-200 dark:border-gray-700 rounded-lg px-2 py-1.5 bg-white dark:bg-gray-800 text-slate-700 dark:text-gray-300 shadow-sm focus:ring-2 focus:ring-blue-500 cursor-pointer outline-none">
                                            <option value="" ${val === '' ? 'selected' : ''}>Rol: ${rolLoTiene ? 'SÍ' : 'NO'}</option>
                                            <option value="1" ${val === '1' ? 'selected' : ''}>+ Conceder</option>
                                            <option value="0" ${val === '0' ? 'selected' : ''}>- Denegar</option>
                                        </select>
                                    </div>
                                </div>
                            `;
                        }).join('');

                        htmlGrupos += `
                            <div class="mb-3 rounded-2xl bg-slate-50 dark:bg-gray-800/40 border border-slate-100 dark:border-gray-700 overflow-hidden">
                                <div class="flex items-center justify-between p-4 cursor-pointer hover:bg-slate-100 dark:hover:bg-gray-800/60 transition-colors" onclick="window.acordeonesAbiertosIndiv['${nombreGrupo}'] = !window.acordeonesAbiertosIndiv['${nombreGrupo}']; window.renderizarModalPermisosIndiv();">
                                    <div class="flex items-center gap-3">
                                        <div class="w-8 h-8 rounded-full bg-white dark:bg-gray-700 flex items-center justify-center text-slate-700 dark:text-gray-200 shadow-sm">
                                            <span class="iconify" data-icon="${data.icon}"></span>
                                        </div>
                                        <h4 class="font-bold text-sm text-slate-800 dark:text-gray-100">${nombreGrupo}</h4>
                                    </div>
                                    <div class="flex items-center gap-4">
                                        <span class="px-2.5 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 text-xs font-bold">${excepcionesGrupo}/${cantTotal}</span>
                                        <span class="iconify text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}" data-icon="mdi:chevron-down"></span>
                                    </div>
                                </div>
                                <div class="transition-all ${isOpen ? 'block' : 'hidden'} pb-2">
                                    ${htmlPermisos}
                                </div>
                            </div>
                        `;
                    }

                    document.getElementById('permisosIndivCheckboxesContainer').innerHTML = `
                        <div class="flex flex-col gap-4">
                            <div class="flex items-center justify-between gap-4 bg-white dark:bg-gray-900 sticky top-0 z-10 pb-2">
                                <div class="relative flex-1">
                                    <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                                        <span class="iconify" data-icon="mdi:magnify"></span>
                                    </span>
                                    <input type="text" placeholder="Buscar permiso..." value="${escapeHtml(window.terminoBusquedaPermisosIndiv)}" oninput="window.terminoBusquedaPermisosIndiv = this.value; if(this.value){window.acordeonesAbiertosIndiv = {'Administrador': true, 'Menú de Navegación': true};} window.renderizarModalPermisosIndiv();" class="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-gray-800 border border-slate-200 dark:border-gray-700 rounded-xl text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors">
                                </div>
                                <div class="flex items-center gap-1.5 px-3 py-2 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-800/50 rounded-xl text-[11px] font-bold">
                                    <span class="iconify text-sm" data-icon="mdi:shield-alert-outline"></span>
                                    <span>${totalSeleccionados} excepciones</span>
                                </div>
                            </div>
                            <div class="mt-2">
                                ${htmlGrupos}
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

content = replace_function(content, "abrirModalPermisosIndividuales", indiv_code)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Accordion modal for Permisos Individuales built successfully!")
