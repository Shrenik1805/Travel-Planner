# app/routes/settings.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, Setting

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        flash('Please log in to access settings.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get or create user settings
    user_settings = user.settings
    if not user_settings:
        user_settings = Setting(user_id=user.id)
        db.session.add(user_settings)
        db.session.commit()
    
    if request.method == 'POST':
        language = request.form.get('language')
        currency = request.form.get('currency')
        location = request.form.get('location')

        # Update settings in database
        user_settings.language = language
        user_settings.currency = currency
        user_settings.location = location
        db.session.commit()

        # Also store in session for immediate use
        session['language'] = language
        session['currency'] = currency
        session['location'] = location

        flash('Settings updated!', 'success')
        return redirect(url_for('settings.settings'))

    # Pre-populate form with current settings
    return render_template('settings.html', 
                           title="Settings",
                           settings=user_settings)