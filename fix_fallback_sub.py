import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_fallback = """map = { 
                            master: 'Administrador', 
                            sub: 'Configuraciones', 
                            subsub: ssub,
                            nombre: p.nombre, 
                            icon: crud.icon, 
                            badgeText: crud.text, 
                            badgeColor: crud.color 
                        };"""

new_fallback = """let finalSub = 'Configuraciones';
                        if (ssub === 'Directorio General' || ssub === 'Usuarios Reportados' || ssub === 'Métricas' || ssub === 'Solicitudes de Verificación') {
                            finalSub = 'Panel de Administración';
                        }
                        
                        map = { 
                            master: 'Administrador', 
                            sub: finalSub, 
                            subsub: ssub,
                            nombre: p.nombre, 
                            icon: crud.icon, 
                            badgeText: crud.text, 
                            badgeColor: crud.color 
                        };"""

content = content.replace(old_fallback, new_fallback)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated fallback successfully")
