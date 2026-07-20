import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change the name of VER_HISTORIAL_PERSONAL to avoid confusion with the regular user's "historial"
old_mapping = "'VER_HISTORIAL_PERSONAL': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Historial', nombre: 'Ver historial de actividades', icon: 'mdi:history', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' }"
new_mapping = "'VER_HISTORIAL_PERSONAL': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Panel Global', nombre: 'Ver postulaciones globales', icon: 'mdi:history', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' }"

content = content.replace(old_mapping, new_mapping)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Renamed VER_HISTORIAL_PERSONAL")
