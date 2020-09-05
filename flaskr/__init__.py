from flask import Flask
from config import Config
from .db import init_db, db
from flask_migrate import Migrate
from .auth import auth_bp
from .models.book import Book
from .models.challenge import Challenge
from .models.challenge_participants import ChallengeParticipants
from .models.list import List
from .models.list_books import ListBooks
from .models.reading_progress import ReadingProgress
from .models.review import Review
from .models.user import User


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config())
    else:
        app.config.from_object(test_config)

    init_db(app)

    Migrate(app, db)

    app.register_blueprint(auth_bp.bp)

    @app.route('/hello')
    def hello():
        return 'Hello, world'

    return app
