import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("? \\'is-open\\' : \\'\\'", "? 'is-open' : ''")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax error")
