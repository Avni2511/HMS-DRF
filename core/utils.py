import os
import requests

def send_email_sendgrid(to_email, subject, message):
    api_key = os.getenv("SENDGRID_API_KEY")

    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "personalizations": [
            {
                "to": [{"email": to_email}]
            }
        ],
        "from": {"email": "your_verified_email@domain.com"},
        "subject": subject,
        "content": [
            {
                "type": "text/plain",
                "value": message
            }
        ]
    }

    requests.post(url, headers=headers, json=data, timeout=5)