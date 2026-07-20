import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the lighter blue with the exact deeper blue (blue-600) used in the rest of the UI
content = content.replace("bg-blue-50 text-blue-500", "bg-blue-50 text-blue-600")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated blue color to blue-600")
