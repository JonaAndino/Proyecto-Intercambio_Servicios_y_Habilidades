with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

get_icono = """
        const getIconoGrupo = (grupo) => {
            const iconos = {
                'Administrador': 'mdi:shield-account',
                'Usuario Normal': 'mdi:account-group'
            };
            return iconos[grupo] || 'mdi:folder-outline';
        };
"""

if 'const getIconoGrupo = (grupo) => {' not in content:
    content = content.replace("window.abrirModalPermisosIndividuales = async function", get_icono + "\n        window.abrirModalPermisosIndividuales = async function")
    with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
