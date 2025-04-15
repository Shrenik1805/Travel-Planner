from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User  # Import db and User model
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'danger')
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Correct hashing method
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can log in now.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', title="Register")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch user from the database by email
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user'] = email
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html', title="Login")

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.', 'info')
    return redirect(url_for('main.index'))
