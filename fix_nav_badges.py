import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace rounded-full with rounded-md for the menu navigation badges
content = content.replace("badgeColor: 'bg-blue-50 text-blue-500 rounded-full'", "badgeColor: 'bg-blue-50 text-blue-500 rounded-md'")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed rounded borders")
