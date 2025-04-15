# app/routes/itinerary.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Trip, Activity, User  # Import the User model
from datetime import datetime

itinerary_bp = Blueprint('itinerary', __name__)

# Helper function to check if user is logged in
def is_logged_in():
    return 'user' in session

# Route to display and create new itineraries
@itinerary_bp.route('/', methods=['GET', 'POST'])
def itinerary():
    if not is_logged_in():
        flash('Please log in to access your itineraries.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        trip_name = request.form.get('trip_name')
        destination = request.form.get('destination')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        activities_data = request.form.get('activities').split('\n')

        # Create a new trip and save it to DB
        new_trip = Trip(
            trip_name=trip_name,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            user_id=user.id  # Associate trip with the logged-in user
        )

        # Add activities to the trip
        for activity_name in activities_data:
            if activity_name.strip():  # Skip empty activity names
                activity = Activity(activity_name=activity_name.strip(), trip=new_trip)
                db.session.add(activity)

        db.session.add(new_trip)
        db.session.commit()

        flash('Itinerary saved successfully!', 'success')
        return redirect(url_for('itinerary.itinerary'))

    # Retrieve all trips for the current user
    trips = Trip.query.filter_by(user_id=user.id).all()
    return render_template('itinerary.html', title="Itinerary Planner", trips=trips)


# Route to delete a trip
@itinerary_bp.route('/delete/<int:trip_id>', methods=['POST'])
def delete_trip(trip_id):
    if not is_logged_in():
        flash('Please log in to access your itineraries.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    trip = Trip.query.get(trip_id)
    
    if not trip or trip.user_id != user.id:
        flash("Trip not found or you don't have permission to delete it.", "danger")
        return redirect(url_for('itinerary.itinerary'))
    
    db.session.delete(trip)
    db.session.commit()
    flash('Trip deleted successfully.', 'info')
    return redirect(url_for('itinerary.itinerary'))


# Route to edit a trip
@itinerary_bp.route('/edit/<int:trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    if not is_logged_in():
        flash('Please log in to access your itineraries.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    trip = Trip.query.get(trip_id)

    if not trip or trip.user_id != user.id:
        flash("Trip not found or you don't have permission to edit it.", "danger")
        return redirect(url_for('itinerary.itinerary'))

    if request.method == 'POST':
        trip.trip_name = request.form.get('trip_name')
        trip.destination = request.form.get('destination')
        trip.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        trip.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')

        # Handle activities (clear existing activities, then add new ones)
        # We don't need to explicitly delete activities since we've set up cascade delete
        trip.activities = []
        activities_data = request.form.get('activities').split('\n')

        for activity_name in activities_data:
            if activity_name.strip():
                activity = Activity(activity_name=activity_name.strip(), trip=trip)
                db.session.add(activity)

        db.session.commit()
        flash("Trip updated successfully.", "success")
        return redirect(url_for('itinerary.itinerary'))

    return render_template('edit_trip.html', title="Edit Trip", trip=trip)