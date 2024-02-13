"""
Tests for the CI server routes.
"""

def test_webhook(client):
    # Input: client used to perform request to the base URL.
    # Expected behavior: the base HTML file is received as a response.
    response = client.get('/server/')
    assert b"<title>CI Server</title>" in response.data

def test_logging(app, captured_logs):
    # Input: 
    # - app used to send logs
    # - logs captured by the handler
    # Expected behaviour: the logs are correct.
    app.logger.info("This is an info log")
    app.logger.warning("This is a warning log")
    app.logger.error("This is an error log")

    assert any("This is an info log" in record.msg for record in captured_logs)
    assert any("This is a warning log" in record.msg for record in captured_logs)
    assert any("This is an error log" in record.msg for record in captured_logs)