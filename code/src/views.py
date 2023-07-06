import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from .models import Admin, User, Venue, Show, Booking
from . import db
from . import views
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


views = Blueprint('views', __name__)




@views.route('/')
def index():
    return render_template('index.html') 


@views.route('/admin_registration', methods=['GET', 'POST'])
def admin_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #add new Admin record to database
        admin = Admin(username=username, password=password)
        db.session.add(admin)
        db.session.commit()
        flash('Admin Registered Successfully', category='success')
        return redirect(url_for('views.admin_login'))
    
    return render_template('admin_reg.html')


@views.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #add new User record to database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('User Registered Successfully', category='success')
        return redirect(url_for('views.user_login'))
        
    return render_template('user_reg.html')


# Admin Login
@views.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            session['admin_id'] = admin.id
            return redirect(url_for('views.admin_dashboard'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('views.admin_login'))
     return render_template('admin_login.html')

#Admin Logout
@views.route('/admin_logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('views.index'))


# User Login
@views.route('/user_login', methods=['GET', 'POST'])
def user_login():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('views.user_dashboard'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('views.user_login'))
     return render_template('user_login.html')


#User Logout
@views.route('/user_logout')
def user_logout():
    session.pop('user_id', None)
    return redirect(url_for('views.index'))

# Admin Dashboard
@views.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        if len(Venue.query.all()) > 0:
            venues = Venue.query.all()
            return render_template('admin_dash.html', venues=venues, admin=admin)
        else: 
            return render_template('admin_dash.html', admin=admin)
    else:
        return redirect(url_for('views.admin_login'))


# User Dashboard
@views.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        venues = Venue.query.all()
        if len(venues) > 0: 
                
                print(venues[0].shows.first(),"line115")
                return render_template('user_dash.html', venues=venues, user=user)
        else: 
            print(venues,"line118")
            return render_template('user_dash.html', user=user)
    else:
        return redirect(url_for('views.user_login'))

# Add Venue
@views.route('/add_venue', methods=['GET', 'POST'])
def add_venue():
     if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        if request.method == 'POST':
            venue_name = request.form['venue_name']
            place = request.form['place']
            location = request.form['location']
            capacity = request.form['capacity']

            #add new Venue record to database
            venue = Venue(venue_name=venue_name, place=place, location=location, capacity=capacity)
            db.session.add(venue)
            db.session.commit()
            return redirect(url_for('views.admin_dashboard'))
            
        return render_template('add_venue.html', admin=admin)




# Add Show
@views.route('/venue/<int:venue_id>/add_show', methods=['GET', 'POST'])
def add_show(venue_id):
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        if request.method == 'POST':
            show_name = request.form['show_name']
            venue_id = request.form['venue_id']
            rating = request.form['rating']
            tags = request.form['tags']
            time = request.form['time']
            price = request.form['price']
            poster = request.files['poster']
            poster_path = 'src/static/images/' + poster.filename
            poster.save(poster_path)
            

            #add new Show record to database
            show = Show(show_name=show_name, venue_id=venue_id, tags=tags, time=time, rating=rating, price=price, poster_path=poster_path, seats_booked=0)
            db.session.add(show)
            db.session.commit()
            return redirect(url_for('views.admin_dashboard'))
            
        return render_template('add_show.html', venue_id=venue_id, admin=admin)


@views.route('/static/images/<path:filename>')
def uploaded_poster(filename):
    return send_from_directory('static/images/', filename)




#Edit Venue
@views.route('/venue/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        venue = Venue.query.get(venue_id)
        if request.method == 'POST':
            new_venue_name = request.form.get("new_venue_name")
            venue.venue_name = new_venue_name
            db.session.commit()
            return redirect("/admin_dashboard")
        return render_template('edit_venue.html', venue=venue, admin=admin)


#Delete Venue
@views.route('/venue/<int:venue_id>/delete', methods=['GET', 'POST'])
def delete_venue(venue_id):
    book = Venue.query.get(venue_id)
    db.session.delete(book)
    db.session.commit()
    return redirect("/admin_dashboard")


#Edit Show
@views.route('/show/<int:show_id>/actions', methods=['GET', 'POST'])
def edit_show(show_id):
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        show = Show.query.get(show_id)
        if request.method == 'POST':
            new_show_name = request.form.get("new_show_name")
            show.show_name = new_show_name
            db.session.commit()
            return redirect("/admin_dashboard")
        return render_template('show_actions.html', show=show, admin=admin)


#Delete Show
@views.route('/show/<int:show_id>/delete', methods=['GET', 'POST'])
def delete_show(show_id):
    show = Show.query.get(show_id)
    db.session.delete(show)
    db.session.commit()
    return redirect("/admin_dashboard")


#Book Show
@views.route('/show/<int:show_id>/book', methods=['GET', 'POST'])
def book_show(show_id):
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        show = Show.query.get(show_id)
        venue = Venue.query.get(show.venue_id)
        venue_id = show.venue_id
        available_seats = venue.capacity 
        
        if request.method == 'POST':
            show_id = request.form.get("show_id")
            user_id = request.form.get("user_id")
            seats_booked = request.form.get("seats_booked")
            show_price = request.form.get("price")
            total_price = int(show_price) * int(seats_booked)

            show.seats_booked += int(seats_booked)
            user.seats_booked += int(seats_booked)
            
            booking=Booking(show_id=show_id, user_id=user_id , seats_booked=seats_booked, total_price=total_price)
            db.session.add(booking)
            db.session.commit()
            return redirect("/user_dashboard")
        
        available_seats = venue.capacity - show.seats_booked #update available seats
        return render_template('book_show.html', show_id=show_id, venue_id=venue_id, show=show, user=user, venue=venue, available_seats=available_seats)


#User Profile
@views.route('/user_bookings', methods=['GET', 'POST'])
def user_profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        booking=Booking.query.filter_by(user_id=user.id).all()
        show=Show.query.all()
        venue=Venue.query.all()
        booked_shows = [booked_shows.show_id for booked_shows in booking]
            
        return render_template('user_booking.html', user=user, booking=booking, booked_shows=booked_shows, show=show, venue=venue)


#Search Show
@views.route('/search', methods=['POST'])
def search():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        search = request.form.get("search")
        searched_show = Show.query.filter(Show.show_name.like('%'+search+'%'))
        show=Show.query.all()
        venue = Venue.query.all()
        return render_template('search.html', searched_show=searched_show, venue=venue, user=user, show=show)
    

#Rate Show
@views.route('/show/<int:show_id>/rate', methods=['GET', 'POST'])
def rate_show(show_id):
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        show = Show.query.get(show_id)
        if request.method == 'POST':
            rating = request.form.get("rate")
            show.rating = rating
            db.session.commit()
            return redirect("/user_bookings")
        return render_template('rate_page.html', show=show, user=user)
    



#Summary Page
@views.route('/summary', methods=['GET'])
def summary():
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        show_sale={}
        show = Show.query.all()
        for show in show:
            show_sale[show.show_name] = show.seats_booked

        sorted_show_sale = {n: m for n, m in sorted(show_sale.items(), key=lambda x: x[1], reverse=True)}

        
        plt.bar(range(len(sorted_show_sale)), list(sorted_show_sale.values()), align='center')
        plt.xticks(range(len(sorted_show_sale)), list(sorted_show_sale.keys()))
        plt.ylabel('Number of Tickets Sold')
        plt.xlabel('Most Sold Shows')

        graph_file = os.path.join(views.root_path, 'static', 'graph.png')
        plt.savefig(graph_file)

        return render_template('summary.html', graph_file='/static/graph.png', admin=admin, show=show, sorted_show_sale=sorted_show_sale)

       