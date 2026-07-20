import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the folder icon span
content = content.replace('<span class="iconify text-slate-400" data-icon="mdi:folder-outline"></span>', '')

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed folder icon")
