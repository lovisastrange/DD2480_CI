"""
Tests for the CI server routes.
"""

def test_home(client):
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

def test_home_page(client):
    # Make a GET request to the home page route
    response = client.get('/server/')
    assert response.status_code == 200

    # Check for build ID and status in the response
    builds = [
        {"id": 10, "status": "fail"},
        {"id": 11, "status": "success"},
        {"id": 12, "status": "success"},
        {"id": 13, "status": "fail"},
    ]

    for build in builds:
        #assert f"Build #{build['id']}" in response.data.decode('utf-8')
        assert build['status'].capitalize() in response.data.decode('utf-8')

def test_specific_build_page(client):
    test_build = {
        "id": "cdc20f11-b101-4eaf-ae17-ac1ef0e6dc2d",
        "date": "03/02/2024, 00:00:00",
        "branch": "new-branch",
        "event": "push",
        "status": "success",
    }

    response = client.get(f'/server/{test_build["id"]}')
    assert response.status_code == 200

    content = response.data.decode('utf-8')
    #assert f"Build No. {test_build['id']}" in content
    assert f"Event</strong>: {test_build['event'].capitalize()}" in content
    assert f"Date</strong>: {test_build['date']}" in content
    assert f"Branch</strong>: {test_build['branch']}" in content
    assert f"Status</strong>: <span class=\"{ 'success' if test_build['status'] == 'success' else 'fail' }\">{test_build['status'].capitalize()}" in content
