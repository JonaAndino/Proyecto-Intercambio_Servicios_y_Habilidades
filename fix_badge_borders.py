import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add borders to the badge colors
content = content.replace("bg-blue-50 text-blue-600 rounded-md", "bg-blue-50 text-blue-600 border border-blue-200 rounded-md")
content = content.replace("bg-slate-100 text-slate-600 rounded-md", "bg-slate-50 text-slate-600 border border-slate-200 rounded-md") # Also make slate lighter to match the border style
content = content.replace("bg-red-50 text-red-500 rounded-md", "bg-red-50 text-red-500 border border-red-200 rounded-md")
content = content.replace("bg-emerald-50 text-emerald-500 rounded-md", "bg-emerald-50 text-emerald-500 border border-emerald-200 rounded-md")
content = content.replace("bg-amber-50 text-amber-500 rounded-md", "bg-amber-50 text-amber-500 border border-amber-200 rounded-md")
content = content.replace("bg-purple-50 text-purple-500 rounded-md", "bg-purple-50 text-purple-500 border border-purple-200 rounded-md")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added borders to badges")
