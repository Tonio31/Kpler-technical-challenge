import os
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.logger.setLevel(logging.DEBUG)  # Set log level to INFO
    handler = logging.FileHandler('app.log')  # Log to a file
    app.logger.addHandler(handler)

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


    return app