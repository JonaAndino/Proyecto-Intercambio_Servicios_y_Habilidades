import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'if \(!rol \|\| rol\.es_default\) return;'
new_code = 'if (!rol) return;'

if re.search(pattern, content):
    content = re.sub(pattern, new_code, content)
    with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated successfully")
else:
    print("Could not find the pattern")
