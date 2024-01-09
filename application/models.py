from .import db
from flask_sqlalchemy import SQLAlchemy


# Model for Admin
class Admin(db.Model):
    id = db.Column('admin_id', db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)



# Model for User
class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    booking = db.relationship('Booking', backref='user')
    seats_booked = db.Column(db.Integer, nullable=False, default=0)



# Model for Venue
class Venue(db.Model):
    id = db.Column('venue_id', db.Integer, primary_key = True)
    venue_name = db.Column(db.String(120), nullable=False)
    place = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='venue', lazy='dynamic', cascade='all, delete-orphan')

# Model for Show
class Show(db.Model):
    id = db.Column('show_id', db.Integer, primary_key = True)
    show_name = db.Column(db.String(120), nullable=False)
    venue_id =  db.Column(db.Integer,db.ForeignKey('venue.venue_id', ondelete='CASCADE'))
    tags = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    poster_path = db.Column(db.String(120), nullable=False)
    booking = db.relationship('Booking', backref='show')
    seats_booked = db.Column(db.Integer, nullable=False)


# Model for Booking
class Booking(db.Model):
    id = db.Column('booking_id', db.Integer, primary_key = True)
    show_id = db.Column(db.Integer,db.ForeignKey('show.show_id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id', ondelete='CASCADE'))
    seats_booked = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    
