const nodemailer = require('nodemailer');
const https = require('https');

// Limpiar variables de entorno para evitar espacios accidentales o caracteres extraños
if (process.env.EMAIL_USER) {
    process.env.EMAIL_USER = process.env.EMAIL_USER.trim();
}
if (process.env.EMAIL_PASSWORD) {
    process.env.EMAIL_PASSWORD = process.env.EMAIL_PASSWORD.replace(/\s+/g, '');
}
if (process.env.EMAIL_FROM_ADDRESS) {
    process.env.EMAIL_FROM_ADDRESS = process.env.EMAIL_FROM_ADDRESS.trim();
}
if (process.env.EMAIL_PROVIDER) {
    process.env.EMAIL_PROVIDER = process.env.EMAIL_PROVIDER.trim();
}
if (process.env.EMAIL_HOST) {
    process.env.EMAIL_HOST = process.env.EMAIL_HOST.trim();
}
if (process.env.EMAIL_PORT) {
    process.env.EMAIL_PORT = String(process.env.EMAIL_PORT).trim();
}

const EMAIL_TIMEOUT_MS = Number(process.env.EMAIL_TIMEOUT_MS || 15000);
const EMAIL_PROVIDER = (process.env.EMAIL_PROVIDER || 'gmail').toLowerCase();
const EMAIL_FROM_NAME = process.env.EMAIL_FROM_NAME || 'SEMACKRO';
const BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email';
const EMAIL_FROM_ADDRESS = process.env.EMAIL_FROM_ADDRESS || process.env.EMAIL_USER || '';
const EMAIL_HOST_LOWER = String(process.env.EMAIL_HOST || '').toLowerCase();

let transporterInstance = null;

function maskEmail(email) {
    if (!email || typeof email !== 'string' || !email.includes('@')) return '[email-invalido]';
    const [local, domain] = email.split('@');
    const visibleLocal = local.length <= 2 ? local[0] || '*' : local.slice(0, 2);
    return `${visibleLocal}***@${domain}`;
}

function normalizeFrontendUrl(rawUrl) {
    try {
        if (!rawUrl) return null;
        const normalized = new URL(String(rawUrl));
        return normalized.origin;
    } catch (_) {
        return null;
    }
}

function isConnectionTimeoutError(error) {
    const code = String((error && error.code) || '').toUpperCase();
    const command = String((error && error.command) || '').toUpperCase();
    return code.includes('TIMEDOUT') || 
           code.includes('CONN') || 
           code === 'ENOTFOUND' || 
           code === 'EHOSTUNREACH' || 
           code === 'EADDRNOTAVAIL' || 
           code === 'EMAIL_TIMEOUT' || 
           command === 'CONN';
}

function parseFallbackPorts(defaultPort) {
    const rawFallback = process.env.EMAIL_FALLBACK_PORTS || '2525,465';
    const parsed = rawFallback
        .split(',')
        .map((p) => Number(String(p).trim()))
        .filter((p) => Number.isInteger(p) && p > 0);

    return parsed.filter((p) => p !== defaultPort);
}

function parseFromAddress(rawFrom) {
    const fromValue = String(rawFrom || '').trim();
    const match = fromValue.match(/^(?:"?([^"<>]*)"?\s*)?<([^<>]+)>$/);

    if (match) {
        const name = (match[1] || EMAIL_FROM_NAME || 'SEMACKRO').trim();
        return {
            name: name || 'SEMACKRO',
            email: match[2].trim()
        };
    }

    return {
        name: EMAIL_FROM_NAME || 'SEMACKRO',
        email: EMAIL_FROM_ADDRESS || fromValue
    };
}

function canUseBrevoHttpFallback() {
    return EMAIL_PROVIDER === 'smtp' &&
        (EMAIL_HOST_LOWER.includes('brevo') || EMAIL_HOST_LOWER.includes('sendinblue'));
}

function getBrevoApiKeyWithSource() {
    if (process.env.BREVO_API_KEY) {
        return { key: process.env.BREVO_API_KEY, source: 'BREVO_API_KEY' };
    }

    if (canUseBrevoHttpFallback() && process.env.EMAIL_PASSWORD) {
        return { key: process.env.EMAIL_PASSWORD, source: 'EMAIL_PASSWORD(smtp)' };
    }

    return { key: null, source: null };
}

const sendMailViaBrevoApi = (mailOptions, context = {}) =>
    new Promise((resolve, reject) => {
        const traceId = context.traceId || 'sin-trace';
        const destination = context.destination || maskEmail(mailOptions.to);
        const { key: apiKey, source: keySource } = getBrevoApiKeyWithSource();

        if (!apiKey) {
            const err = new Error('No hay API key para fallback HTTP de Brevo (define BREVO_API_KEY o usa SMTP Brevo con EMAIL_PASSWORD)');
            err.code = 'BREVO_API_KEY_MISSING';
            return reject(err);
        }

        const from = parseFromAddress(mailOptions.from);
        const payload = JSON.stringify({
            sender: {
                name: from.name,
                email: from.email
            },
            to: [{ email: mailOptions.to }],
            subject: mailOptions.subject,
            htmlContent: mailOptions.html
        });

        const url = new URL(BREVO_API_URL);
        const requestOptions = {
            method: 'POST',
            hostname: url.hostname,
            path: url.pathname,
            headers: {
                accept: 'application/json',
                'api-key': apiKey,
                'content-type': 'application/json',
                'content-length': Buffer.byteLength(payload)
            }
        };

        console.log(`[email:brevo-api][${traceId}] Intentando envío HTTP a ${destination} usando key=${keySource}`);

        const req = https.request(requestOptions, (res) => {
            let body = '';
            res.on('data', (chunk) => {
                body += chunk;
            });
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    let parsed;
                    try {
                        parsed = body ? JSON.parse(body) : {};
                    } catch (_) {
                        parsed = {};
                    }

                    const messageId = parsed.messageId || parsed.messageid || `brevo-http-${Date.now()}`;
                    console.log(`[email:brevo-api][${traceId}] Envío HTTP exitoso a ${destination} messageId=${messageId}`);
                    return resolve({ messageId });
                }

                const apiError = new Error(`Brevo API respondió ${res.statusCode}: ${body || 'sin detalle'}`);
                apiError.code = `BREVO_API_${res.statusCode}`;
                return reject(apiError);
            });
        });

        req.on('error', (error) => {
            const wrapped = new Error(error.message || 'Error de conexión con Brevo API');
            wrapped.code = error.code || 'BREVO_API_CONNECTION_ERROR';
            reject(wrapped);
        });

        req.setTimeout(EMAIL_TIMEOUT_MS, () => {
            const timeoutError = new Error(`Tiempo de espera excedido en Brevo API (${EMAIL_TIMEOUT_MS}ms)`);
            timeoutError.code = 'BREVO_API_TIMEOUT';
            req.destroy(timeoutError);
        });

        req.write(payload);
        req.end();
    });

function getTransportConfig() {
    if (EMAIL_PROVIDER === 'smtp') {
        const smtpPort = Number(process.env.EMAIL_PORT || 587);
        const secureByPort = smtpPort === 465;
        const secureByEnv = String(process.env.EMAIL_SECURE || '').toLowerCase() === 'true';

        return {
            host: process.env.EMAIL_HOST,
            port: smtpPort,
            secure: secureByEnv || secureByPort,
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASSWORD
            },
            connectionTimeout: EMAIL_TIMEOUT_MS,
            greetingTimeout: EMAIL_TIMEOUT_MS,
            socketTimeout: EMAIL_TIMEOUT_MS
        };
    }

    // Para gmail, usar smtp.gmail.com con TLS directo (puerto 465) es mucho más robusto en Railway y entornos cloud.
    return {
        host: 'smtp.gmail.com',
        port: 465,
        secure: true,
        auth: {
            user: process.env.EMAIL_USER,
            pass: process.env.EMAIL_PASSWORD
        },
        connectionTimeout: EMAIL_TIMEOUT_MS,
        greetingTimeout: EMAIL_TIMEOUT_MS,
        socketTimeout: EMAIL_TIMEOUT_MS
    };
}

function getTransporter() {
    if (transporterInstance) return transporterInstance;
    const transportConfig = getTransportConfig();
    transporterInstance = nodemailer.createTransport(transportConfig);

    const descriptor = EMAIL_PROVIDER === 'smtp'
        ? `host=${transportConfig.host || 'no-definido'} port=${transportConfig.port} secure=${transportConfig.secure}`
        : `host=smtp.gmail.com port=465 secure=true`;

    console.log(`[email:${EMAIL_PROVIDER}] Transporte inicializado (${descriptor}) user=${maskEmail(process.env.EMAIL_USER)}`);
    return transporterInstance;
}

function getEmailConfigError() {
    if (EMAIL_PROVIDER === 'brevo-api') {
        const { key: apiKey } = getBrevoApiKeyWithSource();
        if (!apiKey) {
            return 'No hay API key para EMAIL_PROVIDER=brevo-api (define BREVO_API_KEY)';
        }

        if (!EMAIL_FROM_ADDRESS) {
            return 'EMAIL_FROM_ADDRESS o EMAIL_USER no configurada para EMAIL_PROVIDER=brevo-api';
        }

        return null;
    }

    if (!process.env.EMAIL_USER || !process.env.EMAIL_PASSWORD) {
        return 'Variables EMAIL_USER/EMAIL_PASSWORD no configuradas';
    }

    if (EMAIL_PROVIDER === 'smtp' && !process.env.EMAIL_HOST) {
        return 'EMAIL_HOST no configurado para EMAIL_PROVIDER=smtp';
    }

    return null;
}

const sendMailWithTimeout = (mailOptions, timeoutMs = EMAIL_TIMEOUT_MS, context = {}) =>
    new Promise((resolve, reject) => {
        const startedAt = Date.now();
        const traceId = context.traceId || 'sin-trace';
        const destination = context.destination || maskEmail(mailOptions.to);

        console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Iniciando envío a ${destination} con timeout=${timeoutMs}ms`);

        const timer = setTimeout(() => {
            const timeoutError = new Error(`Tiempo de espera excedido al enviar correo (${timeoutMs}ms)`);
            timeoutError.code = 'EMAIL_TIMEOUT';
            reject(timeoutError);
        }, timeoutMs);

        getTransporter()
            .sendMail(mailOptions)
            .then((info) => {
                clearTimeout(timer);
                console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Envío exitoso a ${destination} en ${Date.now() - startedAt}ms messageId=${info.messageId || 'n/a'}`);
                resolve(info);
            })
            .catch((error) => {
                clearTimeout(timer);
                const errorCode = error && (error.code || error.responseCode || error.command || 'UNKNOWN_ERROR');
                console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Error enviando a ${destination} en ${Date.now() - startedAt}ms code=${errorCode}`, {
                    message: error && error.message,
                    responseCode: error && error.responseCode,
                    command: error && error.command
                });
                reject(error);
            });
    });

const sendMailWithTransportConfig = (mailOptions, transportConfig, timeoutMs = EMAIL_TIMEOUT_MS, context = {}) =>
    new Promise((resolve, reject) => {
        const startedAt = Date.now();
        const traceId = context.traceId || 'sin-trace';
        const destination = context.destination || maskEmail(mailOptions.to);
        const attemptedPort = transportConfig.port || 'n/a';

        console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Reintento por puerto ${attemptedPort} a ${destination} con timeout=${timeoutMs}ms`);

        const timer = setTimeout(() => {
            const timeoutError = new Error(`Tiempo de espera excedido al enviar correo (${timeoutMs}ms)`);
            timeoutError.code = 'EMAIL_TIMEOUT';
            reject(timeoutError);
        }, timeoutMs);

        const tempTransporter = nodemailer.createTransport(transportConfig);
        tempTransporter
            .sendMail(mailOptions)
            .then((info) => {
                clearTimeout(timer);
                console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Reintento exitoso por puerto ${attemptedPort} en ${Date.now() - startedAt}ms messageId=${info.messageId || 'n/a'}`);
                resolve(info);
            })
            .catch((error) => {
                clearTimeout(timer);
                const errorCode = error && (error.code || error.responseCode || error.command || 'UNKNOWN_ERROR');
                console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Reintento falló por puerto ${attemptedPort} en ${Date.now() - startedAt}ms code=${errorCode}`, {
                    message: error && error.message,
                    responseCode: error && error.responseCode,
                    command: error && error.command
                });
                reject(error);
            });
    });

// Función para enviar correo de recuperación de contraseña
const enviarCorreoRecuperacion = async (destinatario, token, options = {}) => {
    const cleanDestinatario = String(destinatario || '').trim();
    const traceId = options.traceId || 'sin-trace';
    const destinatarioMask = maskEmail(cleanDestinatario);

    console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Preparando correo de recuperación para ${destinatarioMask}`);

    const configError = getEmailConfigError();
    if (configError) {
        console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Configuración inválida: ${configError}`);
        return { success: false, error: configError };
    }

    const frontendUrl =
        normalizeFrontendUrl(options.frontendUrl) ||
        normalizeFrontendUrl(process.env.FRONTEND_URL) ||
        'https://semackro.vercel.app';

    const fromName = String(options.emailFromName || EMAIL_FROM_NAME || 'SEMACKRO').trim().slice(0, 80) || 'SEMACKRO';
    const enlaceRecuperacion = `${frontendUrl}/restablecer-password.html?token=${token}`;
    console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Enlace de recuperación generado con frontend=${frontendUrl}`);

    const formatDuration = (seconds) => {
        if (!seconds) return "24 horas (1 día)";
        const secs = Number(seconds);
        if (secs < 60) return `${secs} segundos`;
        if (secs < 3600) return `${Math.round(secs / 60)} minutos`;
        const hours = Math.round(secs / 3600);
        if (hours === 1) return "1 hora";
        if (hours < 24) return `${hours} horas`;
        const days = Math.round(hours / 24);
        if (days === 1) return "24 horas (1 día)";
        return `${hours} horas (${days} días)`;
    };
    const duracionTexto = formatDuration(options.tokenDuration);
    
    const mailOptions = {
        from: `"${fromName}" <${EMAIL_FROM_ADDRESS}>`,
        to: cleanDestinatario,
        subject: 'Recuperación de Contraseña - SEMACKRO',
        html: `
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f3f4f6; -webkit-font-smoothing: antialiased;">
                <!-- Contenedor principal con padding -->
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f3f4f6; padding: 40px 20px;">
                    <tr>
                        <td align="center">
                            <!-- Tarjeta blanca central -->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                                <!-- Header con banda de color azul corporativo -->
                                <tr>
                                    <td align="center" style="background-color: #2563EB; padding: 40px 20px;">
                                        <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 800; letter-spacing: 2px;">SEMACKRO</h1>
                                        <p style="color: #bfdbfe; margin: 10px 0 0 0; font-size: 16px; font-weight: 500;">Recuperación de Contraseña</p>
                                    </td>
                                </tr>
                                
                                <!-- Cuerpo del mensaje -->
                                <tr>
                                    <td style="padding: 40px 40px 20px 40px; color: #374151; font-size: 16px; line-height: 1.6;">
                                        <p style="margin: 0 0 20px 0;">Hola,</p>
                                        
                                        <p style="margin: 0 0 20px 0;">Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en <strong>SEMACKRO</strong> asociada al siguiente usuario:</p>
                                        
                                        <!-- Caja destacada para el correo -->
                                        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 25px;">
                                            <span style="font-size: 14px; color: #64748b; display: block; margin-bottom: 5px;">Tu usuario (correo electrónico)</span>
                                            <strong style="font-size: 18px; color: #1e293b;">${cleanDestinatario}</strong>
                                        </div>
                                        
                                        <p style="margin: 0 0 25px 0;">Para continuar y crear tu nueva contraseña, haz clic en el botón de abajo. Este enlace es único y seguro.</p>
                                        
                                        <!-- Botón CTA -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td align="center" style="padding-bottom: 30px;">
                                                    <a href="${enlaceRecuperacion}" style="display: inline-block; padding: 16px 36px; background-color: #2563EB; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; text-align: center;">
                                                        Restablecer mi contraseña
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <p style="margin: 0 0 15px 0; font-size: 14px; color: #64748b;">Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:</p>
                                        <p style="margin: 0 0 30px 0; font-size: 13px; color: #2563EB; word-break: break-all;">
                                            <a href="${enlaceRecuperacion}" style="color: #2563EB; text-decoration: underline;">${enlaceRecuperacion}</a>
                                        </p>
                                        
                                        <!-- Advertencia de expiración -->
                                        <div style="background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 16px; border-radius: 0 8px 8px 0; margin-bottom: 20px;">
                                            <p style="margin: 0; color: #b45309; font-size: 14px;">
                                                <strong>Importante:</strong> Por razones de seguridad, este enlace expirará en <strong>${duracionTexto}</strong>.
                                            </p>
                                        </div>
                                        
                                        <p style="margin: 0; font-size: 14px; color: #94a3b8;">Si no solicitaste este cambio, puedes ignorar este correo de forma segura. Tu cuenta seguirá protegida.</p>
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td align="center" style="background-color: #f8fafc; padding: 25px 40px; border-top: 1px solid #e2e8f0;">
                                        <p style="margin: 0 0 10px 0; font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;">SEMACKRO</p>
                                        <p style="margin: 0; font-size: 12px; color: #94a3b8;">Este es un mensaje automático, por favor no respondas a esta dirección de correo.</p>
                                        <p style="margin: 10px 0 0 0; font-size: 12px; color: #94a3b8;">&copy; 2025 SEMACKRO. Todos los derechos reservados.</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
        `
    };

    if (EMAIL_PROVIDER === 'brevo-api') {
        try {
            const apiInfo = await sendMailViaBrevoApi(mailOptions, {
                traceId,
                destination: destinatarioMask
            });
            return { success: true, messageId: apiInfo.messageId, channel: 'brevo-api' };
        } catch (apiError) {
            console.error(`[email:brevo-api][${traceId}] Error al enviar correo de recuperación para ${destinatarioMask}:`, {
                message: apiError && apiError.message,
                code: apiError && apiError.code
            });
            return { success: false, error: apiError.message };
        }
    }

    try {
        const info = await sendMailWithTimeout(mailOptions, EMAIL_TIMEOUT_MS, {
            traceId,
            destination: destinatarioMask
        });
        console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Correo de recuperación confirmado para ${destinatarioMask} messageId=${info.messageId || 'n/a'}`);
        return { success: true, messageId: info.messageId };
    } catch (error) {
        console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Error al enviar correo de recuperación para ${destinatarioMask}:`, {
            message: error && error.message,
            code: error && (error.code || error.responseCode || error.command || 'UNKNOWN_ERROR')
        });

        // Fallback robusto si la conexión falla/tiempos de espera excedidos (especialmente común en Railway y hosting cloud)
        if (isConnectionTimeoutError(error)) {
            // Caso 1: Si es Gmail (o por defecto), intentamos alternar de puerto 465 (SSL) a puerto 587 (TLS)
            if (EMAIL_PROVIDER === 'gmail') {
                try {
                    const fallbackConfig = {
                        host: 'smtp.gmail.com',
                        port: 587,
                        secure: false, // TLS
                        auth: {
                            user: process.env.EMAIL_USER,
                            pass: process.env.EMAIL_PASSWORD
                        },
                        connectionTimeout: EMAIL_TIMEOUT_MS,
                        greetingTimeout: EMAIL_TIMEOUT_MS,
                        socketTimeout: EMAIL_TIMEOUT_MS
                    };

                    const fallbackInfo = await sendMailWithTransportConfig(
                        mailOptions,
                        fallbackConfig,
                        EMAIL_TIMEOUT_MS,
                        {
                            traceId: `${traceId}-p587`,
                            destination: destinatarioMask
                        }
                    );

                    return {
                        success: true,
                        messageId: fallbackInfo.messageId,
                        fallbackPort: 587
                    };
                } catch (fallbackError) {
                    console.error(`[email:gmail][${traceId}] Fallback de puerto 587 también falló para ${destinatarioMask}`);
                }
            }

            // Caso 2: Si es SMTP genérico, intentar los puertos de fallback configurados
            if (EMAIL_PROVIDER === 'smtp') {
                const defaultPort = Number(process.env.EMAIL_PORT || 587);
                const fallbackPorts = parseFallbackPorts(defaultPort);

                for (const fallbackPort of fallbackPorts) {
                    try {
                        const fallbackConfig = {
                            host: process.env.EMAIL_HOST,
                            port: fallbackPort,
                            secure: fallbackPort === 465,
                            auth: {
                                user: process.env.EMAIL_USER,
                                pass: process.env.EMAIL_PASSWORD
                            },
                            connectionTimeout: EMAIL_TIMEOUT_MS,
                            greetingTimeout: EMAIL_TIMEOUT_MS,
                            socketTimeout: EMAIL_TIMEOUT_MS
                        };

                        const fallbackInfo = await sendMailWithTransportConfig(
                            mailOptions,
                            fallbackConfig,
                            EMAIL_TIMEOUT_MS,
                            {
                                traceId: `${traceId}-p${fallbackPort}`,
                                destination: destinatarioMask
                            }
                        );

                        return {
                            success: true,
                            messageId: fallbackInfo.messageId,
                            fallbackPort
                        };
                    } catch (_) {
                        // El detalle del error ya se registra en sendMailWithTransportConfig.
                    }
                }
            }

            // Caso 3: Fallback HTTP con la API de Brevo si está disponible
            if (process.env.BREVO_API_KEY || canUseBrevoHttpFallback()) {
                try {
                    const apiInfo = await sendMailViaBrevoApi(mailOptions, {
                        traceId: `${traceId}-brevo-api`,
                        destination: destinatarioMask
                    });

                    return {
                        success: true,
                        messageId: apiInfo.messageId,
                        channel: 'brevo-api'
                    };
                } catch (apiError) {
                    console.error(`[email:brevo-api][${traceId}] Fallback HTTP también falló para ${destinatarioMask}:`, {
                        message: apiError && apiError.message,
                        code: apiError && apiError.code
                    });
                }
            } else {
                console.warn(`[email:brevo-api][${traceId}] Se omite fallback HTTP: no hay BREVO_API_KEY y el host SMTP no parece ser Brevo.`);
            }
        }

        return { success: false, error: error.message };
    }
};

// Función para enviar notificación contextual (H8)
const enviarNotificacionContextual = async (destinatario, alertas, frontendUrl) => {
    if (!destinatario || !alertas || alertas.length === 0) return { success: false };
    const configError = getEmailConfigError();
    if (configError) {
        return { success: false, error: configError };
    }

    // Prioridad: 1) URL enviada como parámetro  2) variable de entorno  3) localhost
    const appUrl = (frontendUrl || process.env.FRONTEND_URL || 'https://semackro.vercel.app').replace(/\/$/, '');
    const urlDestino = `${appUrl}/Descubrir.html`;

    const filasHtml = alertas.map(a => {
        const COLORES = {
            alerta:       { fondo: '#eff6ff', borde: '#bfdbfe', etiqueta: '#1d4ed8', texto: 'Alerta' },
            exito:        { fondo: '#f0fdf4', borde: '#bbf7d0', etiqueta: '#15803d', texto: 'Completado' },
            recordatorio: { fondo: '#fffbeb', borde: '#fde68a', etiqueta: '#92400e', texto: 'Recordatorio' },
            critico:      { fondo: '#fef2f2', borde: '#fecaca', etiqueta: '#991b1b', texto: 'Instrucción Crítica' },
        };
        const c = COLORES[a.tipo] || COLORES.alerta;
        return `
        <div style="margin-bottom:12px;padding:14px 16px;border-radius:10px;background:${c.fondo};border:1px solid ${c.borde};">
            <span style="display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:700;color:${c.etiqueta};background:#fff;margin-bottom:6px;">${c.texto}</span>
            ${a.orden ? `<span style="font-size:11px;color:#6b7280;margin-left:6px;">${a.orden}</span>` : ''}
            <div style="font-size:15px;font-weight:600;color:#111827;margin-top:4px;">${a.titulo}</div>
            ${a.detalle ? `<div style="font-size:13px;color:#6b7280;margin-top:3px;">${a.detalle}</div>` : ''}
        </div>`;
    }).join('');

    const mailOptions = {
        from: `"${EMAIL_FROM_NAME}" <${process.env.EMAIL_USER}>`,
        to: destinatario,
        subject: `${alertas.length} alerta${alertas.length > 1 ? 's' : ''} nueva${alertas.length > 1 ? 's' : ''} en SEMACKRO`,
        html: `
        <!DOCTYPE html>
        <html><head><meta charset="UTF-8"></head>
        <body style="font-family:Arial,sans-serif;background:#f9fafb;padding:24px;margin:0;">
            <div style="max-width:580px;margin:0 auto;background:#fff;border-radius:14px;box-shadow:0 2px 10px rgba(0,0,0,.07);padding:32px;">
                <div style="text-align:center;margin-bottom:24px;">
                    <h1 style="color:#4f46e5;margin:0 0 4px;">SEMACKRO</h1>
                    <p style="color:#6b7280;margin:0;font-size:14px;">Tienes ${alertas.length} alerta${alertas.length>1?'s':''} pendiente${alertas.length>1?'s':''}</p>
                </div>
                ${filasHtml}
                <div style="margin-top:24px;text-align:center;">
                    <a href="${urlDestino}"
                       style="display:inline-block;padding:12px 32px;background:#4f46e5;color:#fff;text-decoration:none;border-radius:8px;font-weight:700;font-size:15px;">Ver en SEMACKRO</a>
                </div>
                <div style="margin-top:24px;border-top:1px solid #e5e7eb;padding-top:16px;text-align:center;font-size:11px;color:#9ca3af;">
                    Correo automático — no respondas a este mensaje. &copy; 2025 SEMACKRO
                </div>
            </div>
        </body></html>`
    };

    try {
        const info = await sendMailWithTimeout(mailOptions);
        console.log('Notificación contextual enviada:', info.messageId);
        return { success: true };
    } catch (error) {
        console.error(`[email:${EMAIL_PROVIDER}] Error al enviar notificación contextual:`, error);
        return { success: false, error: error.message };
    }
};


const enviarCorreoUsuarioRecuperado = async (destinatario, nombrePersona, correoUsuario, options = {}) => {
    const cleanDestinatario = String(destinatario || '').trim();
    const cleanCorreoUsuario = String(correoUsuario || '').trim();
    const traceId = options.traceId || 'sin-trace';
    const destinatarioMask = maskEmail(cleanDestinatario);

    console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Preparando correo de recuperación de usuario para ${destinatarioMask}`);

    const configError = getEmailConfigError();
    if (configError) {
        console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Configuración inválida: ${configError}`);
        return { success: false, error: configError };
    }

    const frontendUrl =
        normalizeFrontendUrl(options.frontendUrl) ||
        normalizeFrontendUrl(process.env.FRONTEND_URL) ||
        'https://semackro.vercel.app';

    const fromName = String(options.emailFromName || EMAIL_FROM_NAME || 'SEMACKRO').trim().slice(0, 80) || 'SEMACKRO';
    const enlaceLogin = `${frontendUrl}/login.html`;
    
    const mailOptions = {
        from: `"${fromName}" <${EMAIL_FROM_ADDRESS}>`,
        to: cleanDestinatario,
        subject: 'Recuperación de Usuario - SEMACKRO',
        html: `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .container {
                        background-color: #f9f9f9;
                        border-radius: 10px;
                        padding: 30px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }
                    .header {
                        text-align: center;
                        color: #4f46e5;
                        margin-bottom: 30px;
                    }
                    .info-box {
                        background-color: #eff6ff;
                        border-left: 4px solid #3b82f6;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
                    }
                    .button {
                        display: inline-block;
                        padding: 12px 30px;
                        background-color: #4f46e5;
                        color: white !important;
                        text-decoration: none;
                        border-radius: 5px;
                        margin: 20px 0;
                        font-weight: bold;
                    }
                    .button:hover {
                        background-color: #4338ca;
                    }
                    .footer {
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #ddd;
                        font-size: 12px;
                        color: #666;
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>SEMACKRO</h1>
                        <h2>Recuperación de Usuario</h2>
                    </div>
                    
                    <p>Hola <strong>${nombrePersona}</strong>,</p>
                    
                    <p>Hemos procesado tu solicitud de recuperación de usuario en SEMACKRO.</p>
                    
                    <p>Los datos asociados a tu número de identidad son los siguientes:</p>
                    
                    <div class="info-box">
                        <p style="margin: 0 0 10px 0; font-size: 16px;"><strong>Usuario / Correo electrónico registrado:</strong></p>
                        <p style="margin: 0; font-size: 20px; font-weight: bold; color: #1e3a8a; word-break: break-all;">${correoUsuario}</p>
                    </div>
                    
                    <p>Este correo electrónico es tu <strong>nombre de usuario</strong> para acceder a la plataforma. Puedes utilizarlo junto con tu contraseña para iniciar sesión.</p>
                    
                    <div style="text-align: center;">
                        <a href="${enlaceLogin}" class="button">Iniciar Sesión</a>
                    </div>
                    
                    <div class="footer">
                        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                        <p>&copy; 2025 SEMACKRO. Todos los derechos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
        `
    };

    if (EMAIL_PROVIDER === 'brevo-api') {
        try {
            const apiInfo = await sendMailViaBrevoApi(mailOptions, {
                traceId,
                destination: destinatarioMask
            });
            return { success: true, messageId: apiInfo.messageId, channel: 'brevo-api' };
        } catch (apiError) {
            console.error(`[email:brevo-api][${traceId}] Error al enviar correo de recuperación de usuario para ${destinatarioMask}:`, apiError);
            return { success: false, error: apiError.message };
        }
    }

    try {
        const info = await sendMailWithTimeout(mailOptions, EMAIL_TIMEOUT_MS, {
            traceId,
            destination: destinatarioMask
        });
        console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Correo de recuperación de usuario enviado para ${destinatarioMask} messageId=${info.messageId || 'n/a'}`);
        return { success: true, messageId: info.messageId };
    } catch (error) {
        console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Error al enviar correo de recuperación de usuario para ${destinatarioMask}:`, error);

        if (isConnectionTimeoutError(error)) {
            if (EMAIL_PROVIDER === 'gmail') {
                try {
                    const fallbackConfig = {
                        host: 'smtp.gmail.com',
                        port: 587,
                        secure: false,
                        auth: { user: process.env.EMAIL_USER, pass: process.env.EMAIL_PASSWORD },
                        connectionTimeout: EMAIL_TIMEOUT_MS,
                        greetingTimeout: EMAIL_TIMEOUT_MS,
                        socketTimeout: EMAIL_TIMEOUT_MS
                    };
                    const fallbackInfo = await sendMailWithTransportConfig(mailOptions, fallbackConfig, EMAIL_TIMEOUT_MS, {
                        traceId: `${traceId}-p587`,
                        destination: destinatarioMask
                    });
                    return { success: true, messageId: fallbackInfo.messageId, fallbackPort: 587 };
                } catch (fallbackError) {
                    console.error(`[email:gmail][${traceId}] Fallback 587 también falló para ${destinatarioMask}`);
                }
            }
            if (EMAIL_PROVIDER === 'smtp') {
                const defaultPort = Number(process.env.EMAIL_PORT || 587);
                const fallbackPorts = parseFallbackPorts(defaultPort);
                for (const fallbackPort of fallbackPorts) {
                    try {
                        const fallbackConfig = {
                            host: process.env.EMAIL_HOST,
                            port: fallbackPort,
                            secure: fallbackPort === 465,
                            auth: { user: process.env.EMAIL_USER, pass: process.env.EMAIL_PASSWORD },
                            connectionTimeout: EMAIL_TIMEOUT_MS,
                            greetingTimeout: EMAIL_TIMEOUT_MS,
                            socketTimeout: EMAIL_TIMEOUT_MS
                        };
                        const fallbackInfo = await sendMailWithTransportConfig(mailOptions, fallbackConfig, EMAIL_TIMEOUT_MS, {
                            traceId: `${traceId}-p${fallbackPort}`,
                            destination: destinatarioMask
                        });
                        return { success: true, messageId: fallbackInfo.messageId, fallbackPort };
                    } catch (_) {}
                }
            }
            if (process.env.BREVO_API_KEY || canUseBrevoHttpFallback()) {
                try {
                    const apiInfo = await sendMailViaBrevoApi(mailOptions, {
                        traceId: `${traceId}-brevo-api`,
                        destination: destinatarioMask
                    });
                    return { success: true, messageId: apiInfo.messageId, channel: 'brevo-api' };
                } catch (apiError) {
                    console.error(`[email:brevo-api][${traceId}] Fallback HTTP también falló para ${destinatarioMask}:`, apiError);
                }
            }
        }

        return { success: false, error: error.message };
    }
};

const enviarCorreoBloqueo = async (destinatario, nombrePersona, motivoBloqueo, options = {}) => {
    const cleanDestinatario = String(destinatario || '').trim();
    const traceId = options.traceId || 'sin-trace';
    const destinatarioMask = maskEmail(cleanDestinatario);

    console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Preparando correo de bloqueo de usuario para ${destinatarioMask}`);

    const configError = getEmailConfigError();
    if (configError) {
        console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Configuración inválida: ${configError}`);
        return { success: false, error: configError };
    }

    const frontendUrl =
        normalizeFrontendUrl(options.frontendUrl) ||
        normalizeFrontendUrl(process.env.FRONTEND_URL) ||
        'https://semackro.vercel.app';

    const fromName = String(options.emailFromName || EMAIL_FROM_NAME || 'SEMACKRO').trim().slice(0, 80) || 'SEMACKRO';
    
    const mailOptions = {
        from: `"${fromName}" <${EMAIL_FROM_ADDRESS}>`,
        to: cleanDestinatario,
        subject: 'Tu cuenta ha sido bloqueada - SEMACKRO',
        html: `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .container {
                        background-color: #f9f9f9;
                        border-radius: 10px;
                        padding: 30px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }
                    .header {
                        text-align: center;
                        color: #dc2626;
                        margin-bottom: 30px;
                    }
                    .info-box {
                        background-color: #fef2f2;
                        border-left: 4px solid #ef4444;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
                    }
                    .footer {
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #ddd;
                        font-size: 12px;
                        color: #666;
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>SEMACKRO</h1>
                        <h2>Notificación de Cuenta Bloqueada</h2>
                    </div>
                    
                    <p>Hola <strong>${nombrePersona}</strong>,</p>
                    
                    <p>Te informamos que tu cuenta en SEMACKRO ha sido restringida/bloqueada por el administrador del sistema.</p>
                    
                    <div class="info-box">
                        <p style="margin: 0 0 10px 0; font-size: 16px;"><strong>Motivo del bloqueo:</strong></p>
                        <p style="margin: 0; font-size: 18px; font-weight: bold; color: #dc2626; word-break: break-word;">${motivoBloqueo}</p>
                    </div>
                    
                    <p>Si crees que esto se trata de un error o deseas apelar la decisión, ponte en contacto con nuestro equipo de soporte respondiendo directamente a este correo.</p>
                    
                    <div class="footer">
                        <p>Este es un correo automático, por favor no respondas a este mensaje si no es necesario.</p>
                        <p>&copy; 2025 SEMACKRO. Todos los derechos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
        `
    };

    if (EMAIL_PROVIDER === 'brevo-api') {
        try {
            const apiInfo = await sendMailViaBrevoApi(mailOptions, {
                traceId,
                destination: destinatarioMask
            });
            return { success: true, messageId: apiInfo.messageId, channel: 'brevo-api' };
        } catch (apiError) {
            console.error(`[email:brevo-api][${traceId}] Error al enviar correo de bloqueo de usuario para ${destinatarioMask}:`, apiError);
            return { success: false, error: apiError.message };
        }
    }

    try {
        const info = await sendMailWithTimeout(mailOptions, EMAIL_TIMEOUT_MS, {
            traceId,
            destination: destinatarioMask
        });
        console.log(`[email:${EMAIL_PROVIDER}][${traceId}] Correo de bloqueo de usuario enviado para ${destinatarioMask} messageId=${info.messageId || 'n/a'}`);
        return { success: true, messageId: info.messageId };
    } catch (error) {
        console.error(`[email:${EMAIL_PROVIDER}][${traceId}] Error al enviar correo de bloqueo de usuario para ${destinatarioMask}:`, error);

        if (isConnectionTimeoutError(error)) {
            if (EMAIL_PROVIDER === 'gmail') {
                try {
                    const fallbackConfig = {
                        host: 'smtp.gmail.com',
                        port: 587,
                        secure: false,
                        auth: { user: process.env.EMAIL_USER, pass: process.env.EMAIL_PASSWORD },
                        connectionTimeout: EMAIL_TIMEOUT_MS,
                        greetingTimeout: EMAIL_TIMEOUT_MS,
                        socketTimeout: EMAIL_TIMEOUT_MS
                    };
                    const fallbackInfo = await sendMailWithTransportConfig(mailOptions, fallbackConfig, EMAIL_TIMEOUT_MS, {
                        traceId: `${traceId}-p587`,
                        destination: destinatarioMask
                    });
                    return { success: true, messageId: fallbackInfo.messageId, fallbackPort: 587 };
                } catch (fallbackError) {
                    console.error(`[email:gmail][${traceId}] Fallback 587 también falló para ${destinatarioMask}`);
                }
            }
        }

        return { success: false, error: error.message };
    }
};

module.exports = { enviarCorreoRecuperacion, enviarNotificacionContextual, enviarCorreoUsuarioRecuperado, enviarCorreoBloqueo };
