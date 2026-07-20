import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_str = "'VER_POSTULACIONES_GLOBALES': { master: 'Administrador', sub: 'Postulaciones', subsub: 'Panel Global', nombre: 'Ver postulaciones globales'"
new_str = "'VER_POSTULACIONES_GLOBALES': { master: 'Administrador', sub: 'Postulaciones', subsub: null, nombre: 'Ver postulaciones en formato de lista'"

if old_str in content:
    content = content.replace(old_str, new_str)
    with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated VER_POSTULACIONES_GLOBALES mapping.")
else:
    print("Warning: old string not found.")

