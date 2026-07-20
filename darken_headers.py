import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the initial render background classes
content = content.replace("masterBg = isMasterOpen ? 'bg-slate-100' : 'bg-white'", "masterBg = isMasterOpen ? 'bg-slate-200' : 'bg-white'")
content = content.replace("subBg = isSubOpen ? 'bg-slate-100' : 'bg-white'", "subBg = isSubOpen ? 'bg-slate-200' : 'bg-white'")
content = content.replace("${isSubSubOpen ? 'bg-slate-100' : 'bg-white'}", "${isSubSubOpen ? 'bg-slate-200' : 'bg-white'}")

# Replace the JS toggle logic classes
content = content.replace("header.classList.add('bg-slate-100')", "header.classList.add('bg-slate-200')")
content = content.replace("header.classList.remove('bg-slate-100')", "header.classList.remove('bg-slate-200')")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated to bg-slate-200")
