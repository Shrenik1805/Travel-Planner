# app/models.py
from datetime import datetime
from app import db

# User Model for Authentication
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Relationship with Trip model
    trips = db.relationship('Trip', back_populates='user', lazy=True)
    # Relationship with settings
    settings = db.relationship('Setting', back_populates='user', uselist=False, lazy=True)

# Trip Model for itinerary planning
class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    trip_name = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Foreign key linking to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='trips')

    # Relationships with Budget, Activities, and Expenses
    budget = db.relationship('Budget', back_populates='trip', uselist=False, lazy=True, cascade="all, delete-orphan")
    activities = db.relationship('Activity', back_populates='trip', lazy=True, cascade="all, delete-orphan")
    expenses = db.relationship('Expense', back_populates='trip', lazy=True, cascade="all, delete-orphan")

# Budget Model for storing trip budgets
class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, nullable=False)
    categories = db.Column(db.JSON, nullable=True)  # Store categories as JSON

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='budget')

# Activity Model for storing trip activities
class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='activities')

# Expense Model for tracking expenses related to trips
class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Track the date of expense

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='expenses')

# Additional model for managing settings (like language, currency, etc.)
class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(10), nullable=False, default="en")
    currency = db.Column(db.String(10), nullable=False, default="INR")  # Updated to INR
    location = db.Column(db.String(120), nullable=True)

    # Relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='settings')