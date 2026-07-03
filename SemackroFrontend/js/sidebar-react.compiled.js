// Guard: verificar que React esté disponible antes de ejecutar el módulo
(function initWhenReady() {
  if (typeof React === 'undefined' || typeof ReactDOM === 'undefined') {
    console.warn('⏳ React/ReactDOM no disponible aún, reintentando...');
    setTimeout(initWhenReady, 50);
    return;
  }
  initSidebar();
})();
function initSidebar() {
  const {
    useState,
    useEffect
  } = React;

  /**
   * SidebarReact V9: 100% CSS - Sin Framer Motion
   * Elimina completamente la dependencia de Motion para evitar conflictos de keys
   */

  // Helper para traducciones
  var t = key => {
    if (window.t_real && typeof window.t_real === 'function') return window.t_real(key);
    if (window.t && typeof window.t === 'function' && window.t !== t) return window.t(key);
    return key;
  };
  const SidebarReact = () => {
    const [conversations, setConversations] = useState([]);
    const [isHovered, setIsHovered] = useState(false);
    const [activeId, setActiveId] = useState(null);
    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    useEffect(() => {
      const handleResize = () => setIsMobile(window.innerWidth < 768);
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }, []);
    useEffect(() => {
      const fetchGlobal = () => {
        const raw = window.conversacionesDashboard || [];

        // Deduplicación por ID
        const seen = new Set();
        const unique = raw.filter(c => {
          const id = c.id_conversacion;
          if (!id || seen.has(id)) return false;
          seen.add(id);
          return true;
        });
        setConversations(prev => {
          const isSame = prev.length === unique.length && JSON.stringify(prev) === JSON.stringify(unique);
          return isSame ? prev : [...unique];
        });
        if (window.conversacionActivaDashboard) {
          setActiveId(window.conversacionActivaDashboard.id_conversacion);
        }
      };
      const timer = setInterval(fetchGlobal, 450);
      fetchGlobal();
      return () => clearInterval(timer);
    }, []);

    // En móvil siempre expandido (width 100%), en desktop usa hover
    const sidebarStyle = isMobile ? {
      width: '100%'
    } : {
      width: isHovered ? '280px' : '88px',
      transition: 'width 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
    };

    // En móvil mostramos los detalles siempre
    const showDetails = isMobile || isHovered;
    return /*#__PURE__*/React.createElement("div", {
      className: `h-full bg-white border-r border-gray-100 flex flex-col relative z-50 shadow-md overflow-hidden ${isMobile ? 'w-full' : ''}`,
      style: sidebarStyle,
      onMouseEnter: () => !isMobile && setIsHovered(true),
      onMouseLeave: () => !isMobile && setIsHovered(false)
    }, /*#__PURE__*/React.createElement("div", {
      className: "h-[80px] border-b border-gray-50 flex items-center justify-center shrink-0 px-4"
    }, /*#__PURE__*/React.createElement("div", {
      className: `transition-all duration-300 ${showDetails ? 'opacity-100' : 'opacity-0 w-0'}`
    }, /*#__PURE__*/React.createElement("h2", {
      className: "text-lg font-black text-slate-800 whitespace-nowrap"
    }, typeof t === 'function' ? t('messages.title') : 'Mensajes')), /*#__PURE__*/React.createElement("div", {
      className: `transition-all duration-300 text-blue-600 ${showDetails ? 'opacity-0 w-0 absolute' : 'opacity-100'}`
    }, /*#__PURE__*/React.createElement("span", {
      className: "iconify",
      "data-icon": "mdi:chat-processing",
      "data-width": "32"
    }))), /*#__PURE__*/React.createElement("div", {
      className: "flex-1 overflow-y-auto overflow-x-hidden py-4 space-y-1",
      style: {
        scrollbarWidth: 'none',
        /* Firefox */
        msOverflowStyle: 'none' /* IE/Edge */
      }
    }, /*#__PURE__*/React.createElement("style", null, `
                    .sidebar-scroll::-webkit-scrollbar {
                        display: none;
                    }
                `), conversations.length === 0 ? /*#__PURE__*/React.createElement("div", {
      className: "p-8 text-center opacity-10"
    }, /*#__PURE__*/React.createElement("span", {
      className: "iconify mx-auto",
      "data-icon": "mdi:chat-outline",
      "data-width": "32"
    })) : conversations.map(conv => /*#__PURE__*/React.createElement(ConversationItem, {
      key: conv.id_conversacion,
      conv: conv,
      isHovered: showDetails,
      isActive: activeId === conv.id_conversacion,
      onClick: () => window.seleccionarConversacionDashboard?.(conv.id_conversacion)
    }))));
  };
  const ConversationItem = ({
    conv,
    isHovered,
    isActive,
    onClick
  }) => {
    const nombre = conv.nombre_contacto || "Usuario";
    const initials = nombre.charAt(0).toUpperCase();
    const unread = conv.mensajes_no_leidos || 0;

    // Paleta de colores para grupos (OT:) — distingue cada conversación visualmente
    const GROUP_COLORS = ['bg-violet-500',
    // morado
    'bg-emerald-500',
    // verde
    'bg-orange-500',
    // naranja
    'bg-pink-500',
    // rosa
    'bg-teal-500',
    // teal
    'bg-amber-500',
    // ámbar
    'bg-cyan-600',
    // cyan
    'bg-rose-500',
    // rojo rosado
    'bg-lime-600',
    // lima
    'bg-fuchsia-500' // fucsia
    ];

    // Asignar color basado en el id_conversacion (siempre determinístico)
    const isGroup = nombre.startsWith('OT:') || conv.es_grupo;
    const colorIdx = conv.id_conversacion ? Number(conv.id_conversacion) % GROUP_COLORS.length : 0;
    const avatarBgClass = isGroup ? GROUP_COLORS[colorIdx] : isActive ? 'bg-white/20' : 'bg-blue-500';
    return /*#__PURE__*/React.createElement("div", {
      onClick: onClick,
      className: `mx-3 my-2 rounded-xl cursor-pointer transition-all duration-200 flex items-center relative group h-14 ${isActive ? 'bg-blue-600' : 'bg-white hover:bg-blue-100'}`
    }, /*#__PURE__*/React.createElement("div", {
      className: "relative shrink-0 w-11 h-11 flex items-center justify-center"
    }, conv.imagenUrl_contacto ? /*#__PURE__*/React.createElement("img", {
      src: conv.imagenUrl_contacto,
      className: `w-full h-full rounded-full object-cover border-2 shadow-sm ${isActive ? 'border-blue-400' : 'border-white'}`,
      alt: nombre
    }) : /*#__PURE__*/React.createElement("div", {
      className: `w-full h-full rounded-full flex items-center justify-center text-white font-bold shadow-sm ${avatarBgClass}`
    }, initials), !isHovered && unread > 0 && /*#__PURE__*/React.createElement("div", {
      className: "absolute -top-1 -right-1 w-4 h-4 bg-red-500 border-2 border-white rounded-full shadow-md z-10"
    })), /*#__PURE__*/React.createElement("div", {
      className: `ml-3 flex-1 min-w-0 transition-all duration-300 ${isHovered ? 'opacity-100' : 'opacity-0 w-0 overflow-hidden'}`
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex items-center justify-between gap-1"
    }, /*#__PURE__*/React.createElement("p", {
      className: `text-sm font-bold truncate ${isActive ? 'text-white' : 'text-slate-800'}`
    }, nombre), unread > 0 && /*#__PURE__*/React.createElement("span", {
      className: `text-[10px] font-black rounded-full px-1.5 py-0.5 min-w-[18px] text-center ${isActive ? 'bg-white text-blue-600' : 'bg-blue-600 text-white'}`
    }, unread)), /*#__PURE__*/React.createElement("p", {
      className: `text-[11px] truncate mt-0.5 font-medium ${isActive ? 'text-blue-100' : 'text-slate-400'}`
    }, conv.ultimo_mensaje || "Empieza a chatear..."), !isGroup && /*#__PURE__*/React.createElement("p", {
      className: "text-[10px] mt-0.5",
      id: `status-user-${conv.id_contacto}`
    }, conv.en_linea ? /*#__PURE__*/React.createElement("span", {
      className: "text-emerald-500 font-semibold flex items-center gap-1"
    }, /*#__PURE__*/React.createElement("span", {
      className: "w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block"
    }), "Activo ahora") : /*#__PURE__*/React.createElement("span", {
      className: isActive ? 'text-blue-200' : 'text-slate-400'
    }, "\xDAlt. vez ", window.formatearFechaConexionDashboard ? window.formatearFechaConexionDashboard(conv.ultima_conexion) : 'desconocida'))), !isHovered && /*#__PURE__*/React.createElement("div", {
      className: "absolute left-full ml-4 px-2 py-1.5 bg-slate-900 text-white text-xs font-bold rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-[100] shadow-2xl ring-1 ring-white/10"
    }, nombre));
  };

  // Renderizado
  const rootElement = document.getElementById("sidebar-react-root");
  if (rootElement) {
    ReactDOM.createRoot(rootElement).render(/*#__PURE__*/React.createElement(SidebarReact, null));
  }
} // fin initSidebar
