from flask import Flask
from config import Config
from .db import init_db, db
from flask_migrate import Migrate
from .auth import auth_bp
from . import books_bp
from . import lists_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config())
    else:
        app.config.from_object(test_config)

    init_db(app)

    Migrate(app, db)

    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(books_bp.bp)
    app.register_blueprint(lists_bp.bp)

    @app.route('/hello')
    def hello():
        return 'Hello, world'

    return app
