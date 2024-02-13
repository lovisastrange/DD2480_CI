import pytest 
from main import create_app
from utils.logger import LogCaptureHandler

@pytest.fixture
def app():
    """
    Pytest fixture that creates an app
    used during testing.
    """
    app = create_app({
        'TESTING': True,
        'DEBUG': True
    })

    yield app

@pytest.fixture()
def client(app):
    """
    Pytest fixture that creates a client
    object used to perform requests during testing.

    Parameters
    ----------
    app: Flask app
        the app created with the app fixture.
    """
    return app.test_client()

@pytest.fixture()
def runner(app):
    """
    Pytest fixture that creates a cli runner
    object used to run commands during testing.

    Parameters
    ----------
    app: Flask app
        the app created with the app fixture.
    """
    return app.test_cli_runner()

@pytest.fixture
def captured_logs(app):
    """
    Pytest fixture that creates a logger
    object and a handler able to capture
    logs while testing.

    Parameters
    ----------
    app: Flask app
        the app created with the app fixture.
    """
    logger = app.logger
    handler = LogCaptureHandler()
    logger.addHandler(handler)
    yield handler.records
    logger.removeHandler(handler)