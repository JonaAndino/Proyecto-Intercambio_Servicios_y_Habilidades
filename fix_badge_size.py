import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the badge class in both roles and individual modals
old_badge_class = 'px-3 py-1 rounded-full text-[10px] font-extrabold tracking-wider uppercase ${p.badgeColor}'
new_badge_class = 'w-[90px] py-1.5 rounded-full text-[10px] font-extrabold tracking-wider uppercase text-center flex-shrink-0 ${p.badgeColor}'

content = content.replace(old_badge_class, new_badge_class)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Badges updated to have identical size!")
