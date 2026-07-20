import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update jerarquia
content = content.replace("const jerarquia = { 'Menú de Navegación': {}, 'Administrador': {}, 'Postulaciones': {} };", "const jerarquia = { 'Menú de Navegación': {}, 'Administrador': {} };")

# 2. Update finalMaster checks
content = content.replace("finalMaster !== 'Menú de Navegación' && finalMaster !== 'Administrador' && finalMaster !== 'Postulaciones'", "finalMaster !== 'Menú de Navegación' && finalMaster !== 'Administrador'")

# 3. Update MAPEO_AVANZADO
old_mapping = "'VER_POSTULACIONES_GLOBALES': { master: 'Postulaciones', sub: 'Panel Global', nombre: 'Ver postulaciones globales'"
new_mapping = "'VER_POSTULACIONES_GLOBALES': { master: 'Administrador', sub: 'Postulaciones', subsub: 'Panel Global', nombre: 'Ver postulaciones globales'"
content = content.replace(old_mapping, new_mapping)

# 4. Update ICONOS_MASTER
old_iconos = """            const ICONOS_MASTER = {
                'Menú de Navegación': 'mdi:compass-outline',
                'Administrador': 'mdi:shield-star-outline',
                'Postulaciones': 'mdi:file-document-multiple-outline'
            };"""
new_iconos = """            const ICONOS_MASTER = {
                'Menú de Navegación': 'mdi:compass-outline',
                'Administrador': 'mdi:shield-star-outline'
            };"""
if old_iconos in content:
    content = content.replace(old_iconos, new_iconos)
else:
    content = content.replace("'Postulaciones': 'mdi:file-document-multiple-outline'", "")

# 5. Remove from default open
old_open = """            window.acordeonesMasterAbiertos = window.acordeonesMasterAbiertos || { 
                'Menú de Navegación': true, 
                'Administrador': true,
                'Postulaciones': true
            };"""
new_open = """            window.acordeonesMasterAbiertos = window.acordeonesMasterAbiertos || { 
                'Menú de Navegación': true, 
                'Administrador': true 
            };"""
content = content.replace(old_open, new_open)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Moved Postulaciones inside Administrador")
