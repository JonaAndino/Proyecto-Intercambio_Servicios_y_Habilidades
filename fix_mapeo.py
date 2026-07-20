import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change ACEPTAR_INTERCAMBIOS mapping to Menu de Navegacion -> Descubrir
old_mapping = "'ACEPTAR_INTERCAMBIOS': { master: 'Administrador', sub: 'Panel de Administración', subsub: 'Solicitudes de Verificación', nombre: 'Aceptar y gestionar intercambios', icon: 'mdi:handshake-outline', badgeText: 'VER', badgeColor: 'bg-slate-50 text-slate-600 border border-slate-200 rounded-md' }"
new_mapping = "'ACEPTAR_INTERCAMBIOS': { master: 'Menú de Navegación', sub: 'Descubrir', nombre: 'Aceptar y gestionar intercambios', icon: 'mdi:handshake-outline', badgeText: 'NAVEGAR', badgeColor: 'bg-blue-50 text-blue-600 border border-blue-200 rounded-md' }"

content = content.replace(old_mapping, new_mapping)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated ACEPTAR_INTERCAMBIOS mapping")
