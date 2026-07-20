import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix for Sub Accordion
old_sub = r'<div class="transition-all \$\{isSubOpen \? \'block\' : \'hidden\'\} bg-white border-t border-slate-50">\s*\$\{htmlPermisos\}\s*</div>'
new_sub = """<div class="grid transition-all duration-300 ease-in-out ${isSubOpen ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'}">
                                    <div class="overflow-hidden bg-white border-t ${isSubOpen ? 'border-slate-50' : 'border-transparent'}">
                                        ${htmlPermisos}
                                    </div>
                                </div>"""

# Fix for Master Accordion
old_master = r'<div class="transition-all \$\{isMasterOpen \? \'block\' : \'hidden\'\} bg-white border-t border-slate-200">\s*<div class="flex flex-col">\s*\$\{htmlSubs\}\s*</div>\s*</div>'
new_master = """<div class="grid transition-all duration-300 ease-in-out ${isMasterOpen ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'}">
                                <div class="overflow-hidden bg-white border-t ${isMasterOpen ? 'border-slate-200' : 'border-transparent'}">
                                    <div class="flex flex-col">
                                        ${htmlSubs}
                                    </div>
                                </div>
                            </div>"""


if re.search(old_sub, content) and re.search(old_master, content):
    content = re.sub(old_sub, new_sub, content)
    content = re.sub(old_master, new_master, content)
    with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated accordion animations successfully")
else:
    print("Regex match failed")

