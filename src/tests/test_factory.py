"""
Tests for the app factory.
"""
from main import create_app

def test_config():
    # Input: app factory.
    # Expected behavior: the app factory generates the right
    # config for the app.
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing