import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# For Roles
content = content.replace(
    '<span class="text-[15px] font-bold text-slate-700">${escapeHtml(p.nombre)}</span>',
    '<input type="text" value="${escapeHtml(p.nombre)}" onclick="event.stopPropagation()" onchange="guardarNombrePermisoGlobal(\'${p.clave}\', this.value)" class="bg-transparent border-none p-0 focus:ring-0 text-[15px] font-bold text-slate-700 hover:text-blue-600 focus:text-blue-600 transition-colors w-full cursor-text" />'
)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Inputs added!")
