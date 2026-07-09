
                        document.addEventListener('DOMContentLoaded', function () {
                            const idCardInput = document.getElementById('idCardInput');
                            const idCardUploadArea = document.getElementById('idCardUploadArea');
                            const idCardPlaceholder = document.getElementById('idCardPlaceholder');
                            const idCardPreview = document.getElementById('idCardPreview');
                            const idCardImage = document.getElementById('idCardImage');
                            const removeIdCard = document.getElementById('removeIdCard');

                            // Highlight drop area on drag
                            ['dragenter', 'dragover'].forEach(eventName => {
                                idCardUploadArea.addEventListener(eventName, (e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    idCardUploadArea.style.borderColor = '#2563eb';
                                    idCardUploadArea.style.backgroundColor = '#eff6ff';
                                }, false);
                            });

                            ['dragleave', 'drop'].forEach(eventName => {
                                idCardUploadArea.addEventListener(eventName, (e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    idCardUploadArea.style.borderColor = '#d1d5db';
                                    idCardUploadArea.style.backgroundColor = '#f9fafb';
                                }, false);
                            });

                            // Handle file input change
                            idCardInput.addEventListener('change', function (e) {
                                handleFiles(this.files);
                            });

                            // Handle file drop
                            idCardUploadArea.addEventListener('drop', function (e) {
                                const dt = e.dataTransfer;
                                const files = dt.files;
                                handleFiles(files);

                                // Update input files (optional/hacky but good for consistency)
                                if (files.length > 0) {
                                    idCardInput.files = files;
                                }
                            });

                            function handleFiles(files) {
                                if (files && files[0]) {
                                    const file = files[0];
                                    if (!file.type.startsWith('image/')) {
                                        alert('Por favor selecciona un archivo de imagen válido.');
                                        return;
                                    }

                                    // Mostrar estado de carga
                                    idCardPlaceholder.style.display = 'none';
                                    idCardPreview.style.display = 'none';

                                    // Crear elemento de carga si no existe
                                    let loadingEl = idCardUploadArea.querySelector('.upload-loading');
                                    if (!loadingEl) {
                                        loadingEl = document.createElement('div');
                                        loadingEl.className = 'upload-loading';
                                        loadingEl.innerHTML = `
                                                <div class="spinner" style="border: 4px solid rgba(0, 0, 0, 0.1); width: 36px; height: 36px; border-radius: 50%; border-left-color: #2563eb; animation: spin 1s linear infinite; margin: 0 auto 12px;"></div>
                                                <p style="font-size: 14px; color: #4b5563;">Subiendo a cloudflare...</p>
                                                <style>@keyframes spin { to { transform: rotate(360deg); } }</style>
                                            `;
                                        idCardUploadArea.appendChild(loadingEl);
                                    } else {
                                        loadingEl.style.display = 'block';
                                    }

                                    const formData = new FormData();
                                    formData.append('image', file);

                                    // Subir a Cloudflare
                                    fetch(`${API_BASE}/upload`, {
                                        method: 'POST',
                                        body: formData
                                    })
                                        .then(res => res.json())
                                        .then(result => {
                                            loadingEl.style.display = 'none';
                                            if (result.success) {
                                                console.log('ID Card subida a Cloudflare:', result.url);
                                                idCardImage.src = result.url;
                                                idCardPreview.style.display = 'block';
                                                // Guardar la URL en un atributo para uso posterior
                                                idCardUploadArea.setAttribute('data-cloudflare-url', result.url);

                                                // Persistir en la base de datos automáticamente
                                                if (typeof updateUsuario === 'function') {
                                                    updateUsuario('url_Dni', result.url);
                                                }

                                                // Mostrar mensaje de éxito temporal
                                                const successMsg = document.createElement('p');
                                                successMsg.style.color = '#059669';
                                                successMsg.style.fontSize = '12px';
                                                successMsg.style.marginTop = '8px';
                                                successMsg.textContent = '¡Subido correctamente!';
                                                idCardPreview.appendChild(successMsg);
                                                setTimeout(() => successMsg.remove(), 3000);
                                            } else {
                                                throw new Error(result.error || 'Error al subir');
                                            }
                                        })
                                        .catch(err => {
                                            console.error('Error subiendo ID Card:', err);
                                            loadingEl.style.display = 'none';
                                            idCardPlaceholder.style.display = 'block';
                                            alert('Error al subir la imagen a Cloudflare. Por favor intenta de nuevo.');
                                        });
                                }
                            }

                            // Remove image
                            removeIdCard.addEventListener('click', function (e) {
                                e.preventDefault();
                                e.stopPropagation();

                                const currentUrl = idCardUploadArea.getAttribute('data-cloudflare-url');
                                if (currentUrl && currentUrl.includes('r2.dev')) {
                                    // Opcional: Eliminar de Cloudflare también
                                    fetch(`${API_BASE}/upload`, {
                                        method: 'DELETE',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify({ imageUrl: currentUrl })
                                    }).catch(err => console.error('Error al eliminar de R2:', err));
                                }

                                idCardInput.value = '';
                                idCardImage.src = '';
                                idCardPreview.style.display = 'none';
                                idCardPlaceholder.style.display = 'block';
                                idCardUploadArea.removeAttribute('data-cloudflare-url');
                            });
                        });
                    