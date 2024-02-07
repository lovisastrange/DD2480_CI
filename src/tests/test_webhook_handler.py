import unittest
from unittest.mock import patch
from app.webhook_handler import Webhook_handler
from flask import Flask

app = Flask(__name__)


class TestWebhookHandler(unittest.TestCase):

    def setUp(self):
        self.secret_key = 'test_secret'
        self.handler = Webhook_handler(self.secret_key)

    """
    Test case 1: Successful verification
    Sending a request with a valid signature should not raise an exception.
    """
    @patch('webhook_handler.request')
    def test_verify_success(self, mock_request):
        mock_request.headers = {'X-Hub-Signature-256': 'sha256=valid_signature'}
        mock_request.data = b'test data'
        # Mocking `hmac.new().hexdigest()` to return 'valid_signature'
        with patch('hmac.new') as mock_hmac:
            mock_hmac.return_value.hexdigest.return_value = 'valid_signature'
            # No exception means verification passed
            self.handler.verify()
    
    """
    Test case 2: Failed verification
    Sending a request without a signature should raise a ValueError.
    """
    @patch('webhook_handler.request')
    def test_verify_failure(self, mock_request):
        mock_request.headers = {'X-Hub-Signature-256': 'sha256=invalid_signature'}
        mock_request.data = b'test data'
        with patch('hmac.new') as mock_hmac:
            mock_hmac.return_value.hexdigest.return_value = 'valid_signature'
            with self.assertRaises(ValueError):
                self.handler.verify()

    """
    Test case 3: Successful data parsing
    Sending a request with valid data should return the expected dictionary.
    """
    @patch('webhook_handler.request')
    def test_parse_data_success(self, mock_request):
        mock_request.get_json.return_value = {
            'repository': {'name': 'test_repo'},
            'after': 'test_commit',
            'ref': 'refs/heads/test_branch'
        }
        expected = {
            "repo": "test_repo",
            "commit": "test_commit",
            "branch": "test_branch"
        }
        self.assertEqual(self.handler.parse_data(), expected)

    """
    Test case 4: Missing data
    Sending a request without data should raise a ValueError.
    """
    @patch('webhook_handler.request')
    def test_parse_data_missing_data(self, mock_request):
        mock_request.get_json.return_value = None
        with self.assertRaises(ValueError):
            self.handler.parse_data()

if __name__ == '__main__':
    unittest.main()