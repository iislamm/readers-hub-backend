import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_SECRET = os.environ.get('TOKEN_SECRET')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
