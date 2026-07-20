import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = """        window.abrirModalEditarPermisos = function(idRol) {
            idRolEditandoPermisos = idRol;
            const rol = todosLosRolesCargados.find(r => r.id_rol === idRol);
            if (!rol) return;

            permisosOriginalesRol = [...(rol.permisos || [])];

            const nameElement = document.getElementById('permisosRoleNombre');
            if (nameElement) {
                nameElement.textContent = `Permisos para "${rol.nombre_rol}"`;
            }
            
            const subtitle = document.querySelector('#permisosModalRoot p.text-slate-500');
            if (subtitle) {
                subtitle.textContent = "Marca o desmarca los accesos concedidos a este Rol.";
            }

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
            
            const getNombreAmigable = (clave, defaultName) => {
                const map = {
                    'GESTIONAR_CONFIGURACION': 'Acceso al Panel de Configuraciones',
                    'VER_HISTORIAL_PERSONAL': 'Ver listado de postulaciones globales',
                    'CREAR_CUENTAS': 'Crear y enrolar nuevas cuentas de usuario',
                    'ASIGNAR_ROLES_PERMISOS': 'Asignar roles y permisos a usuarios',
                    'ACEPTAR_INTERCAMBIOS': 'Solicitar y concretar intercambios de habilidades',
                    'VER_DIRECTORIO': 'Ver listado y tabla del directorio general',
                    'EDITAR_USUARIOS': 'Editar perfiles y datos de usuarios',
                    'VER_SOLICITUDES_VERIFICACION': 'Cola de validadores para identidad y certificaciones'
                };
                return map[clave] || defaultName;
            };

            const container = document.getElementById('permisosCheckboxesContainer');
            if (container) {
                const generarHTMLPermiso = (p) => {
                    const activo = rol.permisos && rol.permisos.includes(p.clave);
                    const iconoSVG = getIconoOpcion(p.clave);
                    const nombreAmigable = getNombreAmigable(p.clave, p.nombre);
                    return `
                        <label class="flex items-center gap-3 p-4 rounded-xl border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-blue-500 dark:hover:border-blue-500 hover:shadow-md transition-all cursor-pointer">
                            <input type="checkbox" value="${p.clave}" ${activo ? 'checked' : ''} onchange="actualizarContadoresPermisos()"
                                class="permiso-checkbox w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer">
                            <div class="flex items-center gap-3">
                                <span class="iconify text-2xl text-slate-500 dark:text-gray-400" data-icon="${iconoSVG}"></span>
                                <div class="flex flex-col">
                                    <span class="text-sm font-bold text-slate-800 dark:text-gray-100">${escapeHtml(nombreAmigable)}</span>
                                    <span class="text-[10px] font-mono text-slate-400 dark:text-gray-500 mt-0.5">${escapeHtml(p.clave)}</span>
                                </div>
                            </div>
                        </label>
                    `;
                };

                const htmlUnico = `<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-2">${todosLosPermisosDisponibles.map(generarHTMLPermiso).join('')}</div>`;

                container.innerHTML = htmlUnico;
                actualizarContadoresPermisos();
            }

            const root = document.getElementById('permisosModalRoot');
            const backdrop = document.getElementById('permisosBackdrop');
            const card = document.getElementById('permisosCard');
            if (root) {
                root.style.display = 'flex';
                backdrop.classList.remove('animate-backdrop-out');
                backdrop.classList.add('animate-backdrop-in');
                card.classList.remove('animate-modal-out');
                card.classList.add('animate-modal-in');
            }
        };"""

pattern = re.compile(r'window\.abrirModalEditarPermisos = function\(idRol\) \{.*?root\.style\.display = \'flex\';\s*backdrop.*?animate-modal-in\'\);\s*\}\s*\};', re.DOTALL)

# Since the pattern didn't match, let's use replace_file_content or a simpler string split.
start_idx = content.find('window.abrirModalEditarPermisos = function(idRol) {')
end_idx = content.find('window.cerrarModalPermisos = function() {')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_logic + '\n\n        ' + content[end_idx:]
    with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced modal with screenshot version!")
else:
    print("Could not find start or end index!")
