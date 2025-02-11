import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///heartrate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False