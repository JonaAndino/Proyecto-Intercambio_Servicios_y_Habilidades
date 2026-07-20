with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove the accidentally injected code from inside <script src="js/toast.js">
import re
content = re.sub(r'<script src="js/toast\.js">.*?</script>', '<script src="js/toast.js"></script>', content, flags=re.DOTALL)

# Now, add a new <script> block right before </body> to hold these functions securely
close_funcs = """
    <script>
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
    </script>
"""

content = content.replace('</body>', close_funcs + '\n</body>')

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Close functions moved to a valid script block!")
