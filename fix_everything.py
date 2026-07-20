import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

with open('old_modal.txt', 'r', encoding='utf-8') as f:
    old_modal_content = f.read().strip()

with open('SemackroFrontend/abrir_modal_old.txt', 'r', encoding='utf-8') as f:
    abrir_modal_old_content = f.read().strip()

# Find the start and end of the current window.abrirModalEditarPermisos
start_idx1 = html_content.find('window.abrirModalEditarPermisos = function(idRol) {')
end_idx1 = html_content.find('window.cerrarModalPermisos = function() {')

if start_idx1 != -1 and end_idx1 != -1:
    html_content = html_content[:start_idx1] + old_modal_content + '\n\n        ' + html_content[end_idx1:]

# Find the start and end of the current window.abrirModalPermisosIndividuales
start_idx2 = html_content.find('window.abrirModalPermisosIndividuales = async function')
# Note: we need to find the previous const MAPEO_GRUPOS_PERMISOS = { ... } and remove it as well.
mapeo_idx = html_content.find('const MAPEO_GRUPOS_PERMISOS = {')
if mapeo_idx != -1 and mapeo_idx < start_idx2:
    start_idx2 = mapeo_idx

end_idx2 = html_content.find('window.cerrarModalPermisosIndividuales = function() {')

if start_idx2 != -1 and end_idx2 != -1:
    html_content = html_content[:start_idx2] + abrir_modal_old_content + '\n\n        ' + html_content[end_idx2:]

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SUCCESSFULLY REPLACED BOTH MODALS WITH EXACT BACKUPS!")
