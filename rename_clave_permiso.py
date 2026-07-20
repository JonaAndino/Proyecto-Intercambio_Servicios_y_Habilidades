import re

def replace_in_file(filepath, old_str, new_str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old_str, new_str)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Update Reportes.html
replace_in_file('SemackroFrontend/Reportes.html', "'VER_HISTORIAL_PERSONAL'", "'VER_POSTULACIONES_GLOBALES'")

# 2. Update permisos.js
replace_in_file('SemackroFrontend/js/permisos.js', "'VER_HISTORIAL_PERSONAL'", "'VER_POSTULACIONES_GLOBALES'")

# 3. Update session-security.js
replace_in_file('SemackroFrontend/js/session-security.js', "'VER_HISTORIAL_PERSONAL'", "'VER_POSTULACIONES_GLOBALES'")

# 4. Update the SQL setup files so any future fresh installs are correct
replace_in_file('SemackroBackend/BaseDatos/setup_roles_permisos_motivos.sql', "'VER_HISTORIAL_PERSONAL'", "'VER_POSTULACIONES_GLOBALES'")

print("Updated frontend files and sql files")
