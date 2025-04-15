# app/routes/share.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import mail
from flask_mail import Message
from app.models import Trip, User

share_bp = Blueprint('share', __name__)

@share_bp.route('/', methods=['GET', 'POST'])
def share():
    if 'user' not in session:
        flash('Please log in to share itineraries.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user's trips for sharing
    trips = Trip.query.filter_by(user_id=user.id).all()
    
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        message = request.form.get('message')
        trip_id = request.form.get('trip_id')
        
        # Verify trip belongs to user if trip_id is provided
        if trip_id:
            trip = Trip.query.get(trip_id)
            if not trip or trip.user_id != user.id:
                flash('Trip not found or you do not have permission to share this trip.', 'danger')
                return redirect(url_for('share.share'))
            
            # Add trip details to message
            message += f"\n\nTrip: {trip.trip_name}\nDestination: {trip.destination}\n"
            message += f"Dates: {trip.start_date.strftime('%Y-%m-%d')} to {trip.end_date.strftime('%Y-%m-%d')}\n"
            
            # Add activities if any
            if trip.activities:
                message += "\nActivities:\n"
                for activity in trip.activities:
                    message += f"- {activity.activity_name}\n"

        try:
            msg = Message(subject, recipients=[recipient], body=message, sender=user.email)
            mail.send(msg)
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send email: {str(e)}', 'danger')

        return redirect(url_for('share.share'))

    return render_template('share.html', title="Share via Email", trips=trips)