import re

with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We only want to replace purple with blue in the contexts of the individual permissions styling.
# We should probably leave 'admin' badge as purple (line 7283).
# Let's replace the specific lines 6963-6966, 7155-7159, and 7428-7431 manually or via string replace.

# Block 1 (renderRow inside abrirModalPermisosIndividuales):
block1_old = """                                    colorFondo = 'border-purple-200 dark:border-purple-800 bg-purple-50/50 dark:bg-purple-900/20';
                                    colorTitulo = 'text-purple-800 dark:text-purple-200';
                                    colorIcono = 'text-purple-500';
                                    colorFinal = 'text-purple-600';"""

block1_new = """                                    colorFondo = 'border-blue-200 dark:border-blue-800 bg-blue-50/50 dark:bg-blue-900/20';
                                    colorTitulo = 'text-blue-800 dark:text-blue-200';
                                    colorIcono = 'text-blue-500';
                                    colorFinal = 'text-blue-600';"""

content = content.replace(block1_old, block1_new)

# Block 2 (actualizarVisualFilaPermiso)
block2_old = """                    colorFondo = 'border-purple-200 dark:border-purple-800 bg-purple-50/50 dark:bg-purple-900/20';
                    colorTitulo = 'text-purple-800 dark:text-purple-200';
                    colorIcono = 'text-purple-500';
                    colorFinal = 'text-purple-600';
                    bgIcono = 'bg-purple-100 dark:bg-purple-900/30';"""

block2_new = """                    colorFondo = 'border-blue-200 dark:border-blue-800 bg-blue-50/50 dark:bg-blue-900/20';
                    colorTitulo = 'text-blue-800 dark:text-blue-200';
                    colorIcono = 'text-blue-500';
                    colorFinal = 'text-blue-600';
                    bgIcono = 'bg-blue-100 dark:bg-blue-900/30';"""

content = content.replace(block2_old, block2_new)


# Let's double check if there's any other place.
with open('Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Color replacement successful.")
