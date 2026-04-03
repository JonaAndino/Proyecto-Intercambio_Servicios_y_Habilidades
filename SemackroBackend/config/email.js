const nodemailer = require('nodemailer');

// Configuración del transporte de correo (Gmail)
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER, // Tu correo de Gmail
        pass: process.env.EMAIL_PASSWORD // Contraseña de aplicación de Gmail
    }
});

// Función para enviar correo de recuperación de contraseña
const enviarCorreoRecuperacion = async (destinatario, token) => {
    // Auto-detectar entorno: si NODE_ENV no es production, usar localhost
    const isLocal = process.env.NODE_ENV !== 'production';
    const frontendUrl = isLocal ? 'http://localhost:5050' : (process.env.FRONTEND_URL || 'https://SEMACKRO.duckdns.org');
    const enlaceRecuperacion = `${frontendUrl}/restablecer-password.html?token=${token}`;
    
    const mailOptions = {
        from: `"SEMACKRO" <${process.env.EMAIL_USER}>`,
        to: destinatario,
        subject: 'Recuperación de Contraseña - SEMACKRO',
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
                    .button {
                        display: inline-block;
                        padding: 12px 30px;
                        background-color: #4f46e5;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        margin: 20px 0;
                        font-weight: bold;
                    }
                    .button:hover {
                        background-color: #4338ca;
                    }
                    .warning {
                        background-color: #fef3c7;
                        border-left: 4px solid #f59e0b;
                        padding: 15px;
                        margin: 20px 0;
                        border-radius: 5px;
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
                        <h2>Recuperación de Contraseña</h2>
                    </div>
                    
                    <p>Hola,</p>
                    
                    <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en SEMACKRO.</p>
                    
                    <p>Si realizaste esta solicitud, haz clic en el siguiente botón para crear una nueva contraseña:</p>
                    
                    <div style="text-align: center;">
                        <a href="${enlaceRecuperacion}" style="display: inline-block; padding: 15px 40px; background-color: #4f46e5; color: #ffffff !important; text-decoration: none; border-radius: 8px; margin: 20px 0; font-weight: bold; font-size: 16px;">Restablecer Contraseña</a>
                    </div>
                    
                    <p>O copia y pega este enlace en tu navegador:</p>
                    <p style="word-break: break-all; color: #4f46e5;">${enlaceRecuperacion}</p>
                    
                    <div class="warning">
                        <strong>Importante:</strong> Este enlace expirará en <strong>15 minutos</strong> por razones de seguridad.
                    </div>
                    
                    <p>Si no solicitaste restablecer tu contraseña, puedes ignorar este correo de forma segura.</p>
                    
                    <div class="footer">
                        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                        <p>&copy; 2025 SEMACKRO. Todos los derechos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
        `
    };

    try {
        const info = await transporter.sendMail(mailOptions);
        console.log('Correo enviado:', info.messageId);
        return { success: true, messageId: info.messageId };
    } catch (error) {
        console.error('Error al enviar correo:', error);
        return { success: false, error: error.message };
    }
};

// Función para enviar notificación contextual (H8)
const enviarNotificacionContextual = async (destinatario, alertas, frontendUrl) => {
    if (!destinatario || !alertas || alertas.length === 0) return { success: false };

    // Prioridad: 1) URL enviada como parámetro  2) variable de entorno  3) localhost
    const appUrl = (frontendUrl || process.env.FRONTEND_URL || 'http://localhost:5050').replace(/\/$/, '');
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
        from: `"SEMACKRO" <${process.env.EMAIL_USER}>`,
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
        const info = await transporter.sendMail(mailOptions);
        console.log('Notificación contextual enviada:', info.messageId);
        return { success: true };
    } catch (error) {
        console.error('Error al enviar notificación contextual:', error);
        return { success: false, error: error.message };
    }
};

module.exports = { enviarCorreoRecuperacion, enviarNotificacionContextual };
