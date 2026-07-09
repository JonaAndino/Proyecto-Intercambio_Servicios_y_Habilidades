
        // SCRUM-25: Modo Minimalista para vista desde el Dashboard
        (function() {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('minimal') === 'true') {
                document.body.classList.add('mode-minimal');
                const style = document.createElement('style');
                style.innerHTML = `
                    .mode-minimal .logout-button, 
                    .mode-minimal .action-buttons,
                    .mode-minimal .tour-start-button,
                    .mode-minimal .camera-icon,
                    .mode-minimal .add-skill-button-primary,
                    .mode-minimal .add-skill-button-secondary,
                    .mode-minimal .file-upload-area {
                        display: none !important;
                    }
                    .mode-minimal .editable:hover::after {
                        display: none !important;
                    }
                    .mode-minimal .editable {
                        cursor: default !important;
                        pointer-events: none !important;
                        background: transparent !important;
                    }
                    .mode-minimal .profile-pic-container {
                        cursor: default !important;
                    }
                    .mode-minimal body {
                        padding: 10px !important;
                    }
                `;
                document.head.appendChild(style);
            }
        })();
    