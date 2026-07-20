import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix hover issue on headers
# Master headers
content = content.replace('hover:bg-slate-50', 'hover:bg-slate-100')

# Actually, if an open header is bg-slate-200, hover:bg-slate-100 will make it LIGHTER (which they complained about: "se pone de color blanco eso no debe pasar").
# We should change the JS so that when OPEN, we add a class that disables the lighter hover, OR just manage hover in CSS.
# Let's remove hover:bg-slate-50 entirely from headers, and use CSS instead.

# Let's replace 'hover:bg-slate-50' with '' in the specific header contexts:
content = content.replace('cursor-pointer transition-colors hover:bg-slate-50', 'cursor-pointer transition-colors acc-header')
content = content.replace('cursor-pointer hover:bg-slate-50 transition-colors', 'cursor-pointer transition-colors acc-header')

# Inject CSS for hover behavior
css_injection = """
                    .acc-header:not(.is-active-header):hover {
                        background-color: #f1f5f9; /* bg-slate-100 */
                    }
"""

content = content.replace('.accordion-grid {', css_injection + '\n                    .accordion-grid {')

# Now update the JS to toggle 'is-active-header' along with 'bg-slate-200'
content = content.replace("header.classList.add('bg-slate-200')", "header.classList.add('bg-slate-200', 'is-active-header')")
content = content.replace("header.classList.remove('bg-slate-200')", "header.classList.remove('bg-slate-200', 'is-active-header')")


# 2. Fix text colors to be black inside the accordions
# Sub names
content = content.replace('font-bold text-slate-600 text-[14.5px]', 'font-bold text-black text-[14.5px]')
# SubSub names
content = content.replace('font-bold text-slate-600 text-[13.5px]', 'font-bold text-black text-[13.5px]')
# Permission input text
content = content.replace('text-[14px] font-bold text-slate-700', 'text-[14px] font-bold text-black')
# Icon colors to match black text, maybe make them text-black too? "las letras dentro de los acordeones deben ser negras no grises". Let's just focus on text.
# The chevron icons are text-slate-400 and become text-slate-600. Let's make them text-black when open:
content = content.replace("chevron.classList.add('rotate-180', 'text-slate-600')", "chevron.classList.add('rotate-180', 'text-black')")
content = content.replace("chevron.classList.remove('rotate-180', 'text-slate-600')", "chevron.classList.remove('rotate-180', 'text-black')")

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated hover and text colors successfully")
