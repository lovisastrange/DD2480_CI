import json
import pytest

def test_verify_success(client, mocker):
    mocker.patch('main.webhook_handler.hmac.new', return_value=mocker.Mock(hexdigest=lambda: 'valid_signature'))
    data = {
        'repository': {'name': 'test_repo', 'clone_url':'unknow'},
        'after': 'test_commit',
        'ref': 'refs/heads/test_branch'
    }
    
    response = client.post('/server/webhook', headers={'X-Hub-Signature-256': f'sha256=valid_signature', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 200

def test_verify_failure(client, mocker):
    mocker.patch('main.webhook_handler.hmac.new', return_value=mocker.Mock(hexdigest=lambda: 'valid_signature'))
    
    with pytest.raises(ValueError):
        client.post('/server/webhook', headers={'X-Hub-Signature-256': 'sha256=invalid_signature'}, data=b'test data')

def test_parse_data_success(client, mocker):
    mocker.patch('main.webhook_handler.hmac.new', return_value=mocker.Mock(hexdigest=lambda: 'valid_signature'))
    data = {
        'repository': {'name': 'test_repo', 'clone_url':'unknown'},
        'after': 'test_commit',
        'ref': 'refs/heads/test_branch'
    }
    response = client.post('/server/webhook', headers={'X-Hub-Signature-256': f'sha256=valid_signature', 'Content-Type': 'application/json'}, json=data)
    expected = {
        "repo": "test_repo",
        "clone_url": "unknown",
        "commit": "test_commit",
        "branch": "test_branch"
    }
    assert json.loads(response.data) == expected

def test_parse_data_missing_data(client):
    with pytest.raises(ValueError):
        client.post('/server/webhook', data={})