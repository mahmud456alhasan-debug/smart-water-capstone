"""Tests for optional email alert extension."""

from __future__ import annotations

from alerts import check_alert
from config import offline_settings
from email_alerts import (
    format_alert_email,
    send_red_alert_email,
    smtp_settings_from_env,
    write_email_outbox,
)


def test_format_alert_email_red():
    settings = offline_settings()
    alert = check_alert(25.0, settings)
    subject, body = format_alert_email("Dhaka,BD", alert)
    assert "RED" in subject
    assert "Dhaka,BD" in body
    assert "25.00" in body


def test_write_email_outbox(tmp_path):
    settings = offline_settings()
    alert = check_alert(22.0, settings)
    out = tmp_path / "outbox.txt"
    write_email_outbox("London,GB", alert, str(out))
    text = out.read_text(encoding="utf-8")
    assert "London,GB" in text
    assert "RED" in text


def test_send_red_skips_green(tmp_path, monkeypatch):
    settings = offline_settings()
    alert = check_alert(5.0, settings)
    assert send_red_alert_email("X", alert, outbox_path=str(tmp_path / "o.txt")) is False


def test_send_red_logs_outbox_when_no_smtp(tmp_path, monkeypatch):
    monkeypatch.delenv("SMTP_HOST", raising=False)
    settings = offline_settings()
    alert = check_alert(21.0, settings)
    out = tmp_path / "outbox.txt"
    assert send_red_alert_email("Paris,FR", alert, outbox_path=str(out)) is True
    assert "Paris,FR" in out.read_text(encoding="utf-8")


def test_smtp_settings_from_env(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("ALERT_EMAIL_TO", "user@example.com")
    cfg = smtp_settings_from_env()
    assert cfg["host"] == "smtp.example.com"
    assert cfg["recipient"] == "user@example.com"
