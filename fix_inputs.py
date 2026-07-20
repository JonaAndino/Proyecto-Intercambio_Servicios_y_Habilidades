import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the input field for permission names with a span
old_input = r'<input type="text" value="\$\{escapeHtml\(p\.nombre\)\}" onclick="event\.stopPropagation\(\)" onchange="guardarNombrePermisoGlobal\(\'\$\{p\.clave\}\', this\.value\)" class="bg-transparent border-none p-0 focus:ring-0 text-\[14px\] font-bold text-black hover:text-blue-600 focus:text-blue-600 transition-colors w-full cursor-text" />'
new_span = r'<span class="text-[14px] font-bold text-black w-full block">${escapeHtml(p.nombre)}</span>'

content = re.sub(old_input, new_span, content)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated inputs to spans")
