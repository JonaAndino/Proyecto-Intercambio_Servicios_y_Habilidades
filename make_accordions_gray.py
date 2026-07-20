import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the gray color much more noticeable for open accordions

# 1. Master bg
content = content.replace("const masterBg = isMasterOpen ? 'bg-slate-50' : 'bg-white';", "const masterBg = isMasterOpen ? 'bg-slate-100' : 'bg-white';")

# 2. Sub bg
content = content.replace("const subBg = isSubOpen ? 'bg-slate-50' : 'bg-white';", "const subBg = isSubOpen ? 'bg-slate-100' : 'bg-white';")

# 3. SubSub bg
content = content.replace("${isSubSubOpen ? 'bg-slate-50' : 'bg-white'}", "${isSubSubOpen ? 'bg-slate-100' : 'bg-white'}")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated backgrounds to bg-slate-100")
