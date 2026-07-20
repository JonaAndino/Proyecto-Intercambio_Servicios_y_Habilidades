import re

with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the broken block from `window.abrirModalPermisosIndividuales` down to `window.cerrarModalPermisos`
broken_pattern = re.compile(r'window\.abrirModalPermisosIndividuales = async function\(idUsuario, nombre, idRol\) \{.*?window\.cerrarModalPermisos = function', re.DOTALL)

clean_indiv_and_roles = """window.abrirModalPermisosIndividuales = async function(idUsuario, nombre, idRol) {
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

                    const rolLoTiene = rol.permisos && rol.permisos.includes(p.clave);
                    const exc = excepciones.find(e => e.permiso_clave === p.clave);
                    const val = exc ? (exc.concedido ? '1' : '0') : '';

                    if (!grupos[metadata.grupo]) {
                        grupos[metadata.grupo] = {
                            nombre: metadata.grupo,
                            icon: getIconoGrupo(metadata.grupo),
                            permisos: []
                        };
                    }

                    if (metadata.isCrudBase) {
                        ['ver', 'crear', 'editar', 'eliminar'].forEach(accion => {
                            const subClave = `${p.clave}:${accion}`;
                            const subRolLoTiene = rol.permisos && rol.permisos.includes(subClave);
                            const subExc = excepciones.find(e => e.permiso_clave === subClave);
                            const subVal = subExc ? (subExc.concedido ? '1' : '0') : '';
                            const nombreAccion = accion.charAt(0).toUpperCase() + accion.slice(1);

                            grupos[metadata.grupo].permisos.push({
                                clave: subClave,
                                nombre: `${nombreAccion} ${metadata.nombre}`,
                                subgrupo: metadata.subgrupo || 'General',
                                categoria: metadata.nombre,
                                tipo: accion,
                                icon: metadata.icon,
                                rolLoTiene: subRolLoTiene,
                                val: subVal
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
                                    colorFondo = 'border-blue-200 dark:border-blue-800 bg-blue-50/50 dark:bg-blue-900/20';
                                    colorTitulo = 'text-blue-800 dark:text-blue-200';
                                    colorIcono = 'text-blue-500';
                                    colorFinal = 'text-blue-600';
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

                        const renderCategoria = (catNombre, catPerms) => `
                            <div class="group/cat bg-white dark:bg-gray-900 rounded-xl my-2 mx-1 overflow-hidden flex flex-col is-closed border border-slate-100 dark:border-gray-800">
                                <div onclick="event.stopPropagation(); this.parentElement.classList.toggle('is-closed'); this.parentElement.classList.toggle('is-open');" class="flex items-center justify-between p-3 cursor-pointer select-none hover:bg-slate-50 dark:hover:bg-gray-800/50 group-[.is-open]/cat:bg-slate-100 dark:group-[.is-open]/cat:bg-gray-800 transition-colors">
                                    <div class="flex items-center gap-3">
                                        <span class="text-[13px] font-bold text-slate-700 dark:text-gray-200">${catNombre}</span>
                                        <div class="dot-indicator w-2 h-2 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)] ${catPerms.some(p => (p.val !== '' ? p.val === '1' : p.rolLoTiene)) ? '' : 'hidden'}"></div>
                                    </div>
                                    <span class="iconify text-lg text-slate-400 group-[.is-open]/cat:rotate-180 transition-transform duration-300" data-icon="mdi:chevron-down"></span>
                                </div>
                                <div class="grid transition-[grid-template-rows] duration-300 ease-in-out grid-rows-[0fr] group-[.is-open]/cat:grid-rows-[1fr]">
                                    <div class="overflow-hidden">
                                        <div class="px-1 pb-2 bg-white dark:bg-gray-900 border-t border-slate-100 dark:border-gray-800">
                                            ${catPerms.map(renderRow).join('')}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;

                        let subContent = '';
                        if (permsSinCategoria.length > 0) {
                            subContent += permsSinCategoria.map(renderRow).join('');
                        }
                        for (const [catNombre, catPerms] of Object.entries(categorias)) {
                            subContent += renderCategoria(catNombre, catPerms);
                        }

                        if (subNombre === 'General') {
                            htmlPermisos += subContent;
                        } else {
                            htmlPermisos += `
                                <div class="group/sub bg-slate-50 dark:bg-gray-800/50 rounded-xl my-2 mx-1 overflow-hidden flex flex-col is-closed border border-slate-200 dark:border-gray-700">
                                    <div onclick="this.parentElement.classList.toggle('is-closed'); this.parentElement.classList.toggle('is-open');" class="flex items-center justify-between p-3 cursor-pointer select-none hover:bg-slate-100 dark:hover:bg-gray-800 group-[.is-open]/sub:bg-slate-100 dark:group-[.is-open]/sub:bg-gray-700 transition-colors">
                                        <div class="flex items-center gap-3">
                                            <span class="text-[14px] font-bold text-slate-800 dark:text-gray-100">${subNombre}</span>
                                            <div class="dot-indicator w-2 h-2 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)] ${perms.some(p => (p.val !== '' ? p.val === '1' : p.rolLoTiene)) ? '' : 'hidden'}"></div>
                                        </div>
                                        <span class="iconify text-xl text-slate-500 group-[.is-open]/sub:rotate-180 transition-transform duration-300" data-icon="mdi:chevron-down"></span>
                                    </div>
                                    <div class="grid transition-[grid-template-rows] duration-300 ease-in-out grid-rows-[0fr] group-[.is-open]/sub:grid-rows-[1fr]">
                                        <div class="overflow-hidden">
                                            <div class="p-2 bg-slate-100/50 dark:bg-gray-900/30">
                                                ${subContent}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                        }
                    }

                    return `
                        <div class="grupo-permisos-card mb-4 bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-2xl overflow-hidden shadow-sm group is-open" data-grupo="${escapeHtml(g.nombre)}">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-white dark:bg-gray-900 group-[.is-open]:bg-slate-100 dark:group-[.is-open]:bg-gray-800/80 hover:bg-slate-50 dark:hover:bg-gray-800/50 transition-colors border-b border-transparent group-[.is-open]:border-slate-200 dark:group-[.is-open]:border-gray-700 cursor-pointer select-none" onclick="this.parentElement.classList.toggle('is-open');">
                                <div class="flex items-center gap-3 mb-3 sm:mb-0">
                                    <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                                        <span class="iconify" data-icon="${g.icon}"></span>
                                    </div>
                                    <span class="font-bold text-sm text-slate-800 dark:text-gray-200">${escapeHtml(g.nombre)}</span>
                                </div>
                                <span class="iconify chevron-icon text-slate-400 group-[.is-open]:rotate-180 transition-transform duration-300 ml-2" data-icon="mdi:chevron-down" onclick="this.closest('.grupo-permisos-card').classList.toggle('is-open')"></span>
                            </div>
                            <div class="grid transition-[grid-template-rows] duration-300 ease-in-out grid-rows-[0fr] group-[.is-open]:grid-rows-[1fr]">
                                <div class="overflow-hidden">
                                    <div class="grupo-permisos-body p-3">
                                        ${htmlPermisos}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (err) {
                console.error('[abrirModalPermisosIndividuales]', err);
                container.innerHTML = '<div class="p-4 text-center text-sm text-red-500">Error al cargar los permisos del usuario.</div>';
            }
        };

        window.cerrarModalPermisos = function"""

content = broken_pattern.sub(clean_indiv_and_roles, content)

with open('Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax in Reportes.html")
