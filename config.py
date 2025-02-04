import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:password@127.0.0.1:3306/se481pj'
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False
CORS_HEADERS = 'Content-Type'
# 16 mb
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SQLALCHEMY_POOL_SIZE = 30
SQLALCHEMY_POOL_TIMEOUT = 300
