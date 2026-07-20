import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove subsub from GESTIONAR_CONFIGURACION
content = content.replace(
    "'GESTIONAR_CONFIGURACION': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Gestionar configuración general'",
    "'GESTIONAR_CONFIGURACION': { master: 'Administrador', sub: 'Configuraciones', subsub: null, nombre: 'Gestionar configuración general'"
)

# Remove subsub from ASIGNAR_ROLES_PERMISOS
content = content.replace(
    "'ASIGNAR_ROLES_PERMISOS': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Roles y Permisos', nombre: 'Asignar permisos a usuarios'",
    "'ASIGNAR_ROLES_PERMISOS': { master: 'Administrador', sub: 'Configuraciones', subsub: null, nombre: 'Asignar permisos a usuarios'"
)

# Fix the fallback to set ssub = null instead of 'Otros Permisos'
content = content.replace(
    "let ssub = 'Otros Permisos';",
    "let ssub = null;"
)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed config subsubs")
