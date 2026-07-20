import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject the CSS styles at the beginning of the modal rendering
custom_css = """
            if (!document.getElementById('accordion-styles')) {
                const style = document.createElement('style');
                style.id = 'accordion-styles';
                style.innerHTML = `
                    .accordion-grid {
                        display: grid;
                        grid-template-rows: 0fr;
                        transition: grid-template-rows 350ms cubic-bezier(0.4, 0, 0.2, 1), opacity 350ms ease-in-out;
                        opacity: 0;
                    }
                    .accordion-grid.is-open {
                        grid-template-rows: 1fr;
                        opacity: 1;
                    }
                `;
                document.head.appendChild(style);
            }
"""

# Insert custom_css right after window.abrirModalEditarPermisos = function(idRol) { ...
content = re.sub(
    r'(window\.abrirModalEditarPermisos = function\([^)]*\) \{.*?\n)', 
    r'\1' + custom_css, 
    content, 
    count=1
)

content = re.sub(
    r'(window\.abrirModalPermisosIndividuales = async function\([^)]*\) \{.*?\n)', 
    r'\1' + custom_css, 
    content, 
    count=1
)

# 2. Update the JS toggles to use .is-open
def update_toggle_js(content):
    # Master
    content = re.sub(
        r"grid\.classList\.remove\('grid-rows-\[0fr\]', 'opacity-0'\); grid\.classList\.add\('grid-rows-\[1fr\]', 'opacity-100'\);",
        r"grid.classList.add('is-open');",
        content
    )
    content = re.sub(
        r"grid\.classList\.remove\('grid-rows-\[1fr\]', 'opacity-100'\); grid\.classList\.add\('grid-rows-\[0fr\]', 'opacity-0'\);",
        r"grid.classList.remove('is-open');",
        content
    )
    
    return content

content = update_toggle_js(content)

# 3. Update the HTML strings to use .accordion-grid and conditional .is-open
# Master
content = re.sub(
    r'class="master-grid grid \$\{isMasterOpen \? \'grid-rows-\[1fr\] opacity-100\' : \'grid-rows-\[0fr\] opacity-0\'\}" style="[^"]*"',
    r'class="master-grid accordion-grid ${isMasterOpen ? \'is-open\' : \'\'}"',
    content
)
# Sub
content = re.sub(
    r'class="sub-grid grid \$\{isSubOpen \? \'grid-rows-\[1fr\] opacity-100\' : \'grid-rows-\[0fr\] opacity-0\'\}" style="[^"]*"',
    r'class="sub-grid accordion-grid ${isSubOpen ? \'is-open\' : \'\'}"',
    content
)
# SubSub
content = re.sub(
    r'class="subsub-grid grid \$\{isSubSubOpen \? \'grid-rows-\[1fr\] opacity-100\' : \'grid-rows-\[0fr\] opacity-0\'\}" style="[^"]*"',
    r'class="subsub-grid accordion-grid ${isSubSubOpen ? \'is-open\' : \'\'}"',
    content
)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated animation to pure CSS successfully")
