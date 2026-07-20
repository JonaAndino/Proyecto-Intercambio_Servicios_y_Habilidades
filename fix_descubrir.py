import re

with open('SemackroFrontend/js/descubrir.js', 'r', encoding='latin-1') as f:
    content = f.read()

bad_block = """// === FUNCION PARA CANCELAR POSTULACION ===
async function cancelarPostulacionUsuario(idOrden) {
  if (!confirm(Ests seguro de que deseas cancelar tu postulacin a esta orden?)) return;
  
  const usuarioId = localStorage.getItem(usuarioId);
  if (!usuarioId) return;

  try {
    const res = await fetch(${API_BASE}/ordenes-trabajo//cancelar-postulacion, {
      method: DELETE,
      headers: {
        Content-Type:  pplication/json,
        Authorization: Bearer 
      },"""

# Let's use regex instead
pattern = re.compile(r'// === FUNCION PARA CANCELAR POSTULACION ===\nasync function cancelarPostulacionUsuario\(idOrden\) \{\n  if \(!confirm\(.*?\)\) return;\n  \n  const usuarioId = localStorage\.getItem\(usuarioId\);\n  if \(!usuarioId\) return;\n\n  try \{\n    const res = await fetch\(\$\{API_BASE\}/ordenes-trabajo//cancelar-postulacion, \{\n      method: DELETE,\n      headers: \{\n        Content-Type:\s+pplication/json,\n        Authorization: Bearer \n      \},')

good_block = """// === FUNCION PARA CANCELAR POSTULACION ===
async function cancelarPostulacionUsuario(idOrden) {
  if (!confirm('¿Estás seguro de que deseas cancelar tu postulación a esta orden?')) return;
  
  const usuarioId = localStorage.getItem('usuarioId');
  if (!usuarioId) return;

  try {
    const res = await fetch(`${API_BASE}/ordenes-trabajo/${idOrden}/cancelar-postulacion`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },"""

content = pattern.sub(good_block, content)

with open('SemackroFrontend/js/descubrir.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fix applied to descubrir.js!")
