import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace `const jerarquia = { 'Menú de Navegación': {}, 'Administrador': {} };` with an ordered pre-populated object.
old_jerarquia = "const jerarquia = { 'Menú de Navegación': {}, 'Administrador': {} };"
new_jerarquia = """const jerarquia = { 
                    'Menú de Navegación': {}, 
                    'Administrador': {
                        'Panel de Administración': { _items: [], _subsubs: {} },
                        'Configuraciones': { 
                            _items: [], 
                            _subsubs: {
                                'Ajustes Globales': [],
                                'Modalidades de Intercambio': [],
                                'Categorías de Habilidades': [],
                                'Variables de Entorno': [],
                                'Motivos de Bloqueo': [],
                                'Roles y Permisos': []
                            }
                        },
                        'Postulaciones': { _items: [], _subsubs: {} }
                    } 
                };"""

content = content.replace(old_jerarquia, new_jerarquia)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Forced order of subsubs")
