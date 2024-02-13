import unittest
from unittest.mock import patch
from main.notification import send_notification_webhook

class TestNotification(unittest.TestCase):

    @patch('main.notification.requests.post')
    def test_notification(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 204

        message = "Test message"
        response = send_notification_webhook(message)

        mock_post.assert_called_once()
        
        self.assertEqual(response, 204)

if __name__ == '__main__':
    unittest.main()