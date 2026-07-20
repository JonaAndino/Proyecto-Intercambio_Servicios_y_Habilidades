const MAPEO_AVANZADO = {
    'descubrir': { master: 'Menú de Navegación', sub: 'Descubrir', nombre: 'Acceso a Descubrir' },
    'VER_METRICAS': { master: 'Administrador', sub: 'Panel de Administración', nombre: 'Ver tabla de métricas' },
    'configGenerales:ver': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Ver' },
    'configGenerales:editar': { master: 'Administrador', sub: 'Configuraciones', subsub: 'Ajustes Globales', nombre: 'Editar' },
};

const todosLosPermisosDisponibles = Object.keys(MAPEO_AVANZADO).map(k => ({clave: k, nombre: MAPEO_AVANZADO[k].nombre}));

const jerarquia = { 'Menú de Navegación': {}, 'Administrador': {} }; 

todosLosPermisosDisponibles.forEach(p => {
    let map = MAPEO_AVANZADO[p.clave] || { master: 'Administrador', sub: 'Configuraciones' };
    let finalMaster = map.master;
    if (!jerarquia[finalMaster]) jerarquia[finalMaster] = {};
    
    if (!jerarquia[finalMaster][map.sub]) {
        jerarquia[finalMaster][map.sub] = { _items: [], _subsubs: {} };
    }
    
    if (map.subsub) {
        if (!jerarquia[finalMaster][map.sub]._subsubs[map.subsub]) {
            jerarquia[finalMaster][map.sub]._subsubs[map.subsub] = [];
        }
        jerarquia[finalMaster][map.sub]._subsubs[map.subsub].push({ ...p, ...map });
    } else {
        jerarquia[finalMaster][map.sub]._items.push({ ...p, ...map });
    }
});

console.log(JSON.stringify(jerarquia, null, 2));
