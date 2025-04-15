# app/routes/main.py
from flask import Blueprint, render_template, session, redirect, url_for
from app.models import Trip, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user' in session:
        user = User.query.filter_by(email=session['user']).first()
        if user:
            # Query for the first few trips to display on the main page for logged-in user
            itineraries = Trip.query.filter_by(user_id=user.id).limit(5).all()
            return render_template('index.html', title="Travel Planner", itineraries=itineraries)
    
    # If not logged in or user not found, show generic page
    return render_template('index.html', title="Travel Planner", itineraries=[])