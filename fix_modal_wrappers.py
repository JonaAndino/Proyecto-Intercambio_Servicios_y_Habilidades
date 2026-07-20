import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace permisosModalRoot wrapper
roles_pattern = r'<div id="permisosModalRoot".*?</script>'
roles_match = re.search(roles_pattern, content, re.DOTALL)

# But wait, it's safer to just replace the specific divs.
# For permisosModalRoot:
target_roles = """    <div id="permisosModalRoot" style="display:none;" class="fixed inset-0 z-[9999] flex items-center justify-center p-4 overflow-y-auto">
        <div id="permisosBackdrop" class="fixed inset-0 bg-transparent" onclick="cerrarModalEditarPermisos()"></div>
        <div id="permisosCard" class="relative bg-white dark:bg-gray-800 rounded-3xl w-full max-w-5xl shadow-2xl border border-slate-100 dark:border-gray-700 flex flex-col overflow-visible mt-8 z-10">
            <div class="h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-t-3xl relative overflow-visible flex items-end justify-center pb-2">
                <button onclick="cerrarModalEditarPermisos()" class="absolute top-2 right-4 text-white hover:scale-110 transition-transform z-20 cursor-pointer" aria-label="Cerrar modal">
                    <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
                <div class="absolute -top-6 inset-x-0 flex justify-center items-end pointer-events-none">
                    <div class="w-12 h-12 bg-indigo-600 rounded-2xl shadow-lg flex items-center justify-center border-2 border-white transform translate-y-2">
                        <span class="iconify text-2xl text-white" data-icon="mdi:shield-key-outline"></span>
                    </div>
                </div>
            </div>
            <div class="p-4 md:p-5 space-y-3">
                <div class="text-center">
                    <h3 id="permisosRoleNombre" class="text-2xl font-black text-slate-800 dark:text-white tracking-tight">Permisos</h3>
                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">Habilita o deshabilita los accesos y privilegios de este rol.</p>
                </div>"""

replacement_roles = """    <div id="permisosModalRoot" style="display:none;" class="fixed inset-0 z-[9999] flex items-center justify-center p-4 overflow-y-auto">
        <div id="permisosBackdrop" class="fixed inset-0 bg-transparent transition-opacity" onclick="cerrarModalEditarPermisos()"></div>
        <div id="permisosCard" class="relative bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] shadow-[0_8px_30px_rgb(0,0,0,0.12)] dark:shadow-[0_8px_30px_rgb(0,0,0,0.5)] border border-slate-100 dark:border-gray-800 flex flex-col overflow-visible z-10 transition-all">
            <div class="flex items-center justify-between p-6 pb-4 border-b border-transparent shrink-0">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-indigo-50 dark:bg-indigo-900/30 rounded-xl flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                        <span class="iconify text-xl" data-icon="mdi:shield-key-outline"></span>
                    </div>
                    <div>
                        <h3 id="permisosRoleNombre" class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">Permisos de Rol</h3>
                        <p class="text-[13px] text-slate-500 dark:text-gray-400 mt-0.5 font-medium">Habilita o deshabilita accesos para todos los usuarios con este rol.</p>
                    </div>
                </div>
                <button onclick="cerrarModalEditarPermisos()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 hover:bg-slate-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-slate-500 dark:text-gray-400 transition-colors cursor-pointer" aria-label="Cerrar modal">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
            </div>
            <div class="p-6 pt-0 space-y-4 flex-1 flex flex-col min-h-0">"""

content = content.replace(target_roles, replacement_roles)

target_roles_footer = """            <div class="p-4 md:p-5 bg-slate-50 dark:bg-gray-900/50 rounded-b-3xl border-t border-slate-100 dark:border-gray-800 flex flex-col-reverse sm:flex-row gap-3">
                <button onclick="cerrarModalEditarPermisos()" type="button" class="flex-1 px-5 py-3 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:bg-slate-100 dark:hover:bg-gray-700 text-slate-700 dark:text-gray-300 text-sm font-bold transition-all cursor-pointer">Cancelar</button>
                <button onclick="guardarPermisosRol()" type="button" class="flex-1 px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-sm font-bold shadow-lg shadow-blue-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer">
                    <span>Guardar Permisos</span>
                </button>
            </div>"""

replacement_roles_footer = """            <div class="p-5 bg-slate-50/80 dark:bg-gray-800/80 rounded-b-3xl border-t border-slate-100 dark:border-gray-800 flex justify-end gap-3 backdrop-blur-md shrink-0">
                <button type="button" onclick="cerrarModalEditarPermisos()" class="px-5 py-2.5 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:bg-slate-50 dark:hover:bg-gray-800 text-slate-700 dark:text-gray-300 text-sm font-semibold transition-all cursor-pointer">Cancelar</button>
                <button type="button" onclick="guardarPermisosRol()" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold shadow-md shadow-blue-500/20 transition-all flex items-center gap-2 cursor-pointer">
                    Guardar Permisos
                </button>
            </div>"""

content = content.replace(target_roles_footer, replacement_roles_footer)


# For permisosIndivModalRoot:
target_indiv = """    <div id="permisosIndivModalRoot" style="display:none;" class="fixed inset-0 z-[9999] flex items-center justify-center p-4 overflow-y-auto">
        <div id="permisosIndivBackdrop" class="fixed inset-0 bg-transparent" onclick="cerrarModalPermisosIndividuales()"></div>
        <div id="permisosIndivCard" class="relative bg-white dark:bg-gray-800 rounded-3xl w-full max-w-5xl shadow-2xl border border-slate-100 dark:border-gray-700 flex flex-col overflow-visible mt-8 z-10">
            <div class="h-12 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-t-3xl relative overflow-visible flex items-end justify-center pb-2">
                <button onclick="cerrarModalPermisosIndividuales()" class="absolute top-2 right-4 text-white hover:scale-110 transition-transform z-20 cursor-pointer" aria-label="Cerrar modal">
                    <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
                <div class="absolute -top-6 inset-x-0 flex justify-center items-end pointer-events-none">
                    <div class="w-12 h-12 bg-indigo-600 rounded-2xl shadow-lg flex items-center justify-center border-2 border-white transform translate-y-2">
                        <span class="iconify text-2xl text-white" data-icon="mdi:key"></span>
                    </div>
                </div>
            </div>
            <div class="p-4 md:p-5 space-y-3">
                <div class="text-center">
                    <h3 id="permisosIndivNombre" class="text-2xl font-black text-slate-800 dark:text-white tracking-tight">Permisos de Usuario</h3>
                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">Habilita (concedido) o deshabilita (denegado) accesos individualmente para este usuario. Si dejas todo en gris (neutro), se usará su Rol.</p>
                </div>"""

replacement_indiv = """    <div id="permisosIndivModalRoot" style="display:none;" class="fixed inset-0 z-[9999] flex items-center justify-center p-4 overflow-y-auto">
        <div id="permisosIndivBackdrop" class="fixed inset-0 bg-transparent transition-opacity" onclick="cerrarModalPermisosIndividuales()"></div>
        <div id="permisosIndivCard" class="relative bg-white dark:bg-gray-900 rounded-3xl w-full max-w-4xl max-h-[90vh] shadow-[0_8px_30px_rgb(0,0,0,0.12)] dark:shadow-[0_8px_30px_rgb(0,0,0,0.5)] border border-slate-100 dark:border-gray-800 flex flex-col overflow-visible z-10 transition-all">
            <div class="flex items-center justify-between p-6 pb-4 border-b border-transparent shrink-0">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-indigo-50 dark:bg-indigo-900/30 rounded-xl flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                        <span class="iconify text-xl" data-icon="mdi:shield-account"></span>
                    </div>
                    <div>
                        <h3 id="permisosIndivNombre" class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">Permisos de Usuario</h3>
                        <p class="text-[13px] text-slate-500 dark:text-gray-400 mt-0.5 font-medium">Habilita o deshabilita excepciones de accesos individualmente para este usuario.</p>
                    </div>
                </div>
                <button onclick="cerrarModalPermisosIndividuales()" class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 hover:bg-slate-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-slate-500 dark:text-gray-400 transition-colors cursor-pointer" aria-label="Cerrar modal">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
            </div>
            <div class="p-6 pt-0 space-y-4 flex-1 flex flex-col min-h-0">"""

content = content.replace(target_indiv, replacement_indiv)

target_indiv_footer = """            <div class="p-4 md:p-5 bg-slate-50 dark:bg-gray-900/50 rounded-b-3xl border-t border-slate-100 dark:border-gray-800 flex flex-col-reverse sm:flex-row gap-3">
                <button onclick="cerrarModalPermisosIndividuales()" type="button" class="flex-1 px-5 py-3 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:bg-slate-100 dark:hover:bg-gray-700 text-slate-700 dark:text-gray-300 text-sm font-bold transition-all cursor-pointer">Cancelar</button>
                <button onclick="guardarPermisosIndividuales()" type="button" class="flex-1 px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-sm font-bold shadow-lg shadow-blue-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer">
                    <span>Guardar Excepciones</span>
                </button>
            </div>"""

replacement_indiv_footer = """            <div class="p-5 bg-slate-50/80 dark:bg-gray-800/80 rounded-b-3xl border-t border-slate-100 dark:border-gray-800 flex justify-end gap-3 backdrop-blur-md shrink-0">
                <button type="button" onclick="cerrarModalPermisosIndividuales()" class="px-5 py-2.5 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:bg-slate-50 dark:hover:bg-gray-800 text-slate-700 dark:text-gray-300 text-sm font-semibold transition-all cursor-pointer">Cancelar</button>
                <button type="button" onclick="guardarPermisosIndividuales()" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold shadow-md shadow-blue-500/20 transition-all flex items-center gap-2 cursor-pointer">
                    Guardar Excepciones
                </button>
            </div>"""

content = content.replace(target_indiv_footer, replacement_indiv_footer)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modal wrappers replaced successfully!")
