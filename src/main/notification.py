import requests
import os

def send_notification_webhook(message):
    url = os.getenv('DISCORD_WEBHOOK')
    data = {
        "content": message
    }
    response = requests.post(url, data=data)
    return response.status_code