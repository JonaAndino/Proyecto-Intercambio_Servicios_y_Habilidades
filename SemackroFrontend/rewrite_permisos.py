import re

with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new code for abrirModalPermisosIndividuales
new_code = """
        window.abrirModalPermisosIndividuales = async function(idUsuario, nombre, idRol) {
            idUsuarioEditandoPermisos = idUsuario;
            document.getElementById('permisosIndivNombre').textContent = `Permisos de ${nombre}`;
            
            const container = document.getElementById('permisosIndivCheckboxesContainer');
            container.innerHTML = '<div class="p-4 text-center text-sm text-gray-500">Cargando permisos...</div>';
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
                            todosLosRolesCargados = jsonRoles.data;
                        }
                    }
                }

                const resUsr = await fetch(`${window.APP_CONFIG.BACKEND_URL}/api/configuraciones/usuarios/${idUsuario}/permisos`);
                const dataUsr = resUsr.ok ? await resUsr.json() : { data: [] };
                const excepciones = dataUsr.data || [];
                
                const rolIdFormat = parseInt(idRol, 10);
                const rol = todosLosRolesCargados.find(r => r.id_rol === rolIdFormat) || { permisos: [] };

                const allKeys = new Set(todosLosPermisosDisponibles.map(p => p.clave));
                Object.keys(MAPEO_GRUPOS_PERMISOS).forEach(key => {
                    if (!allKeys.has(key)) {
                        todosLosPermisosDisponibles.push({ clave: key, nombre: MAPEO_GRUPOS_PERMISOS[key].nombre || key });
                        allKeys.add(key);
                    }
                });

                const grupos = {};
                todosLosPermisosDisponibles.forEach(p => {
                    const baseClave = p.clave.split(':')[0];
                    if (p.clave.includes(':') && MAPEO_GRUPOS_PERMISOS[baseClave] && MAPEO_GRUPOS_PERMISOS[baseClave].isCrudBase) {
                        return;
                    }

                    const metadata = MAPEO_GRUPOS_PERMISOS[p.clave] || {
                        grupo: 'Administrador',
                        subgrupo: 'Panel de Administración',
                        nombre: p.nombre || p.clave,
                        tipo: p.clave === p.clave.toUpperCase() ? 'admin' : 'ver',
                        icon: 'mdi:shield-alert-outline',
                        isCrudBase: false
                    };
                    
                    const exc = excepciones.find(e => e.link === p.clave);
                    const rolLoTiene = rol.permisos && rol.permisos.includes(p.clave);
                    
                    let val = '';
                    if (exc) {
                        val = exc.concedido ? '1' : '0';
                    }

                    if (!grupos[metadata.grupo]) {
                        grupos[metadata.grupo] = {
                            nombre: metadata.grupo,
                            icon: getIconoGrupo(metadata.grupo),
                            permisos: []
                        };
                    }

                    if (metadata.isCrudBase) {
                        const acciones = ['ver', 'crear', 'editar', 'eliminar'];
                        if (p.clave === 'configGenerales') {
                            acciones.splice(3, 1); // no eliminar
                            acciones.splice(1, 1); // no crear
                        }
                        acciones.forEach(acc => {
                            const c = `${p.clave}:${acc}`;
                            const cExc = excepciones.find(e => e.link === c);
                            const cRol = rol.permisos && rol.permisos.includes(c);
                            let cVal = '';
                            if (cExc) cVal = cExc.concedido ? '1' : '0';

                            grupos[metadata.grupo].permisos.push({
                                clave: c,
                                nombre: `${acc.charAt(0).toUpperCase() + acc.slice(1)} ${metadata.nombre}`,
                                subgrupo: metadata.subgrupo || 'General',
                                categoria: metadata.nombre,
                                tipo: acc,
                                icon: acc === 'ver' ? metadata.icon : (acc === 'crear' ? 'mdi:plus-box-outline' : (acc === 'editar' ? 'mdi:pencil-outline' : 'mdi:trash-can-outline')),
                                rolLoTiene: cRol,
                                val: cVal
                            });
                        });
                    } else {
                        grupos[metadata.grupo].permisos.push({
                            clave: p.clave,
                            nombre: metadata.nombre,
                            subgrupo: metadata.subgrupo || 'General',
                            categoria: metadata.categoria || null,
                            tipo: metadata.tipo,
                            icon: metadata.icon,
                            rolLoTiene: rolLoTiene,
                            val: val
                        });
                    }
                });

                const ordenGrupos = { 'Menú de Navegación': 1, 'Administrador': 2, 'Otros Permisos': 3 };
                const gruposOrdenados = Object.values(grupos).sort((a, b) => {
                    const ordenA = ordenGrupos[a.nombre] || 99;
                    const ordenB = ordenGrupos[b.nombre] || 99;
                    if (ordenA !== ordenB) return ordenA - ordenB;
                    return a.nombre.localeCompare(b.nombre);
                });

                container.innerHTML = gruposOrdenados.map(g => {
                    const subgrupos = {};
                    g.permisos.forEach(p => {
                        const sub = p.subgrupo || 'General';
                        if (!subgrupos[sub]) subgrupos[sub] = [];
                        subgrupos[sub].push(p);
                    });

                    let htmlPermisos = '';

                    for (const [subNombre, perms] of Object.entries(subgrupos)) {
                        const renderRow = p => {
                            const estadoFinal = p.val !== '' ? p.val === '1' : p.rolLoTiene;
                            let colorFondo = 'border-slate-150 dark:border-gray-700 bg-slate-50/50 dark:bg-gray-900/30';
                            let colorTitulo = 'text-slate-800 dark:text-gray-300';
                            let colorIcono = 'text-gray-400';
                            let colorFinal = 'text-gray-500';
                            
                            if (estadoFinal) {
                                if (p.val === '1') {
                                    colorFondo = 'border-green-200 dark:border-green-800 bg-green-50/50 dark:bg-green-900/20';
                                    colorTitulo = 'text-green-800 dark:text-green-200';
                                    colorIcono = 'text-green-500';
                                    colorFinal = 'text-green-600';
                                } else {
                                    colorFondo = 'border-purple-200 dark:border-purple-800 bg-purple-50/50 dark:bg-purple-900/20';
                                    colorTitulo = 'text-purple-800 dark:text-purple-200';
                                    colorIcono = 'text-purple-500';
                                    colorFinal = 'text-purple-600';
                                }
                            } else {
                                if (p.val === '0') {
                                    colorFondo = 'border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/20';
                                    colorTitulo = 'text-red-800 dark:text-red-200';
                                    colorIcono = 'text-red-500';
                                    colorFinal = 'text-red-600';
                                }
                            }

                            const btnBaseClass = "px-2 py-1 text-[10px] font-bold uppercase transition-all duration-200 flex items-center justify-center border-y border-r first:border-l first:rounded-l-lg last:rounded-r-lg border-gray-300 dark:border-gray-600 focus:outline-none";
                            
                            const rolCls = p.val === '' ? 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white shadow-inner' : 'bg-white dark:bg-gray-800 text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-700';
                            const allowCls = p.val === '1' ? 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-400 border-emerald-300 dark:border-emerald-700 shadow-inner' : 'bg-white dark:bg-gray-800 text-gray-500 hover:bg-emerald-50 dark:hover:bg-emerald-900/20';
                            const denyCls = p.val === '0' ? 'bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-400 border-red-300 dark:border-red-700 shadow-inner' : 'bg-white dark:bg-gray-800 text-gray-500 hover:bg-red-50 dark:hover:bg-red-900/20';

                            return `
                            <div class="flex flex-col lg:flex-row lg:items-center justify-between py-3 px-4 mx-1 my-2 rounded-xl border ${colorFondo} transition-colors" data-rol-tiene="${p.rolLoTiene}">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full flex items-center justify-center icon-container ${colorIcono} ${p.val === '' ? 'bg-slate-200 dark:bg-gray-700/50' : (estadoFinal ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30')}">
                                        <span class="iconify text-sm" data-icon="${p.icon}"></span>
                                    </div>
                                    <div class="flex flex-col">
                                        <span class="text-[13px] font-semibold title-label ${colorTitulo}">${escapeHtml(p.nombre)}</span>
                                        <span class="text-[10px] font-bold tracking-wider status-label ${colorFinal} mt-0.5" id="final-label-${p.clave}">Final: ${estadoFinal ? 'ACCESO CONCEDIDO' : 'ACCESO DENEGADO'}</span>
                                    </div>
                                </div>
                                <div class="flex items-center justify-between lg:justify-end gap-3 mt-3 lg:mt-0 w-full lg:w-auto">
                                    <span class="w-20 text-center inline-block px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider ${getBadgeColorForTipo(p.tipo)}">
                                        ${p.tipo}
                                    </span>
                                    
                                    <div class="flex shadow-sm rounded-lg">
                                        <button onclick="setSegmentedValue('${p.clave}', '')" id="btn-seg-rol-${p.clave}" class="${btnBaseClass} ${rolCls}" style="min-width: 50px;" title="Usar Permiso del Rol">Rol</button>
                                        <button onclick="setSegmentedValue('${p.clave}', '1')" id="btn-seg-allow-${p.clave}" class="${btnBaseClass} ${allowCls}" style="min-width: 65px;" title="Forzar Concedido">Conceder</button>
                                        <button onclick="setSegmentedValue('${p.clave}', '0')" id="btn-seg-deny-${p.clave}" class="${btnBaseClass} ${denyCls}" style="min-width: 60px;" title="Forzar Denegado">Denegar</button>
                                    </div>
                                    <select id="select-${p.clave}" class="permiso-indiv-select hidden" data-clave="${p.clave}">
                                        <option value="" ${p.val === '' ? 'selected' : ''}>Rol</option>
                                        <option value="1" ${p.val === '1' ? 'selected' : ''}>Conceder</option>
                                        <option value="0" ${p.val === '0' ? 'selected' : ''}>Denegar</option>
                                    </select>
                                </div>
                            </div>`;
                        };

                        const categorias = {};
                        const permsSinCategoria = [];
                        perms.forEach(p => {
                            if (p.categoria) {
                                if (!categorias[p.categoria]) categorias[p.categoria] = [];
                                categorias[p.categoria].push(p);
                            } else {
                                permsSinCategoria.push(p);
                            }
                        });

                        htmlPermisos += `
                            <div class="mb-4">
                                ${subNombre !== 'General' ? `<h4 class="text-[11px] font-bold text-slate-400 dark:text-gray-500 uppercase tracking-widest px-2 mb-2 flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-gray-600"></span>${escapeHtml(subNombre)}</h4>` : ''}
                                ${permsSinCategoria.map(renderRow).join('')}
                                ${Object.entries(categorias).map(([catNombre, cPerms]) => `
                                    <div class="ml-2 pl-3 border-l-2 border-slate-100 dark:border-gray-800 my-3">
                                        <h5 class="text-[10px] font-bold text-slate-400 dark:text-gray-500 uppercase mb-2 ml-1 flex items-center gap-1.5"><span class="iconify text-lg" data-icon="mdi:folder-outline"></span>${escapeHtml(catNombre)}</h5>
                                        ${cPerms.map(renderRow).join('')}
                                    </div>
                                `).join('')}
                            </div>
                        `;
                    }

                    return `
                        <div class="mb-4 bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-2xl overflow-hidden shadow-sm">
                            <button type="button" onclick="const content = this.nextElementSibling; const icon = this.querySelector('.chevron-icon'); content.classList.toggle('hidden'); icon.style.transform = content.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';" class="w-full flex items-center justify-between p-4 bg-slate-50 dark:bg-gray-800/30 hover:bg-slate-100 dark:hover:bg-gray-800/50 transition-colors focus:outline-none">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                                        <span class="iconify" data-icon="${g.icon}"></span>
                                    </div>
                                    <span class="font-bold text-sm text-slate-800 dark:text-gray-200">${escapeHtml(g.nombre)}</span>
                                </div>
                                <span class="iconify chevron-icon text-slate-400 transition-transform duration-300" data-icon="mdi:chevron-down" style="transform: rotate(180deg)"></span>
                            </button>
                            <div class="p-3">
                                ${htmlPermisos}
                            </div>
                        </div>
                    `;
                }).join('');

            } catch (error) {
                console.error('Error al cargar permisos del usuario', error);
                container.innerHTML = '<div class="p-4 text-center text-sm text-red-500">Error al cargar permisos</div>';
            }
        };

        window.setSegmentedValue = function(clave, val) {
            const select = document.getElementById(`select-${clave}`);
            if (!select) return;
            select.value = val;
            
            // Actualizar botones visuales
            const btnRol = document.getElementById(`btn-seg-rol-${clave}`);
            const btnAllow = document.getElementById(`btn-seg-allow-${clave}`);
            const btnDeny = document.getElementById(`btn-seg-deny-${clave}`);
            
            const btnBaseClass = "px-2 py-1 text-[10px] font-bold uppercase transition-all duration-200 flex items-center justify-center border-y border-r first:border-l first:rounded-l-lg last:rounded-r-lg border-gray-300 dark:border-gray-600 focus:outline-none";
            
            btnRol.className = btnBaseClass + " " + (val === '' ? 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white shadow-inner' : 'bg-white dark:bg-gray-800 text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-700');
            btnAllow.className = btnBaseClass + " " + (val === '1' ? 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-400 border-emerald-300 dark:border-emerald-700 shadow-inner' : 'bg-white dark:bg-gray-800 text-gray-500 hover:bg-emerald-50 dark:hover:bg-emerald-900/20');
            btnDeny.className = btnBaseClass + " " + (val === '0' ? 'bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-400 border-red-300 dark:border-red-700 shadow-inner' : 'bg-white dark:bg-gray-800 text-gray-500 hover:bg-red-50 dark:hover:bg-red-900/20');
            
            actualizarVisualFilaPermiso(select);
        };

        window.cerrarModalPermisosIndividuales = function() {
            const card = document.getElementById('permisosIndivCard');
            card.classList.remove('scale-100', 'opacity-100');
            setTimeout(() => {
                document.getElementById('permisosIndivModalRoot').style.display = 'none';
                idUsuarioEditandoPermisos = null;
            }, 200);
        };
        
        window.actualizarVisualFilaPermiso = function(selectEl) {
            const val = selectEl.value;
            const fila = selectEl.closest('div[data-rol-tiene]');
            if (!fila) return;
            
            const rolLoTiene = fila.getAttribute('data-rol-tiene') === 'true';
            let estadoFinal = rolLoTiene;
            if (val !== '') estadoFinal = (val === '1');
            
            // Colores
            let colorFondo = 'border-slate-150 dark:border-gray-700 bg-slate-50/50 dark:bg-gray-900/30';
            let colorTitulo = 'text-slate-800 dark:text-gray-300';
            let colorIcono = 'text-gray-400';
            let colorFinal = 'text-gray-500';
            let bgIcono = 'bg-slate-200 dark:bg-gray-700/50';
            
            if (estadoFinal) {
                if (val === '1') {
                    colorFondo = 'border-green-200 dark:border-green-800 bg-green-50/50 dark:bg-green-900/20';
                    colorTitulo = 'text-green-800 dark:text-green-200';
                    colorIcono = 'text-green-500';
                    colorFinal = 'text-green-600';
                    bgIcono = 'bg-green-100 dark:bg-green-900/30';
                } else {
                    colorFondo = 'border-purple-200 dark:border-purple-800 bg-purple-50/50 dark:bg-purple-900/20';
                    colorTitulo = 'text-purple-800 dark:text-purple-200';
                    colorIcono = 'text-purple-500';
                    colorFinal = 'text-purple-600';
                    bgIcono = 'bg-purple-100 dark:bg-purple-900/30';
                }
            } else {
                if (val === '0') {
                    colorFondo = 'border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/20';
                    colorTitulo = 'text-red-800 dark:text-red-200';
                    colorIcono = 'text-red-500';
                    colorFinal = 'text-red-600';
                    bgIcono = 'bg-red-100 dark:bg-red-900/30';
                }
            }
            
            fila.className = `flex flex-col lg:flex-row lg:items-center justify-between py-3 px-4 mx-1 my-2 rounded-xl border ${colorFondo} transition-colors`;
            
            const titleLabel = fila.querySelector('.title-label');
            if (titleLabel) titleLabel.className = `text-[13px] font-semibold title-label ${colorTitulo}`;
            
            const statusLabel = fila.querySelector('.status-label');
            if (statusLabel) {
                statusLabel.className = `text-[10px] font-bold tracking-wider status-label ${colorFinal} mt-0.5`;
                statusLabel.textContent = `Final: ${estadoFinal ? 'ACCESO CONCEDIDO' : 'ACCESO DENEGADO'}`;
            }

            const iconContainer = fila.querySelector('.icon-container');
            if (iconContainer) {
                iconContainer.className = `w-8 h-8 rounded-full flex items-center justify-center icon-container ${colorIcono} ${bgIcono}`;
            }
        };
"""

# We need to replace everything from "window.abrirModalPermisosIndividuales = async function(idUsuario, nombre, idRol) {"
# up to the end of "window.actualizarVisualFilaPermiso = function(selectEl) { ... };"

pattern = re.compile(r'window\.abrirModalPermisosIndividuales = async function\(idUsuario, nombre, idRol\) \{.*?window\.actualizarVisualFilaPermiso = function\(selectEl\) \{.*?^\s*\};\n', re.DOTALL | re.MULTILINE)

if pattern.search(content):
    content = pattern.sub(new_code, content)
    with open('Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replace successful")
else:
    print("Regex match failed")

