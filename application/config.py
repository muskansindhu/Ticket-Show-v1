import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    SQLITE_DB_DIR = "../db_directory"
    SQLITE_DB_NAME = "app.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, SQLITE_DB_DIR, SQLITE_DB_NAME)}'
    UPLOAD_FOLDER = 'application/static/images'
    SECRET_KEY = 'secretkey'


