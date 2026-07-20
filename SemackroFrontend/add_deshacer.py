with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add variable and undo function
if 'let permisosOriginalesRol = [];' not in content:
    content = content.replace('let idRolEditandoPermisos = null;', 'let idRolEditandoPermisos = null;\n        let permisosOriginalesRol = [];')

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

# 2. Add Deshacer button in the HTML (Top bar of roles modal)
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

# 3. Save initial permissions when modal opens
if 'permisosOriginalesRol = [...(rol.permisos || [])];' not in content:
    content = content.replace('const rol = todosLosRolesCargados.find(r => r.id_rol === idRol);\n            if (!rol) return;', 'const rol = todosLosRolesCargados.find(r => r.id_rol === idRol);\n            if (!rol) return;\n\n            permisosOriginalesRol = [...(rol.permisos || [])];')

with open('Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Deshacer button added!")
