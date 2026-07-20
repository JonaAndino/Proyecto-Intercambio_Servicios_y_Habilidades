import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the Master accordion titles text color
content = content.replace('<h4 class="font-bold text-slate-700 text-[15px]">', '<h4 class="font-bold text-black text-[15px]">')

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated master title to black")
