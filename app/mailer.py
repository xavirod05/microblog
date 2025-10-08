# app/mailer.py for http email

import threading
import requests
import os
from app import app

# load and sanitize API key
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_API_KEY = BREVO_API_KEY.strip() if BREVO_API_KEY else None
if __name__ == "main":
    print(f"[DEBUG] BREVO_API_KEY 0805: {BREVO_API_KEY}")

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_email(subject, sender, recipients, text_body, html_body):
    """Launch email send in a background thread to avoid blocking the main app."""
    print("are we in send_email?")
    thread = threading.Thread(
        target=send_async_email,
        args=(subject, sender, recipients, text_body, html_body),
    )
    print(f"[DEBUG] starting thread: {BREVO_API_KEY}")
    thread.start()


def build_payload(subject, sender, recipients, text_body, html_body):
    """Construct the JSON payload for Brevo API."""
    return {
        "sender": {"name": sender.split("@")[0], "email": sender},
        "to": [{"email": r} for r in recipients],
        "subject": subject,
        "htmlContent": html_body,
        "textContent": text_body,
    }


def send_async_email(subject, sender, recipients, text_body, html_body):
    print("[Email Thread] Started send_async_email", flush=True)

    if not BREVO_API_KEY:
        print("[Email Thread] BREVO_API_KEY is missing.")
        raise RuntimeError("BREVO_API_KEY environment variable not set")

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = build_payload(subject, sender, recipients, text_body, html_body)
    print("entering try statement")

    try:
        response = requests.post(BREVO_API_URL, headers=headers, json=payload)
        print(f"[Email Thread] Status: {response.status_code}")

        if response.status_code >= 400:
            print(
                f"[Email Thread] Warning: Received error status {response.status_code}"
            )

        try:
            print(f"[Email Thread] Response: {response.json()}")
        except ValueError:
            print(f"[Email Thread] Non-JSON response: {response.text}")

    except Exception as e:
        print(f"[Email Thread] Error sending email: {e}")


from flask import render_template


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    print("are we in send_password_reset_email?")
    send_email(
        subject="[Microblog] Reset Your Password",
        sender=app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )
