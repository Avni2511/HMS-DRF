import os
import requests
from Hospital import settings

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
        "from": {"email": settings.DEFAULT_FROM_EMAIL},
        "subject": subject,
        "content": [
            {
                "type": "text/plain",
                "value": message
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=5
)

    print("SENDGRID STATUS:", response.status_code)
    print("SENDGRID RESPONSE:", response.text)