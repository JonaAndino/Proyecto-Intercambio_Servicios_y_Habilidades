import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_function(content, func_name, new_func_code):
    pattern = r'(window\.' + func_name + r'\s*=\s*(?:async\s*)?function\s*\([^)]*\)\s*\{|^\s*async function ' + func_name + r'\s*\([^)]*\)\s*\{)(.*?)(?=\n        window\.[a-zA-Z0-9_]+\s*=\s*(?:async\s*)?function|\n        (?:async\s*)?function\s+[a-zA-Z0-9_]+|\n    </script>)'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if not match:
        print(f"Could not find {func_name}")
        return content
    return content[:match.start()] + new_func_code + content[match.end():]

new_code = """async function cargarYRenderizarRolesConfig() {
            const tbody = document.getElementById('rolesTbody');
            if (!tbody) return;
            tbody.innerHTML = `<tr><td colspan="4" class="py-10 text-center text-gray-400 italic">Cargando roles y accesos desde el servidor...</td></tr>`;

            try {
                if (todosLosPermisosDisponibles.length === 0) {
                    const resPerm = await fetch(PERMISOS_API);
                    const jsonPerm = await resPerm.json();
                    if (resPerm.ok && jsonPerm.success) {
                        todosLosPermisosDisponibles = jsonPerm.data;
                    }
                }

                const res = await fetch(ROLES_API);
                const json = await res.json();
                if (!res.ok || !json.success) throw new Error(json.error || 'Error al obtener roles');
                
                todosLosRolesCargados = json.data;
                
                // Sincronizar roles con la tabla del Directorio general
                if (typeof _rolesDirectorio !== 'undefined') {
                    _rolesDirectorio = todosLosRolesCargados.map(r => ({ id_rol: r.id_rol, nombre_rol: r.nombre_rol }));
                    if (typeof renderizarTablaTecnicos === 'function') {
                        renderizarTablaTecnicos();
                    }
                }

                tbody.innerHTML = todosLosRolesCargados.map((rol) => {
                    const countPermisos = rol.permisos ? rol.permisos.length : 0;
                    
                    const btnEliminar = rol.es_default
                        ? `<button disabled class="p-2 rounded-xl bg-slate-50 text-slate-300 cursor-not-allowed">
                                <span class="iconify text-[18px]" data-icon="mdi:trash-can-outline"></span>
                           </button>`
                        : `<button onclick="eliminarRol(${rol.id_rol})" class="p-2 rounded-xl bg-red-50 hover:bg-red-100 text-red-500 transition-all cursor-pointer" title="Eliminar">
                                <span class="iconify text-[18px]" data-icon="mdi:trash-can-outline"></span>
                           </button>`;

                    return `
                        <tr class="hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0">
                            <td class="py-4 px-6">
                                <input type="text" value="${escapeHtml(rol.nombre_rol)}" onchange="renombrarRol(${rol.id_rol}, this.value)"
                                    class="px-5 py-2.5 rounded-full border border-slate-200 bg-white text-slate-800 text-[14.5px] font-bold focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 w-[80%] transition-all">
                            </td>
                            <td class="py-4 px-6">
                                <input type="text" value="${escapeHtml(rol.descripcion_rol || '')}" onchange="actualizarDescripcionRol(${rol.id_rol}, this.value)"
                                    class="px-5 py-2.5 rounded-full border border-slate-200 bg-white text-slate-600 text-[13px] focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 w-[95%] transition-all">
                            </td>
                            <td class="py-4 px-6 text-center">
                                <div class="inline-flex items-center gap-3 px-5 py-1.5 rounded-full border border-blue-100/50 bg-blue-50 text-blue-600 justify-center min-w-[110px]">
                                    <span class="iconify text-[18px]" data-icon="mdi:shield-check-outline"></span>
                                    <div class="flex flex-col items-center leading-none mt-0.5">
                                        <span class="text-[13px] font-extrabold">${countPermisos}</span>
                                        <span class="text-[10.5px] font-bold tracking-wide mt-[2px]">Permisos</span>
                                    </div>
                                </div>
                            </td>
                            <td class="py-4 px-6">
                                <div class="flex items-center justify-center gap-3">
                                    <button onclick="abrirModalEditarPermisos(${rol.id_rol})" class="px-5 py-2 rounded-full bg-indigo-50 hover:bg-indigo-100 text-indigo-600 text-[12.5px] font-extrabold transition-all flex items-center gap-2 cursor-pointer border border-indigo-100/50">
                                        <span class="iconify text-[17px]" data-icon="mdi:shield-key-outline"></span>
                                        Permisos
                                    </button>
                                    ${btnEliminar}
                                </div>
                            </td>
                        </tr>
                    `;
                }).join('');
            } catch (error) {
                console.error('Error cargando roles:', error);
                tbody.innerHTML = `<tr><td colspan="4" class="py-10 text-center text-red-500">Error al cargar los roles. Verifica tu conexión.</td></tr>`;
            }
        }
"""

content = replace_function(content, "cargarYRenderizarRolesConfig", new_code)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated table successfully!")
