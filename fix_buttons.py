import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace <button without type="button" inside my modals
content = content.replace('<button onclick="cerrarModalEditarPermisos()"', '<button type="button" onclick="cerrarModalEditarPermisos()"')
content = content.replace('<button onclick="cerrarModalPermisosIndividuales()"', '<button type="button" onclick="cerrarModalPermisosIndividuales()"')
content = content.replace('<button onclick="seleccionarTodoGlobal', '<button type="button" onclick="seleccionarTodoGlobal')
content = content.replace('<button onclick="seleccionarTodoGrupo', '<button type="button" onclick="seleccionarTodoGrupo')
content = content.replace('<button onclick="window.excepcionesCargadas.forEach', '<button type="button" onclick="window.excepcionesCargadas.forEach')

# Also fix the cargarRoles() call to cargarYRenderizarRolesConfig()
content = content.replace('cargarRoles();', 'if(typeof cargarYRenderizarRolesConfig === "function") cargarYRenderizarRolesConfig(); else if(typeof cargarRoles === "function") cargarRoles();')

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Buttons fixed to have type='button' and table refresh fixed!")
