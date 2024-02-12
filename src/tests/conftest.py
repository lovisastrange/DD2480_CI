import pytest 
from main import create_app
from utils.logger import LogCaptureHandler

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DEBUG': True
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def captured_logs(app):
    logger = app.logger
    handler = LogCaptureHandler()
    logger.addHandler(handler)
    yield handler.records
    logger.removeHandler(handler)