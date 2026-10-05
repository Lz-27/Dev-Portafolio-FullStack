"""
utils/email.py
──────────────
Servicio de notificación por email usando aiosmtplib (async).
Se ejecuta como BackgroundTask en FastAPI para no bloquear la respuesta al cliente.
Si el email falla, solo se loggea el error — el mensaje ya fue guardado en BD.
"""
from __future__ import annotations

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


def _build_html_body(name: str, email: str, subject: str, message: str, message_id: int) -> str:
    """Construye el cuerpo HTML del email de notificación."""
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f23; color: #e2e8f0; margin: 0; padding: 20px; }}
            .card {{ background: #1a1a3e; border-radius: 12px; padding: 32px; max-width: 600px; margin: 0 auto; border: 1px solid #7c3aed; }}
            .header {{ text-align: center; margin-bottom: 24px; }}
            .badge {{ background: linear-gradient(135deg, #7c3aed, #3b82f6); color: white; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 1px; }}
            h1 {{ color: #a78bfa; font-size: 22px; margin-top: 12px; }}
            .field {{ margin-bottom: 16px; }}
            .label {{ font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
            .value {{ color: #e2e8f0; font-size: 15px; margin-top: 4px; padding: 10px 14px; background: #0f0f23; border-radius: 8px; border-left: 3px solid #7c3aed; }}
            .message-box {{ background: #0f0f23; padding: 16px; border-radius: 8px; border-left: 3px solid #3b82f6; white-space: pre-wrap; line-height: 1.6; }}
            .footer {{ text-align: center; font-size: 12px; color: #64748b; margin-top: 24px; }}
            .id-badge {{ display: inline-block; background: #1e293b; padding: 4px 12px; border-radius: 20px; font-family: monospace; color: #7c3aed; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="badge">📬 NUEVO MENSAJE</div>
                <h1>Tienes un nuevo contacto en tu portafolio</h1>
            </div>

            <div class="field">
                <div class="label">De</div>
                <div class="value">👤 {name}</div>
            </div>

            <div class="field">
                <div class="label">Email</div>
                <div class="value">📧 <a href="mailto:{email}" style="color: #7c3aed;">{email}</a></div>
            </div>

            <div class="field">
                <div class="label">Asunto</div>
                <div class="value">📌 {subject}</div>
            </div>

            <div class="field">
                <div class="label">Mensaje</div>
                <div class="message-box">{message}</div>
            </div>

            <div class="footer">
                ID del mensaje: <span class="id-badge">#{message_id}</span><br>
                Portafolio Profesional — Sistema de contacto automático
            </div>
        </div>
    </body>
    </html>
    """


async def send_contact_notification(
    name: str,
    email: str,
    subject: str,
    message: str,
    message_id: int,
) -> None:
    """
    Envía una notificación por email al propietario del portafolio
    cuando recibe un nuevo mensaje de contacto.

    Se ejecuta como BackgroundTask (async, no bloquea la respuesta HTTP).
    Los errores se loggean pero no se re-lanzan para no afectar al cliente.
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning(
            "⚠️  Email no configurado (SMTP_USER/SMTP_PASSWORD vacíos). "
            "Mensaje guardado en BD pero notificación no enviada."
        )
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[Portafolio] Nuevo mensaje de {name}: {subject}"
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = settings.EMAIL_TO
        msg["Reply-To"] = email

        # Parte HTML
        html_body = _build_html_body(name, email, subject, message, message_id)
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        # Parte texto plano (fallback)
        plain_body = (
            f"Nuevo mensaje de contacto #{message_id}\n"
            f"De: {name} <{email}>\n"
            f"Asunto: {subject}\n\n"
            f"{message}"
        )
        msg.attach(MIMEText(plain_body, "plain", "utf-8"))

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )

        logger.info(f"✅ Email de notificación enviado para mensaje #{message_id}")

    except Exception as exc:
        # Loggear pero NO re-lanzar — el mensaje ya está guardado en BD
        logger.error(f"❌ Error al enviar email para mensaje #{message_id}: {exc}")
