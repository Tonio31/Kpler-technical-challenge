import os
import logging

from flask import Flask, jsonify
from flask_cors import CORS

from logging.handlers import RotatingFileHandler

def setup_logging(app):
    app.logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    setup_logging(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import vessels
    app.register_blueprint(vessels.bp)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled Exception")
        response = jsonify({
            "status": "error",
            "message": "An unexpected error occurred.",
            "details": str(error)
        })
        response.status_code = 500  # Internal Server Error
        return response

    return app