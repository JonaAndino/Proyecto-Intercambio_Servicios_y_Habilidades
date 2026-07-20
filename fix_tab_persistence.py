import re

with open('SemackroFrontend/Reportes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update switchSheet to save state
new_switch_sheet = """function switchSheet(nombre) {
            // Guardar pestaña activa para mantener estado al recargar
            sessionStorage.setItem('adminActiveTab', nombre);
            
            // SEGURIDAD ESTRICTA: Evitar cambios de pestaña si no hay permisos"""
content = content.replace('function switchSheet(nombre) {\n            // SEGURIDAD ESTRICTA: Evitar cambios de pestaña si no hay permisos', new_switch_sheet)

# 2. Update DOMContentLoaded logic to load state
auto_select_logic_old = """                // 5. Autoselección de hoja si no tiene acceso a reportes pero sí a configuraciones
                if (!tieneCualquierAccesoReportes && tieneAccesoConfiguracion) {
                    switchSheet('configuraciones');
                }"""
auto_select_logic_new = """                // 5. Autoselección de hoja si no tiene acceso a reportes pero sí a configuraciones
                // O Restaurar la pestaña previamente abierta
                const savedTab = sessionStorage.getItem('adminActiveTab');
                
                if (savedTab) {
                    // Validar permisos antes de restaurar
                    let hasAccess = false;
                    if (savedTab === 'reportes') hasAccess = tieneAccesoReportes;
                    if (savedTab === 'ordenes') hasAccess = tieneCualquierAccesoReportes;
                    if (savedTab === 'recuperar') hasAccess = tieneAccesoVerificacion;
                    if (savedTab === 'configuraciones') hasAccess = tieneAccesoConfiguracion;
                    
                    if (hasAccess) {
                        switchSheet(savedTab);
                    } else {
                        if (!tieneCualquierAccesoReportes && tieneAccesoConfiguracion) switchSheet('configuraciones');
                        else switchSheet('reportes');
                    }
                } else if (!tieneCualquierAccesoReportes && tieneAccesoConfiguracion) {
                    switchSheet('configuraciones');
                }"""

content = content.replace(auto_select_logic_old, auto_select_logic_new)

with open('SemackroFrontend/Reportes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Tab persistence state fixed successfully!")
