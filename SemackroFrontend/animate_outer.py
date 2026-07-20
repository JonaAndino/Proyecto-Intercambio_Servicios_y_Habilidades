import re

with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for the outer accordion button and its subsequent content div.
# Currently looks like:
# <button type="button" onclick="... content.classList.toggle('hidden'); icon.style.transform = content.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';" class="w-full ...">...<span class="iconify chevron-icon ... style="transform: rotate(180deg)"></span></button>
# <div class="p-3">

old_pattern = re.compile(
    r'<button type="button" onclick="this\.parentElement\.classList\.toggle\(\'is-open\'\); const content = this\.nextElementSibling; const icon = this\.querySelector\(\'\.chevron-icon\'\); content\.classList\.toggle\(\'hidden\'\); icon\.style\.transform = content\.classList\.contains\(\'hidden\'\) \? \'rotate\(0deg\)\' : \'rotate\(180deg\)\';" class="w-full flex items-center justify-between p-4 bg-white dark:bg-gray-900 group-\[\.is-open\]:bg-slate-100 dark:group-\[\.is-open\]:bg-gray-800/80 hover:bg-slate-50 dark:hover:bg-gray-800/50 transition-colors focus:outline-none">\s*'
    r'<div class="flex items-center gap-3">\s*'
    r'<div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">\s*'
    r'<span class="iconify" data-icon="\$\{g\.icon\}"></span>\s*'
    r'</div>\s*'
    r'<span class="font-bold text-sm text-slate-800 dark:text-gray-200">\$\{escapeHtml\(g\.nombre\)\}</span>\s*'
    r'</div>\s*'
    r'<span class="iconify chevron-icon text-slate-400 transition-transform duration-300" data-icon="mdi:chevron-down" style="transform: rotate\(180deg\)"></span>\s*'
    r'</button>\s*'
    r'<div class="p-3">',
    re.DOTALL
)

new_code = """<button type="button" onclick="this.parentElement.classList.toggle('is-open');" class="w-full flex items-center justify-between p-4 bg-white dark:bg-gray-900 group-[.is-open]:bg-slate-100 dark:group-[.is-open]:bg-gray-800/80 hover:bg-slate-50 dark:hover:bg-gray-800/50 transition-colors focus:outline-none">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                                        <span class="iconify" data-icon="${g.icon}"></span>
                                    </div>
                                    <span class="font-bold text-sm text-slate-800 dark:text-gray-200">${escapeHtml(g.nombre)}</span>
                                </div>
                                <span class="iconify chevron-icon text-slate-400 group-[.is-open]:rotate-180 transition-transform duration-300" data-icon="mdi:chevron-down"></span>
                            </button>
                            <div class="grid transition-[grid-template-rows] duration-300 ease-in-out grid-rows-[0fr] group-[.is-open]:grid-rows-[1fr]">
                                <div class="overflow-hidden">
                                    <div class="p-3">"""

count = len(old_pattern.findall(content))
print(f"Found {count} occurrences of the pattern.")

# Also need to close the two extra divs we opened in `new_code`.
# The original ended with:
#                                 ${htmlPermisos}
#                             </div>
#                         </div>

end_pattern = re.compile(
    r'(\$\{htmlPermisos\}\s*'
    r'</div>\s*'
    r'</div>)',
    re.DOTALL
)

def end_replacer(match):
    original = match.group(1)
    # The original is:
    # ${htmlPermisos}
    # </div>
    # </div>
    # But since we added two more div wrappers (grid and overflow-hidden) BEFORE `<div class="p-3">`,
    # we need to close them BEFORE the final `</div>` of the outer `rounded-2xl` container.
    return original.replace('</div>\s*</div>', '</div>\n                                    </div>\n                                </div>\n                        </div>')

# Actually, it's safer to just replace it all together or use string manipulation.
# Let's write a targeted function to do the block replacement.
# The whole block is:
full_pattern = re.compile(
    r'<button type="button" onclick="this\.parentElement\.classList\.toggle\(\'is-open\'\); const content = this\.nextElementSibling; const icon = this\.querySelector\(\'\.chevron-icon\'\); content\.classList\.toggle\(\'hidden\'\); icon\.style\.transform = content\.classList\.contains\(\'hidden\'\) \? \'rotate\(0deg\)\' : \'rotate\(180deg\)\';" class="w-full flex items-center justify-between p-4 bg-white dark:bg-gray-900 group-\[\.is-open\]:bg-slate-100 dark:group-\[\.is-open\]:bg-gray-800/80 hover:bg-slate-50 dark:hover:bg-gray-800/50 transition-colors focus:outline-none">\s*'
    r'<div class="flex items-center gap-3">\s*'
    r'<div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">\s*'
    r'<span class="iconify" data-icon="\$\{g\.icon\}"></span>\s*'
    r'</div>\s*'
    r'<span class="font-bold text-sm text-slate-800 dark:text-gray-200">\$\{escapeHtml\(g\.nombre\)\}</span>\s*'
    r'</div>\s*'
    r'<span class="iconify chevron-icon text-slate-400 transition-transform duration-300" data-icon="mdi:chevron-down" style="transform: rotate\(180deg\)"></span>\s*'
    r'</button>\s*'
    r'<div class="p-3">\s*'
    r'\$\{htmlPermisos\}\s*'
    r'</div>\s*'
    r'</div>',
    re.DOTALL
)

new_full = """<button type="button" onclick="this.parentElement.classList.toggle('is-open');" class="w-full flex items-center justify-between p-4 bg-white dark:bg-gray-900 group-[.is-open]:bg-slate-100 dark:group-[.is-open]:bg-gray-800/80 hover:bg-slate-50 dark:hover:bg-gray-800/50 transition-colors focus:outline-none">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                                        <span class="iconify" data-icon="${g.icon}"></span>
                                    </div>
                                    <span class="font-bold text-sm text-slate-800 dark:text-gray-200">${escapeHtml(g.nombre)}</span>
                                </div>
                                <span class="iconify chevron-icon text-slate-400 group-[.is-open]:rotate-180 transition-transform duration-300" data-icon="mdi:chevron-down"></span>
                            </button>
                            <div class="grid transition-[grid-template-rows] duration-300 ease-in-out grid-rows-[0fr] group-[.is-open]:grid-rows-[1fr]">
                                <div class="overflow-hidden">
                                    <div class="p-3">
                                        ${htmlPermisos}
                                    </div>
                                </div>
                            </div>
                        </div>"""

if full_pattern.search(content):
    content = full_pattern.sub(new_full, content)
    with open('Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Pattern not found!")

