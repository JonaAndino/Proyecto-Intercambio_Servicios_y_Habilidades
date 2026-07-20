import re

with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to remove from `};                todosLosPermisosDisponibles.forEach` up to `window.cerrarModalPermisos = function`
pattern = re.compile(r'\};\s*todosLosPermisosDisponibles\.forEach\(p => \{.*?window\.cerrarModalPermisos = function', re.DOTALL)
replacement = '};\n\n        window.cerrarModalPermisos = function'

if pattern.search(content):
    content = pattern.sub(replacement, content)
    with open('Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned up dead code successfully!")
else:
    print("Pattern not found!")

