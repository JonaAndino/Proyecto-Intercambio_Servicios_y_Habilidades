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
            
            window.terminoBusquedaPermisosIndiv = '';
            window.acordeonesAbiertosIndiv = { 
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

            const modalRoot = document.getElementById('permisosIndivModalRoot');
            modalRoot.innerHTML = `
                <div id="permisosIndivBackdrop" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-[9998]" onclick="cerrarModalPermisosIndividuales()"></div>
                <div id="permisosIndivCard" class="relative bg-white rounded-3xl w-full max-w-[900px] max-h-[90vh] shadow-[0_20px_60px_rgb(0,0,0,0.2)] border border-slate-100 flex flex-col overflow-hidden z-[9999] transition-all m-auto">
                    <div class="flex items-center justify-between p-6 border-b border-slate-100 shrink-0 bg-white">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-600">
                                <span class="iconify text-2xl" data-icon="mdi:shield-account"></span>
                            </div>
                            <div>
                                <h3 id="permisosIndivNombre" class="text-xl font-black text-slate-800 tracking-tight">Permisos de Usuario: ${nombre}</h3>
                                <p class="text-sm text-slate-400 mt-1 font-medium">Habilita o deshabilita excepciones de accesos individualmente.</p>
                            </div>
                        </div>
                        <button onclick="cerrarModalPermisosIndividuales()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-50 hover:bg-slate-100 text-slate-400 transition-colors cursor-pointer" aria-label="Cerrar modal">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    <div class="p-8 overflow-y-auto flex-1 custom-scrollbar" id="permisosIndivCheckboxesContainer">
                        <div class="flex flex-col items-center justify-center gap-3 py-10">
                            <span class="iconify text-4xl animate-spin text-blue-500" data-icon="mdi:loading"></span> 
                            <span class="text-slate-500 font-medium">Cargando permisos...</span>
                        </div>
                    </div>
                    <div class="px-8 py-5 bg-white border-t border-slate-100 flex justify-end gap-3 shrink-0">
                        <button type="button" onclick="cerrarModalPermisosIndividuales()" class="px-6 py-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-sm font-bold transition-all cursor-pointer">Cancelar</button>
                        <button type="button" onclick="guardarPermisosIndividuales()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold transition-all cursor-pointer shadow-md shadow-blue-500/20">
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
                    const grupos = {};
                    
                    todosLosPermisosDisponibles.forEach(p => {
                        const map = MAPEO_AVANZADO[p.clave] || { grupo: 'Otros Permisos', nombre: p.nombre, icon: 'mdi:checkbox-marked-circle-outline', badgeText: 'PERMISO', badgeColor: 'bg-slate-100 text-slate-700' };
                        
                        if (window.terminoBusquedaPermisosIndiv && 
                            !map.nombre.toLowerCase().includes(window.terminoBusquedaPermisosIndiv.toLowerCase()) && 
                            !p.clave.toLowerCase().includes(window.terminoBusquedaPermisosIndiv.toLowerCase())) {
                            return;
                        }
                        
                        if (!grupos[map.grupo]) grupos[map.grupo] = { permisos: [] };
                        grupos[map.grupo].permisos.push({ ...p, ...map });
                    });

                    let totalSeleccionados = window.excepcionesCargadas.length;
                    let htmlGrupos = '';
                    
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
                        
                        const excepcionesGrupo = data.permisos.filter(p => window.excepcionesCargadas.find(e => e.link === p.clave)).length;
                        const isOpen = window.acordeonesAbiertosIndiv[nombreGrupo];

                        const htmlPermisos = data.permisos.map(p => {
                            const exc = window.excepcionesCargadas.find(e => e.link === p.clave);
                            const rolLoTiene = window.rolCargadoParaIndiv.permisos && window.rolCargadoParaIndiv.permisos.includes(p.clave);
                            
                            let val = '';
                            if (exc) val = exc.concedido ? '1' : '0';

                            let estadoFinal = rolLoTiene;
                            if (exc) estadoFinal = exc.concedido;

                            let bgSelect = 'bg-slate-50 border-slate-200 text-slate-700';
                            if (val === '1') bgSelect = 'bg-emerald-50 border-emerald-200 text-emerald-700';
                            if (val === '0') bgSelect = 'bg-red-50 border-red-200 text-red-700';
                            
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
                                        <select onchange="window.actualizarExcepcionTemporal('${p.clave}', this.value)" class="text-xs font-bold border rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer ${bgSelect}">
                                            <option value="" ${val === '' ? 'selected' : ''}>Neutro (Rol: ${rolLoTiene ? 'SÍ' : 'NO'})</option>
                                            <option value="1" ${val === '1' ? 'selected' : ''}>+ Conceder</option>
                                            <option value="0" ${val === '0' ? 'selected' : ''}>- Denegar</option>
                                        </select>
                                    </div>
                                </div>
                            `;
                        }).join('');

                        htmlGrupos += `
                            <div class="mb-4 rounded-xl bg-slate-50 border border-slate-100 overflow-hidden">
                                <div class="flex items-center justify-between px-6 py-4 cursor-pointer" onclick="window.acordeonesAbiertosIndiv['${nombreGrupo}'] = !window.acordeonesAbiertosIndiv['${nombreGrupo}']; window.renderizarModalPermisosIndiv();">
                                    <div class="flex items-center gap-3">
                                        <h4 class="font-bold text-slate-700 text-lg">${nombreGrupo}</h4>
                                    </div>
                                    <div class="flex items-center gap-6">
                                        <span class="text-xs font-bold text-slate-500">${excepcionesGrupo}/${cantTotal}</span>
                                        <span class="iconify text-slate-400 text-xl transition-transform ${isOpen ? 'rotate-180' : ''}" data-icon="mdi:chevron-down"></span>
                                    </div>
                                </div>
                                <div class="transition-all ${isOpen ? 'block' : 'hidden'} bg-white">
                                    ${htmlPermisos}
                                </div>
                            </div>
                        `;
                    }

                    document.getElementById('permisosIndivCheckboxesContainer').innerHTML = `
                        <div class="flex flex-col gap-4">
                            <div class="flex items-center justify-between gap-4 mb-4">
                                <div class="relative flex-1">
                                    <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-slate-400">
                                        <span class="iconify text-xl" data-icon="mdi:magnify"></span>
                                    </span>
                                    <input type="text" placeholder="Buscar permiso..." value="${escapeHtml(window.terminoBusquedaPermisosIndiv)}" oninput="window.terminoBusquedaPermisosIndiv = this.value; if(this.value){Object.keys(window.acordeonesAbiertosIndiv).forEach(k => window.acordeonesAbiertosIndiv[k] = true);} window.renderizarModalPermisosIndiv();" class="w-full pl-12 pr-4 py-3 bg-white border border-slate-200 rounded-2xl text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors">
                                </div>
                                <div class="flex items-center gap-2 px-4 py-2 border border-blue-200 bg-white text-blue-600 rounded-full text-xs font-bold">
                                    <span class="iconify text-lg" data-icon="mdi:shield-alert-outline"></span>
                                    <span>${totalSeleccionados} excepciones</span>
                                </div>
                            </div>
                            <div>
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

print("Permisos Individuales Modal visually updated!")
