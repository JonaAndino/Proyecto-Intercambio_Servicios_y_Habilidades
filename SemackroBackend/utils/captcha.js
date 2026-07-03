const HCAPTCHA_VERIFY_URL = 'https://api.hcaptcha.com/siteverify';

function obtenerCaptchaSiteKey() {
    return process.env.HCAPTCHA_SITE_KEY || '';
}

async function verificarCaptcha(token, remoteIp) {
    if (!token) {
        return {
            valid: false,
            error: 'Debes completar la verificación anti-bots antes de continuar.'
        };
    }

    const secret = process.env.HCAPTCHA_SECRET_KEY || '';
    if (!secret) {
        return {
            valid: false,
            error: 'El captcha no está configurado en el servidor.'
        };
    }

    const body = new URLSearchParams();
    body.append('secret', secret);
    body.append('response', token);
    if (remoteIp) {
        body.append('remoteip', remoteIp);
    }

    try {
        const response = await fetch(HCAPTCHA_VERIFY_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: body.toString()
        });

        const data = await response.json();

        if (!data.success) {
            return {
                valid: false,
                error: 'No fue posible validar la verificación anti-bots.'
            };
        }

        return { valid: true };
    } catch (error) {
        console.error('Error verificando hCaptcha:', error);
        return {
            valid: false,
            error: 'No se pudo validar la verificación anti-bots.'
        };
    }
}

module.exports = {
    obtenerCaptchaSiteKey,
    verificarCaptcha
};