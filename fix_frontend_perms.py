import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ajustes Globales (configGenerales:editar)
# At the end of cargarConfiguraciones(), after idConfigs.forEach
cfg_old = """                });
            } catch (error) {
                console.error('Error cargando configuraciones:', error);
            }
        }"""
cfg_new = """                });

                // --- PROTECCION DE PERMISOS (Ajustes Globales) ---
                if (window.Permisos && !window.Permisos.tienePermiso('configGenerales:editar')) {
                    document.querySelectorAll('#configPanel-general input, #configPanel-general select').forEach(el => {
                        el.disabled = true;
                        el.classList.add('opacity-70', 'cursor-not-allowed');
                    });
                    const btnGuardar = document.querySelector('#configPanel-general button[onclick="guardarConfiguraciones()"]');
                    if (btnGuardar) btnGuardar.style.display = 'none';
                }
            } catch (error) {
                console.error('Error cargando configuraciones:', error);
            }
        }"""
content = content.replace(cfg_old, cfg_new)

# 2. Modalidades (modalidades:crear, modalidades:editar, modalidades:eliminar)
mod_old = """                tbody.innerHTML = modalidades.map(mod => `
                    <tr class="border-b border-gray-150 dark:border-gray-800 hover:bg-gray-50/50 dark:hover:bg-gray-800/30 transition-colors">"""
mod_new = """                
                const puedeEditar = window.Permisos ? window.Permisos.tienePermiso('modalidades:editar') : false;
                const puedeEliminar = window.Permisos ? window.Permisos.tienePermiso('modalidades:eliminar') : false;
                const attrDisabled = puedeEditar ? '' : 'disabled';
                const classDisabled = puedeEditar ? '' : 'opacity-70 cursor-not-allowed';
                
                tbody.innerHTML = modalidades.map(mod => `
                    <tr class="border-b border-gray-150 dark:border-gray-800 hover:bg-gray-50/50 dark:hover:bg-gray-800/30 transition-colors">"""

content = content.replace(mod_old, mod_new)

# Inside map for modalidades (inputs)
mod_in_old = """<input type="text" value="${mod.nombre}" data-id="${mod.id_modalidad}"
                                class="mod-nombre px-3 py-2 rounded-xl border border-gray-250 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 w-full transition-all duration-200">"""
mod_in_new = """<input type="text" value="${mod.nombre}" data-id="${mod.id_modalidad}" ${attrDisabled}
                                class="mod-nombre px-3 py-2 rounded-xl border border-gray-250 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 w-full transition-all duration-200 ${classDisabled}">"""
content = content.replace(mod_in_old, mod_in_new)

mod_check_old = """<input type="checkbox" class="mod-activo sr-only" data-id="${mod.id_modalidad}" ${mod.activo ? 'checked' : ''}>"""
mod_check_new = """<input type="checkbox" class="mod-activo sr-only" data-id="${mod.id_modalidad}" ${mod.activo ? 'checked' : ''} ${attrDisabled}>"""
content = content.replace(mod_check_old, mod_check_new)

# Hide modal toggle if can't edit
mod_toggle_old = """<div class="w-11 h-6 bg-gray-300 dark:bg-gray-750 rounded-full transition-colors duration-300"></div>"""
mod_toggle_new = """<div class="w-11 h-6 bg-gray-300 dark:bg-gray-750 rounded-full transition-colors duration-300 ${classDisabled}"></div>"""
content = content.replace(mod_toggle_old, mod_toggle_new)

# Hide save/delete buttons conditionally for modalidades
mod_btn_old = """<td class="py-4 px-6 text-right">
                            <div class="flex items-center justify-end gap-2">
                                <button onclick="actualizarModalidad(${mod.id_modalidad})"
                                    class="p-2 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/30 rounded-lg transition-colors tooltip" data-tip="Guardar Cambios">
                                    <span class="iconify text-xl" data-icon="mdi:content-save"></span>
                                </button>
                                <button onclick="confirmarEliminarModalidad(${mod.id_modalidad}, '${mod.nombre}')"
                                    class="p-2 text-red-500 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/30 rounded-lg transition-colors tooltip" data-tip="Eliminar">
                                    <span class="iconify text-xl" data-icon="mdi:delete-outline"></span>
                                </button>
                            </div>
                        </td>"""
mod_btn_new = """<td class="py-4 px-6 text-right">
                            <div class="flex items-center justify-end gap-2">
                                ${puedeEditar ? `
                                <button onclick="actualizarModalidad(${mod.id_modalidad})"
                                    class="p-2 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/30 rounded-lg transition-colors tooltip" data-tip="Guardar Cambios">
                                    <span class="iconify text-xl" data-icon="mdi:content-save"></span>
                                </button>
                                ` : ''}
                                ${puedeEliminar ? `
                                <button onclick="confirmarEliminarModalidad(${mod.id_modalidad}, '${mod.nombre}')"
                                    class="p-2 text-red-500 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/30 rounded-lg transition-colors tooltip" data-tip="Eliminar">
                                    <span class="iconify text-xl" data-icon="mdi:delete-outline"></span>
                                </button>
                                ` : ''}
                            </div>
                        </td>"""
content = content.replace(mod_btn_old, mod_btn_new)

# Hide "Agregar Modalidad" button
add_mod_old = """<button onclick="abrirModalModalidad()" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 active:scale-98 text-white font-bold rounded-xl shadow-md shadow-blue-500/20 transition-all flex items-center gap-2">
                            <span class="iconify text-xl" data-icon="mdi:plus-circle"></span>
                            <span>Agregar Modalidad</span>
                        </button>"""
add_mod_new = """<button id="btnAgregarModalidad" onclick="abrirModalModalidad()" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 active:scale-98 text-white font-bold rounded-xl shadow-md shadow-blue-500/20 transition-all flex items-center gap-2">
                            <span class="iconify text-xl" data-icon="mdi:plus-circle"></span>
                            <span>Agregar Modalidad</span>
                        </button>"""
content = content.replace(add_mod_old, add_mod_new)

add_mod_logic_old = """                if (!modalidades || modalidades.length === 0) {"""
add_mod_logic_new = """                
                const btnAgregar = document.getElementById('btnAgregarModalidad');
                if (btnAgregar && window.Permisos && !window.Permisos.tienePermiso('modalidades:crear')) {
                    btnAgregar.style.display = 'none';
                }

                if (!modalidades || modalidades.length === 0) {"""
content = content.replace(add_mod_logic_old, add_mod_logic_new)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied UI protections for Generales and Modalidades")
