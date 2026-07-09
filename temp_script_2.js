
        (function () {
            function applyProfileTheme(theme) {
                const isDark = theme === 'dark';
                document.documentElement.classList.toggle('dark', isDark);
                if (typeof renderPixelChart === 'function') {
                    renderPixelChart();
                }
            }

            applyProfileTheme(localStorage.getItem('theme'));

            window.addEventListener('message', (event) => {
                if (event.data && event.data.type === 'toggle-theme') {
                    applyProfileTheme(event.data.theme);
                }
            });

            window.addEventListener('storage', (event) => {
                if (event.key === 'theme') {
                    applyProfileTheme(event.newValue);
                }
            });
        })();
    