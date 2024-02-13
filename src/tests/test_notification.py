from main.notification import send_notification_webhook

def test_notification():
    message = "Test message"
    response = send_notification_webhook(message)
    assert response == 204