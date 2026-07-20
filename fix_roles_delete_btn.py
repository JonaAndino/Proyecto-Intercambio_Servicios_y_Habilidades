import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the logic inside cargarYRenderizarRolesConfig
# specifically where btnEliminar is defined.

old_btn_logic = """const btnEliminar = rol.es_default
                        ? `<button disabled class="p-2 rounded-xl bg-slate-50 text-slate-300 cursor-not-allowed">
                                <span class="iconify text-[18px]" data-icon="mdi:trash-can-outline"></span>
                           </button>`
                        : `<button onclick="eliminarRol(${rol.id_rol})" class="p-2 rounded-xl bg-red-50 hover:bg-red-100 text-red-500 transition-all cursor-pointer" title="Eliminar">
                                <span class="iconify text-[18px]" data-icon="mdi:trash-can-outline"></span>
                           </button>`;"""

new_btn_logic = """const btnEliminar = `<button onclick="eliminarRol(${rol.id_rol})" class="p-2 rounded-xl bg-red-50 hover:bg-red-100 text-red-500 transition-all cursor-pointer" title="Eliminar">
                                <span class="iconify text-[18px]" data-icon="mdi:trash-can-outline"></span>
                           </button>`;"""

if old_btn_logic in content:
    content = content.replace(old_btn_logic, new_btn_logic)
    with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated successfully")
else:
    print("Could not find exact logic. Checking regex...")
    pattern = r'const btnEliminar = rol\.es_default[\s\S]*?`([^`]+)`\s*:\s*`([^`]+)`;'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + 'const btnEliminar = `' + match.group(2) + '`;' + content[match.end():]
        with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated via regex successfully")
    else:
        print("Still not found")
