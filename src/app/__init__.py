from flask import Flask

def create_app():
    """
    App factory
    """

    app = Flask(__name__)
    return app