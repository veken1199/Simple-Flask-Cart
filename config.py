
# SQLAlchemy setup
SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
PORT = 3112

# Session secret keys
SECRET_KEY = "my key"
SESSION_TYPE = "sqlalchemy"
SESSION_USE_SIGNER = True
