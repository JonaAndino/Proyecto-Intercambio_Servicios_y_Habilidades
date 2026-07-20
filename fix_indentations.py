import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Sub accordion header
content = content.replace('px-8 py-5 cursor-pointer', 'pl-14 pr-6 py-5 cursor-pointer')

# Sub accordion items (that don't have SubSub)
content = content.replace("renderRow(p, 'px-8')", "renderRow(p, 'pl-[72px] pr-6')")

# SubSub accordion header
content = content.replace('px-10 py-4 cursor-pointer', 'pl-20 pr-6 py-4 cursor-pointer')

# SubSub accordion items
content = content.replace("renderRow(p, 'px-14 bg-white')", "renderRow(p, 'pl-[104px] pr-6 bg-white')")


with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated indentations")
