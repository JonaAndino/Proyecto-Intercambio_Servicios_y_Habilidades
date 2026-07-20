import re

with open('SemackroBackend/routes/ConfiguracionesSistema.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if "const verificarPermiso" not in content:
    content = content.replace("const db = require('../db');", "const db = require('../db');\nconst verificarPermiso = require('../middlewares/verificarPermiso');")

# Routes mapping
replacements = {
    "router.get('/', async (req, res) => {": "router.get('/', verificarPermiso('configGenerales:ver'), async (req, res) => {",
    "router.put('/', async (req, res) => {": "router.put('/', verificarPermiso('configGenerales:editar'), async (req, res) => {",
    
    "router.get('/modalidades', async (req, res) => {": "router.get('/modalidades', verificarPermiso('modalidades:ver'), async (req, res) => {",
    "router.post('/modalidades', async (req, res) => {": "router.post('/modalidades', verificarPermiso('modalidades:crear'), async (req, res) => {",
    "router.put('/modalidades/:id', async (req, res) => {": "router.put('/modalidades/:id', verificarPermiso('modalidades:editar'), async (req, res) => {",
    "router.delete('/modalidades/:id', async (req, res) => {": "router.delete('/modalidades/:id', verificarPermiso('modalidades:eliminar'), async (req, res) => {",
    
    "router.get('/motivos-bloqueo', async (req, res) => {": "router.get('/motivos-bloqueo', verificarPermiso('motivosBloqueo:ver'), async (req, res) => {",
    "router.post('/motivos-bloqueo', async (req, res) => {": "router.post('/motivos-bloqueo', verificarPermiso('motivosBloqueo:crear'), async (req, res) => {",
    "router.put('/motivos-bloqueo/:id', async (req, res) => {": "router.put('/motivos-bloqueo/:id', verificarPermiso('motivosBloqueo:editar'), async (req, res) => {",
    "router.delete('/motivos-bloqueo', async (req, res) => {": "router.delete('/motivos-bloqueo', verificarPermiso('motivosBloqueo:eliminar'), async (req, res) => {",

    "router.get('/permisos', async (req, res) => {": "router.get('/permisos', verificarPermiso('rolesPermisos:ver'), async (req, res) => {",
    "router.put('/permisos/:clave', async (req, res) => {": "router.put('/permisos/:clave', verificarPermiso('rolesPermisos:editar'), async (req, res) => {",

    "router.get('/roles', async (req, res) => {": "router.get('/roles', verificarPermiso('rolesPermisos:ver'), async (req, res) => {",
    "router.post('/roles', async (req, res) => {": "router.post('/roles', verificarPermiso('rolesPermisos:crear'), async (req, res) => {",
    "router.put('/roles/:id', async (req, res) => {": "router.put('/roles/:id', verificarPermiso('rolesPermisos:editar'), async (req, res) => {",
    "router.delete('/roles/:id', async (req, res) => {": "router.delete('/roles/:id', verificarPermiso('rolesPermisos:eliminar'), async (req, res) => {",

    "router.put('/roles/reasignar-usuarios', async (req, res) => {": "router.put('/roles/reasignar-usuarios', verificarPermiso('rolesPermisos:editar'), async (req, res) => {",
    "router.get('/roles/:id/usuarios', async (req, res) => {": "router.get('/roles/:id/usuarios', verificarPermiso('rolesPermisos:ver'), async (req, res) => {"
}

for old, new_r in replacements.items():
    if new_r not in content:
        content = content.replace(old, new_r)

with open('SemackroBackend/routes/ConfiguracionesSistema.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Backend configurations protected")
