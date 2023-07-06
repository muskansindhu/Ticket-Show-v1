# **Ticket Show Web Application**

# Description 
Ticket Show is a Flask-based web application that allows users to make bookings for multiple shows at different venues. The app has a feature where users can search for different shows and have a look at the bookings made by them on a separate page. This app allows the admin to perform CRUD operations on venues and shows and to view a summary chart for the number of bookings made for different shows.

# Technologies Used
- Flask: web framework for building the web application

- Flask-SQLAlchemy: used for streamlined management of databases 

- SQLite: database for storing admin, user, venues, shows and bookings

- Jinja: used for separation of logic and dynamic HTML rendering in Flask app

- HTML: for developing the web page

- Bootstrap: To make the frontend appealing and easily navigate 

- Matplotlib: To create chart to view the most booked show


# API Design
The CRUD API was created for performing operations such as adding the venue, editing and deleting the venue. A similar CRUD API was created for adding the show, editing and deleting the show.


# Architecture and Features:
The application follows the standard MVC architecture. The View of the application is created using HTML and Bootstrap. The Controller is created using Python and Flask. The Model is created using SQLite.

The features of the application are as follows:
- Separate Sign-Up and Login page for admin and user
- Ability to view venue and shows
- Ability to search for shows
- Ability to make bookings
- Ability to view the number of show booking summary chart
- Create, View, Edit and Delete venue
- Create, View, Edit and Delete show


# Installation and Usage

To run the application:

1. Install the dependencies with `pip install -r requirements.txt`

2. To run the flask app, on the shell, run `python app.py`

3. Access the application at `http://127.0.0.1:5000`