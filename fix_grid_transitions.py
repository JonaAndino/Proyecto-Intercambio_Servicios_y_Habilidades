import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the classes that handle the grid transition
old_grid_class_master = r'class="grid transition-all duration-300 ease-in-out \$\{isMasterOpen \? \'grid-rows-\[1fr\] opacity-100\' : \'grid-rows-\[0fr\] opacity-0\'\}"'
new_grid_class_master = 'class="grid ${isMasterOpen ? \'grid-rows-[1fr] opacity-100\' : \'grid-rows-[0fr] opacity-0\'}" style="transition: grid-template-rows 350ms ease-in-out, opacity 350ms ease-in-out;"'

old_grid_class_sub = r'class="grid transition-all duration-300 ease-in-out \$\{isSubOpen \? \'grid-rows-\[1fr\] opacity-100\' : \'grid-rows-\[0fr\] opacity-0\'\}"'
new_grid_class_sub = 'class="grid ${isSubOpen ? \'grid-rows-[1fr] opacity-100\' : \'grid-rows-[0fr] opacity-0\'}" style="transition: grid-template-rows 350ms ease-in-out, opacity 350ms ease-in-out;"'

old_grid_class_subsub = r'class="grid transition-all duration-300 ease-in-out \$\{isSubSubOpen \? \'grid-rows-\[1fr\] opacity-100\' : \'grid-rows-\[0fr\] opacity-0\'\}"'
new_grid_class_subsub = 'class="grid ${isSubSubOpen ? \'grid-rows-[1fr] opacity-100\' : \'grid-rows-[0fr] opacity-0\'}" style="transition: grid-template-rows 350ms ease-in-out, opacity 350ms ease-in-out;"'

content = re.sub(old_grid_class_master, new_grid_class_master, content)
content = re.sub(old_grid_class_sub, new_grid_class_sub, content)
content = re.sub(old_grid_class_subsub, new_grid_class_subsub, content)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated grid transitions successfully")
