from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path



db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder='static')
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
    app.config['SECRET_KEY']='secretkey'
    app.config['UPLOAD_FOLDER'] = 'src/static/images'
        
    db.init_app(app)



    from .views import views


    app.register_blueprint(views, url_prefix='/')


    from .models import Admin, User, Venue, Show, Booking

    create_database(app)


    return app

def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')




