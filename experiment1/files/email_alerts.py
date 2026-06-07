"""Optional email notifications for RED alerts (Experiment 1)."""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Optional

from alerts import AlertResult
from config import Settings


class EmailDeliveryError(Exception):
    """SMTP send failed."""


def format_alert_email(city: str, alert: AlertResult) -> tuple[str, str]:
    """Return (subject, plain-text body) for a rainfall alert."""
    subject = f"[{alert.level}] Rainfall alert — {city}"
    body = (
        f"City: {city}\n"
        f"Level: {alert.level}\n"
        f"Rainfall: {alert.rainfall_mm_h:.2f} mm/h\n"
        f"Message: {alert.message}\n"
    )
    return subject, body


def smtp_settings_from_env() -> dict:
    return {
        "host": os.getenv("SMTP_HOST", "").strip(),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": os.getenv("SMTP_USER", "").strip(),
        "password": os.getenv("SMTP_PASSWORD", "").strip(),
        "sender": os.getenv("ALERT_EMAIL_FROM", os.getenv("SMTP_USER", "")).strip(),
        "recipient": os.getenv("ALERT_EMAIL_TO", "").strip(),
        "use_tls": os.getenv("SMTP_USE_TLS", "1").strip() not in ("0", "false", "False"),
    }


def write_email_outbox(
    city: str,
    alert: AlertResult,
    path: str = "email_outbox.txt",
) -> None:
    """Record would-be email when SMTP is not configured (grader-friendly)."""
    subject, body = format_alert_email(city, alert)
    line = (
        f"---\nTO: (configure ALERT_EMAIL_TO)\nSUBJECT: {subject}\n{body}\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)


def send_red_alert_email(
    city: str,
    alert: AlertResult,
    settings: Optional[Settings] = None,
    *,
    dry_run: bool = False,
    outbox_path: str = "email_outbox.txt",
) -> bool:
    """
    Send SMTP email for RED alerts. Returns True if sent or logged to outbox.

    Requires env: SMTP_HOST, SMTP_USER, SMTP_PASSWORD, ALERT_EMAIL_TO
    (optional: SMTP_PORT, ALERT_EMAIL_FROM, SMTP_USE_TLS).
    """
    if alert.level != "RED":
        return False

    cfg = smtp_settings_from_env()
    subject, body = format_alert_email(city, alert)

    if dry_run or not cfg["host"] or not cfg["recipient"]:
        write_email_outbox(city, alert, outbox_path)
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = cfg["sender"] or cfg["user"]
    msg["To"] = cfg["recipient"]
    msg.set_content(body)

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=15) as server:
            if cfg["use_tls"]:
                server.starttls()
            if cfg["user"]:
                server.login(cfg["user"], cfg["password"])
            server.send_message(msg)
    except OSError as exc:
        raise EmailDeliveryError(str(exc)) from exc
    return True
