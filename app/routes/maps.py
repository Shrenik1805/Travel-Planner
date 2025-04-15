# app/routes/maps.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import User, Trip

maps_bp = Blueprint('maps', __name__)

@maps_bp.route('/')
def maps():
    if 'user' not in session:
        flash('Please log in to access maps.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user's trips to display on the map
    trips = Trip.query.filter_by(user_id=user.id).all()
    
    # You can add logic here to pass map data
    return render_template('maps.html', title="Travel Maps", trips=trips)