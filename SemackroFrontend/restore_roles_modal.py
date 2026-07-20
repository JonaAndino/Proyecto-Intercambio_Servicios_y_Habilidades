import re

with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Store original permissions array variable in JS
if 'let permisosOriginalesRol = [];' not in content:
    content = content.replace('let idRolEditandoPermisos = null;', 'let idRolEditandoPermisos = null;\n        let permisosOriginalesRol = [];')

# 2. Add restablecerPermisosRolOriginales function
undo_func = """
        window.restablecerPermisosRolOriginales = function() {
            const checkboxes = document.querySelectorAll('#permisosCheckboxesContainer .permiso-checkbox');
            checkboxes.forEach(cb => {
                cb.checked = permisosOriginalesRol.includes(cb.value);
            });
            actualizarContadoresPermisos();
            if (typeof Toast !== 'undefined') {
                Toast.info('Cambios deshechos', 'Se han restaurado los permisos originales del rol.');
            }
        };
"""

if 'window.restablecerPermisosRolOriginales' not in content:
    content = content.replace('window.toggleTodosPermisosGlobal = function(checkAll) {', undo_func + '\n        window.toggleTodosPermisosGlobal = function(checkAll) {')

# 3. Add Deshacer button in the top bar of Roles modal
old_top_bar = """<button type="button" onclick="toggleTodosPermisosGlobal(false)" class="px-3 py-1 text-[11px] font-bold text-slate-600 dark:text-gray-300 hover:bg-slate-50 dark:hover:bg-gray-700 rounded-lg transition-all" title="Quitar todos los permisos">
                                Nada
                            </button>
                        </div>"""

new_top_bar = """<button type="button" onclick="toggleTodosPermisosGlobal(false)" class="px-3 py-1 text-[11px] font-bold text-slate-600 dark:text-gray-300 hover:bg-slate-50 dark:hover:bg-gray-700 rounded-lg transition-all" title="Quitar todos los permisos">
                                Nada
                            </button>
                            <div class="w-px h-3 bg-slate-200 dark:bg-gray-700 mx-0.5"></div>
                            <button type="button" onclick="restablecerPermisosRolOriginales()" class="px-3 py-1 text-[11px] font-bold text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all flex items-center gap-1" title="Restaurar selección inicial">
                                <span class="iconify text-sm" data-icon="mdi:undo"></span> Deshacer
                            </button>
                        </div>"""

content = content.replace(old_top_bar, new_top_bar)

# 4. Restore abrirModalEditarPermisos logic to clean original version from git HEAD + save initial permissions
new_modal_logic = """        window.abrirModalEditarPermisos = function(idRol) {
            idRolEditandoPermisos = idRol;
            const rol = todosLosRolesCargados.find(r => r.id_rol === idRol);
            if (!rol) return;

            permisosOriginalesRol = [...(rol.permisos || [])];

            const nameElement = document.getElementById('permisosRoleNombre');
            if (nameElement) {
                nameElement.textContent = `Asignar permisos al rol: ${rol.nombre_rol}`;
            }

            const container = document.getElementById('permisosCheckboxesContainer');
            if (container) {
                const isPermisoAdmin = (clave) => clave === clave.toUpperCase();
                const permisosUsuario = todosLosPermisosDisponibles.filter(p => !isPermisoAdmin(p.clave));
                const permisosAdmin = todosLosPermisosDisponibles.filter(p => isPermisoAdmin(p.clave));

                const generarHTMLPermiso = (p) => {
                    const activo = rol.permisos && rol.permisos.includes(p.clave);
                    const metadata = MAPEO_GRUPOS_PERMISOS[p.clave] || {};
                    const icon = metadata.icon || 'mdi:checkbox-marked-circle-outline';

                    return `
                        <label class="permiso-item-row flex items-center justify-between p-3.5 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-sm transition-all cursor-pointer select-none group/item" data-nombre-permiso="${escapeHtml(p.nombre.toLowerCase())}">
                            <div class="flex items-center gap-3">
                                <div class="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover/item:scale-105 transition-transform">
                                    <span class="iconify text-lg" data-icon="${icon}"></span>
                                </div>
                                <span class="text-xs font-bold text-slate-700 dark:text-gray-200 group-hover/item:text-blue-600 dark:group-hover/item:text-blue-400 transition-colors">${escapeHtml(p.nombre)}</span>
                            </div>
                            <input type="checkbox" value="${p.clave}" ${activo ? 'checked' : ''} onchange="actualizarContadoresPermisos()"
                                class="permiso-checkbox rounded text-blue-600 focus:ring-blue-500/20 w-4.5 h-4.5 cursor-pointer">
                        </label>
                    `;
                };

                const headerUserHTML = permisosUsuario.length > 0 ? `
                    <div class="col-span-1 md:col-span-2 mt-1 mb-2 grupo-permisos-card" data-grupo="Usuario Normal">
                        <div class="flex items-center justify-between border-b border-slate-200 dark:border-gray-700 pb-2">
                            <h4 class="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                                <span class="iconify text-lg text-slate-400" data-icon="mdi:account-group"></span> Permisos de Usuario Normal
                            </h4>
                            <span class="badge-contador-grupo text-[10px] font-bold text-slate-500 font-mono bg-slate-100 dark:bg-gray-800 px-2.5 py-0.5 rounded-full border border-slate-200/50 dark:border-gray-700">0/0</span>
                        </div>
                    </div>
                ` : '';

                const htmlUsuario = permisosUsuario.length > 0 ? `<div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 mb-6">${permisosUsuario.map(generarHTMLPermiso).join('')}</div>` : '';

                const headerAdminHTML = permisosAdmin.length > 0 ? `
                    <div class="col-span-1 md:col-span-2 mt-4 mb-2 grupo-permisos-card" data-grupo="Administrador">
                        <div class="flex items-center justify-between border-b border-blue-200 dark:border-blue-800/50 pb-2">
                            <h4 class="text-xs font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest flex items-center gap-2">
                                <span class="iconify text-lg text-blue-500" data-icon="mdi:shield-account"></span> Permisos de Administrador
                            </h4>
                            <span class="badge-contador-grupo text-[10px] font-bold text-blue-600 dark:text-blue-400 font-mono bg-blue-50 dark:bg-blue-950/30 px-2.5 py-0.5 rounded-full border border-blue-100 dark:border-blue-900/30">0/0</span>
                        </div>
                    </div>
                ` : '';
                
                const htmlAdmin = permisosAdmin.length > 0 ? `<div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">${permisosAdmin.map(generarHTMLPermiso).join('')}</div>` : '';

                container.innerHTML = headerUserHTML + htmlUsuario + headerAdminHTML + htmlAdmin;
                actualizarContadoresPermisos();
            }

            const root = document.getElementById('permisosModalRoot');
            const backdrop = document.getElementById('permisosBackdrop');
            const card = document.getElementById('permisosCard');
            if (root) {
                root.style.display = 'flex';
                backdrop.className = 'fixed inset-0 bg-transparent transition-opacity animate-backdrop-in';
                card.className = 'relative bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] shadow-2xl border border-slate-100 dark:border-gray-800 flex flex-col overflow-visible mt-8 z-10 animate-modal-in';
            }
        };"""

# Replace window.abrirModalEditarPermisos block
pattern = re.compile(r'window\.abrirModalEditarPermisos = function\(idRol\) \{.*?\};\n', re.DOTALL)
content = pattern.sub(new_modal_logic, content)

with open('Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Roles modal successfully restored to original clean layout + Deshacer button added!")
