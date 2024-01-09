from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from .config import Config
from .database import db



db = SQLAlchemy()

def create_database(app):
    if not os.path.exists( app.config['SQLITE_DB_DIR'] + app.config['SQLITE_DB_NAME'] ):
        with app.app_context():
            db.create_all()
            print('Database Created!')

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder='static')

    app.config.from_object(Config)
    db.init_app(app)

    from application.views import views
    app.register_blueprint(views, url_prefix='/')

    from application.models import Admin, User, Venue, Show, Booking
    create_database(app)

    return app






