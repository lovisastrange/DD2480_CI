import pytest 
from ..app import create_app

@pytest.fixture
def application():
    application = create_app()

    yield application

@pytest.fixture()
def client(application):
    return application.test_client()