with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the blue button with the indigo button in the Roles table
target = 'class="px-3 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-600 dark:bg-blue-950/20 dark:hover:bg-blue-900/30 dark:text-blue-400 text-xs font-bold transition-all flex items-center gap-1 cursor-pointer"'
replacement = 'class="px-3 py-1.5 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-600 dark:bg-indigo-950/20 dark:hover:bg-indigo-900/30 dark:text-indigo-400 text-xs font-bold transition-all flex items-center gap-1 cursor-pointer"'

if target in content:
    content = content.replace(target, replacement)
    print("Replaced blue button with indigo button.")

# Also remove any duplicate button they might have pasted
duplicate = """<button onclick="abrirModalEditarPermisos(${rol.id_rol})" class="px-3 py-1.5 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-600 dark:bg-indigo-950/20 dark:hover:bg-indigo-900/30 dark:text-indigo-400 text-xs font-bold transition-all flex items-center gap-1 cursor-pointer">
                                    <button onclick="abrirModalEditarPermisos(${rol.id_rol})" class="px-3 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-600 dark:bg-blue-950/20 dark:hover:bg-blue-900/30 dark:text-blue-400 text-xs font-bold transition-all flex items-center gap-1 cursor-pointer">"""
if duplicate in content:
    # the user probably pasted it, but let's check
    pass

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)
