import json
import pytest
import os
from dotenv import load_dotenv
from ..main.webhook_handler import Webhook_handler

load_dotenv()

def test_verify_failure(client, mocker):
    mocker.patch('main.webhook_handler.hmac.new', return_value=mocker.Mock(hexdigest=lambda: os.getenv('WEBHOOK_SECRET')))
    
    with pytest.raises(ValueError):
        client.post('/server/webhook', headers={'X-Hub-Signature-256': 'sha256=invalid_signature'}, data=b'test data')

def test_parse_data_success():
    data = {
        'repository': {'name': 'test_repo', 'clone_url':'https://github.com/lovisastrange/DD2480_CI.git'},
        'after': 'test_commit',
        'ref': 'refs/heads/main'
    }
    headers = {'X-Hub-Signature-256': f'sha256={os.getenv("WEBHOOK_SECRET")}', 'Content-Type': 'application/json'}
    handler = Webhook_handler(os.getenv('WEBHOOK_SECRET'))
    result = handler.parse_data(headers, data)
    expected = {
        "event": None,
        "owner": 'unknown',
        "repo": "test_repo",
        "clone_url": "https://github.com/lovisastrange/DD2480_CI.git",
        "commit": "test_commit",
        "branch": "main"
    }
    assert result == expected

def test_parse_data_missing_data(client):
    with pytest.raises(ValueError):
        client.post('/server/webhook', data={})