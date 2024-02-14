import os

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from .database import init_db

init_db()


def create_app(test_config : dict = None):
    """
    App factory: creates the app and 
    makes it available for the rest
    of the program.

    Parameters
    ----------
    test_config: dict
        used to provide a special config for testing
    """
    logger = logging.getLogger()
    logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    os.makedirs('../logs/', exist_ok=True)
    fileHandler = RotatingFileHandler(f"../logs/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log", backupCount=100, maxBytes=1024)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path)
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import ci_server
    app.register_blueprint(ci_server.bp)
    
    return app