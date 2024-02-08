def test_webhook(client):
    response = client.get('/server/')
    assert b"<title>CI Server</title>" in response.data