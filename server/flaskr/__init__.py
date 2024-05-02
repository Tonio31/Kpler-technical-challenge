import os
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from logging.handlers import RotatingFileHandler

def setup_logging(app):
    # Create a logger
    app.logger.setLevel(logging.DEBUG)  # Adjust to the appropriate log level

    # Create a file handler that logs even debug messages
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
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
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.before_request
    def log_request_info():
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())

    from . import vessels
    app.register_blueprint(vessels.bp)

    # a simple page that says hello
    @app.route('/hello', methods=('GET', 'POST'))
    def hello():
        return jsonify(user="joe")

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors gracefully."""
        app.logger.exception("Unhandled Exception")
        response = jsonify({
            "status": "error",
            "message": "An unexpected error occurred.",
            "details": str(error)
        })
        response.status_code = 500  # Internal Server Error
        return response

    return app