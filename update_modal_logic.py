import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_function(content, func_name, new_func_code):
    pattern = r'(window\.' + func_name + r'\s*=\s*(?:async\s*)?function\s*\([^)]*\)\s*\{)(.*?)(?=\n        window\.[a-zA-Z0-9_]+\s*=\s*(?:async\s*)?function|\n    </script>)'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"Could not find {func_name}")
        return content
    return content[:match.start()] + new_func_code + content[match.end():]

# We need to extract the existing map and hierarchy building logic.
# Wait, let's just do targeted string replacements inside the file.

# 1. Update toggle functions to NOT re-render, but use DOM
new_toggles = """
            window.togglePermisoRol = (clave, isChecked) => {
                if (isChecked) window.permisosSeleccionados.add(clave);
                else window.permisosSeleccionados.delete(clave);
            };

            window.toggleAcordeonMaster = (e, grupo) => {
                window.acordeonesMasterAbiertos[grupo] = !window.acordeonesMasterAbiertos[grupo];
                const isOpen = window.acordeonesMasterAbiertos[grupo];
                const header = e.currentTarget;
                const container = header.parentElement;
                const grid = container.querySelector('.master-grid');
                const inner = grid.firstElementChild;
                const chevron = header.querySelector('.master-chevron');
                
                if (isOpen) {
                    header.classList.remove('bg-white'); header.classList.add('bg-slate-100');
                    grid.classList.remove('grid-rows-[0fr]', 'opacity-0'); grid.classList.add('grid-rows-[1fr]', 'opacity-100');
                    inner.classList.remove('border-transparent'); inner.classList.add('border-slate-200');
                    chevron.classList.add('rotate-180', 'text-slate-600');
                } else {
                    header.classList.remove('bg-slate-100'); header.classList.add('bg-white');
                    grid.classList.remove('grid-rows-[1fr]', 'opacity-100'); grid.classList.add('grid-rows-[0fr]', 'opacity-0');
                    inner.classList.remove('border-slate-200'); inner.classList.add('border-transparent');
                    chevron.classList.remove('rotate-180', 'text-slate-600');
                }
            };
            
            window.toggleAcordeonSub = (e, subKey) => {
                window.acordeonesSubAbiertos[subKey] = !window.acordeonesSubAbiertos[subKey];
                const isOpen = window.acordeonesSubAbiertos[subKey];
                const header = e.currentTarget;
                const container = header.parentElement;
                const grid = container.querySelector(':scope > .sub-grid');
                const inner = grid.firstElementChild;
                const chevron = header.querySelector('.sub-chevron');
                
                if (isOpen) {
                    header.classList.remove('bg-white'); header.classList.add('bg-slate-100');
                    grid.classList.remove('grid-rows-[0fr]', 'opacity-0'); grid.classList.add('grid-rows-[1fr]', 'opacity-100');
                    inner.classList.remove('border-transparent'); inner.classList.add('border-slate-50');
                    chevron.classList.add('rotate-180', 'text-slate-600');
                } else {
                    header.classList.remove('bg-slate-100'); header.classList.add('bg-white');
                    grid.classList.remove('grid-rows-[1fr]', 'opacity-100'); grid.classList.add('grid-rows-[0fr]', 'opacity-0');
                    inner.classList.remove('border-slate-50'); inner.classList.add('border-transparent');
                    chevron.classList.remove('rotate-180', 'text-slate-600');
                }
            };

            window.toggleAcordeonSubSub = (e, subsubKey) => {
                window.acordeonesSubSubAbiertos[subsubKey] = !window.acordeonesSubSubAbiertos[subsubKey];
                const isOpen = window.acordeonesSubSubAbiertos[subsubKey];
                const header = e.currentTarget;
                const container = header.parentElement;
                const grid = container.querySelector(':scope > .subsub-grid');
                const inner = grid.firstElementChild;
                const chevron = header.querySelector('.subsub-chevron');
                
                if (isOpen) {
                    header.classList.remove('bg-white'); header.classList.add('bg-slate-100');
                    grid.classList.remove('grid-rows-[0fr]', 'opacity-0'); grid.classList.add('grid-rows-[1fr]', 'opacity-100');
                    inner.classList.remove('border-transparent'); inner.classList.add('border-slate-50');
                    chevron.classList.add('rotate-180', 'text-slate-600');
                } else {
                    header.classList.remove('bg-slate-100'); header.classList.add('bg-white');
                    grid.classList.remove('grid-rows-[1fr]', 'opacity-100'); grid.classList.add('grid-rows-[0fr]', 'opacity-0');
                    inner.classList.remove('border-slate-50'); inner.classList.add('border-transparent');
                    chevron.classList.remove('rotate-180', 'text-slate-600');
                }
            };
"""

content = re.sub(
    r'window\.togglePermisoRol = \([^)]*\) => \{.*?\};.*?window\.toggleAcordeonSubSub = \([^)]*\) => \{.*?\};', 
    new_toggles, 
    content, 
    flags=re.DOTALL
)

# 2. Update toggle calls in HTML strings for ROLES MODAL
content = content.replace("onclick=\"toggleAcordeonMaster('", "onclick=\"toggleAcordeonMaster(event, '")
content = content.replace("onclick=\"toggleAcordeonSub('", "onclick=\"toggleAcordeonSub(event, '")
content = content.replace("onclick=\"toggleAcordeonSubSub('", "onclick=\"toggleAcordeonSubSub(event, '")

# Add missing classes for targeting elements in ROLES MODAL
# Master
content = content.replace(
    'class="grid ${isMasterOpen', 
    'class="master-grid grid ${isMasterOpen'
)
content = content.replace(
    'class="iconify text-slate-400 text-xl transition-transform ${isMasterOpen', 
    'class="master-chevron iconify text-slate-400 text-xl transition-transform ${isMasterOpen'
)
# Sub
content = content.replace(
    'class="grid ${isSubOpen', 
    'class="sub-grid grid ${isSubOpen'
)
content = content.replace(
    'class="iconify text-slate-400 text-xl transition-transform ${isSubOpen', 
    'class="sub-chevron iconify text-slate-400 text-xl transition-transform ${isSubOpen'
)
# SubSub
content = content.replace(
    'class="grid ${isSubSubOpen', 
    'class="subsub-grid grid ${isSubSubOpen'
)
content = content.replace(
    'class="iconify text-slate-400 text-lg transition-transform ${isSubSubOpen', 
    'class="subsub-chevron iconify text-slate-400 text-lg transition-transform ${isSubSubOpen'
)


# 3. Repeat for INDIVIDUAL MODAL toggles
new_toggles_indiv = """
                window.toggleExcepcionPermiso = (clave, isChecked) => {
                    const idx = window.excepcionesCargadas.findIndex(e => e.link === clave);
                    if (isChecked) {
                        if (idx !== -1) window.excepcionesCargadas[idx].concedido = true;
                        else window.excepcionesCargadas.push({ link: clave, concedido: true });
                    } else {
                        if (idx !== -1) window.excepcionesCargadas[idx].concedido = false;
                        else window.excepcionesCargadas.push({ link: clave, concedido: false });
                    }
                };

                window.toggleAcordeonMasterIndiv = (e, grupo) => {
                    window.acordeonesMasterAbiertosIndiv[grupo] = !window.acordeonesMasterAbiertosIndiv[grupo];
                    const isOpen = window.acordeonesMasterAbiertosIndiv[grupo];
                    const header = e.currentTarget;
                    const container = header.parentElement;
                    const grid = container.querySelector('.master-grid');
                    const inner = grid.firstElementChild;
                    const chevron = header.querySelector('.master-chevron');
                    
                    if (isOpen) {
                        header.classList.remove('bg-white'); header.classList.add('bg-slate-100');
                        grid.classList.remove('grid-rows-[0fr]', 'opacity-0'); grid.classList.add('grid-rows-[1fr]', 'opacity-100');
                        inner.classList.remove('border-transparent'); inner.classList.add('border-slate-200');
                        chevron.classList.add('rotate-180', 'text-slate-600');
                    } else {
                        header.classList.remove('bg-slate-100'); header.classList.add('bg-white');
                        grid.classList.remove('grid-rows-[1fr]', 'opacity-100'); grid.classList.add('grid-rows-[0fr]', 'opacity-0');
                        inner.classList.remove('border-slate-200'); inner.classList.add('border-transparent');
                        chevron.classList.remove('rotate-180', 'text-slate-600');
                    }
                };
                
                window.toggleAcordeonSubIndiv = (e, subKey) => {
                    window.acordeonesSubAbiertosIndiv[subKey] = !window.acordeonesSubAbiertosIndiv[subKey];
                    const isOpen = window.acordeonesSubAbiertosIndiv[subKey];
                    const header = e.currentTarget;
                    const container = header.parentElement;
                    const grid = container.querySelector(':scope > .sub-grid');
                    const inner = grid.firstElementChild;
                    const chevron = header.querySelector('.sub-chevron');
                    
                    if (isOpen) {
                        header.classList.remove('bg-white'); header.classList.add('bg-slate-100');
                        grid.classList.remove('grid-rows-[0fr]', 'opacity-0'); grid.classList.add('grid-rows-[1fr]', 'opacity-100');
                        inner.classList.remove('border-transparent'); inner.classList.add('border-slate-50');
                        chevron.classList.add('rotate-180', 'text-slate-600');
                    } else {
                        header.classList.remove('bg-slate-100'); header.classList.add('bg-white');
                        grid.classList.remove('grid-rows-[1fr]', 'opacity-100'); grid.classList.add('grid-rows-[0fr]', 'opacity-0');
                        inner.classList.remove('border-slate-50'); inner.classList.add('border-transparent');
                        chevron.classList.remove('rotate-180', 'text-slate-600');
                    }
                };

                window.toggleAcordeonSubSubIndiv = (e, subsubKey) => {
                    window.acordeonesSubSubAbiertosIndiv[subsubKey] = !window.acordeonesSubSubAbiertosIndiv[subsubKey];
                    const isOpen = window.acordeonesSubSubAbiertosIndiv[subsubKey];
                    const header = e.currentTarget;
                    const container = header.parentElement;
                    const grid = container.querySelector(':scope > .subsub-grid');
                    const inner = grid.firstElementChild;
                    const chevron = header.querySelector('.subsub-chevron');
                    
                    if (isOpen) {
                        header.classList.remove('bg-white'); header.classList.add('bg-slate-100');
                        grid.classList.remove('grid-rows-[0fr]', 'opacity-0'); grid.classList.add('grid-rows-[1fr]', 'opacity-100');
                        inner.classList.remove('border-transparent'); inner.classList.add('border-slate-50');
                        chevron.classList.add('rotate-180', 'text-slate-600');
                    } else {
                        header.classList.remove('bg-slate-100'); header.classList.add('bg-white');
                        grid.classList.remove('grid-rows-[1fr]', 'opacity-100'); grid.classList.add('grid-rows-[0fr]', 'opacity-0');
                        inner.classList.remove('border-slate-50'); inner.classList.add('border-transparent');
                        chevron.classList.remove('rotate-180', 'text-slate-600');
                    }
                };
"""

content = re.sub(
    r'window\.toggleExcepcionPermiso = \([^)]*\) => \{.*?\};', 
    new_toggles_indiv, 
    content, 
    flags=re.DOTALL
)

# Replace inline onclicks in Indiv modal
content = re.sub(r"onclick=\"window\.acordeonesMasterAbiertosIndiv\['([^']+)'\] = !window\.acordeonesMasterAbiertosIndiv\['\1'\]; window\.renderizarModalPermisosIndiv\(\);\"", r"onclick=\"window.toggleAcordeonMasterIndiv(event, '\1')\"", content)
content = re.sub(r"onclick=\"window\.acordeonesSubAbiertosIndiv\['([^']+)'\] = !window\.acordeonesSubAbiertosIndiv\['\1'\]; window\.renderizarModalPermisosIndiv\(\);\"", r"onclick=\"window.toggleAcordeonSubIndiv(event, '\1')\"", content)
content = re.sub(r"onclick=\"window\.acordeonesSubSubAbiertosIndiv\['([^']+)'\] = !window\.acordeonesSubSubAbiertosIndiv\['\1'\]; window\.renderizarModalPermisosIndiv\(\);\"", r"onclick=\"window.toggleAcordeonSubSubIndiv(event, '\1')\"", content)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated DOM toggles successfully")
