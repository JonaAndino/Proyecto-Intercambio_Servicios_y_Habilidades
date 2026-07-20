import re

with open('Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the scroll issue in permisosIndivCheckboxesContainer
# Replace: <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar min-h-[300px] flex flex-col" id="permisosIndivCheckboxesContainer">
# With: <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar min-h-0" id="permisosIndivCheckboxesContainer">

content = content.replace(
    'class="flex-1 overflow-y-auto pr-2 custom-scrollbar min-h-[300px] flex flex-col" id="permisosIndivCheckboxesContainer"',
    'class="flex-1 overflow-y-auto pr-2 custom-scrollbar min-h-0" id="permisosIndivCheckboxesContainer"'
)

# And similarly for the Roles modal if it has min-h-[400px]
content = content.replace(
    'class="flex-1 overflow-y-auto pr-2 custom-scrollbar min-h-[400px]" id="permisosCheckboxesContainer"',
    'class="flex-1 overflow-y-auto pr-2 custom-scrollbar min-h-0" id="permisosCheckboxesContainer"'
)

# 2. Make the accordion headers turn grey when expanded.
# We will use the group is-open approach for the outer accordions.
# Original outer button:
btn_pattern_1 = re.compile(r'<button type="button" onclick="const content = this\.nextElementSibling; const icon = this\.querySelector\(\'\.chevron-icon\'\); content\.classList\.toggle\(\'hidden\'\); icon\.style\.transform = content\.classList\.contains\(\'hidden\'\) \? \'rotate\(0deg\)\' : \'rotate\(180deg\)\';" class="w-full flex items-center justify-between p-4 bg-slate-50 dark:bg-gray-800/30 hover:bg-slate-100 dark:hover:bg-gray-800/50 transition-colors focus:outline-none">')

btn_replacement_1 = """<button type="button" onclick="this.parentElement.classList.toggle('is-open'); const content = this.nextElementSibling; const icon = this.querySelector('.chevron-icon'); content.classList.toggle('hidden'); icon.style.transform = content.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';" class="w-full flex items-center justify-between p-4 bg-white dark:bg-gray-900 group-[.is-open]:bg-slate-100 dark:group-[.is-open]:bg-gray-800/80 hover:bg-slate-50 dark:hover:bg-gray-800/50 transition-colors focus:outline-none">"""

content = btn_pattern_1.sub(btn_replacement_1, content)

# Update the wrapper to include group is-open initially so they start grey (since they are open by default)
wrapper_pattern = re.compile(r'<div class="mb-4 bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-2xl overflow-hidden shadow-sm">')
wrapper_replacement = r'<div class="mb-4 bg-white dark:bg-gray-900 border border-slate-200 dark:border-gray-800 rounded-2xl overflow-hidden shadow-sm group is-open">'
content = wrapper_pattern.sub(wrapper_replacement, content)

# 3. Inner categories header color
# group-[.is-open]/cat:bg-slate-50 -> group-[.is-open]/cat:bg-slate-100
cat_pattern = re.compile(r'group-\[\.is-open\]/cat:bg-slate-50')
content = cat_pattern.sub('group-[.is-open]/cat:bg-slate-100', content)


# 4. Inner subgroups header color
# They are already group-[.is-open]/sub:bg-slate-200. We can change them to slate-100 to be consistent.
sub_pattern = re.compile(r'group-\[\.is-open\]/sub:bg-slate-200')
content = sub_pattern.sub('group-[.is-open]/sub:bg-slate-100', content)


with open('Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Changes applied!")

