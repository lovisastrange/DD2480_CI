def test_webhook(client):
    response = client.get('/server/')
    assert b"<title>CI Server</title>" in response.data

def test_logging(app, captured_logs):
    app.logger.info("This is an info log")
    app.logger.warning("This is a warning log")
    app.logger.error("This is an error log")

    assert any("This is an info log" in record.msg for record in captured_logs)
    assert any("This is a warning log" in record.msg for record in captured_logs)
    assert any("This is an error log" in record.msg for record in captured_logs)