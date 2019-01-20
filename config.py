class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # SQLAlchemy setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session secret keys
    SECRET_KEY = 'ae24a87634bf4d749bef9d089cfcb79140d47727'
    SESSION_TYPE = 'sqlalchemy'
    SESSION_USE_SIGNER = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

    # SQLAlchemy setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

