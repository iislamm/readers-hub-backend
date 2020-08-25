from flask import Flask
from config import Config
from .db import init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config())
    else:
        app.config.from_mapping(test_config)

    init_db(app)

    @app.route('/hello')
    def hello():
        return 'Hello, world'

    return app
