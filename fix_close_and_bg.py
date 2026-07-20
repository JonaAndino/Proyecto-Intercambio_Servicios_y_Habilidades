import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix backdrop background
content = content.replace('class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity z-[9998]"', 'class="fixed inset-0 bg-transparent transition-opacity z-[9998]"')

# 2. Add closing functions if missing
close_funcs = """
        window.cerrarModalEditarPermisos = function() {
            const card = document.getElementById('permisosCard');
            if (card) {
                card.classList.remove('scale-100', 'opacity-100');
                card.classList.add('scale-95', 'opacity-0');
            }
            setTimeout(() => {
                const root = document.getElementById('permisosModalRoot');
                if(root) root.style.display = 'none';
            }, 200);
        };

        window.cerrarModalPermisosIndividuales = function() {
            const card = document.getElementById('permisosIndivCard');
            if (card) {
                card.classList.remove('scale-100', 'opacity-100');
                card.classList.add('scale-95', 'opacity-0');
            }
            setTimeout(() => {
                const root = document.getElementById('permisosIndivModalRoot');
                if(root) root.style.display = 'none';
            }, 200);
        };
"""

if 'window.cerrarModalEditarPermisos' not in content:
    # Append it right before the closing script tag of that block
    # It's at the end of the file, let's just append it before `</script>`
    content = content.replace('</script>\n</body>', close_funcs + '\n    </script>\n</body>')

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Close functions and bg-transparent applied!")
