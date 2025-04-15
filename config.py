# config.py
import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
    
    # Email settings for Flask-Mail (for itinerary/expenses sharing, etc.)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Get the email from environment variables
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Get the app-specific password from environment variables

    # SQLAlchemy settings (Database URI and options)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')  # Default to SQLite, can be overridden by DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save resources

    # Flask-Migrate settings (for managing database migrations)
    MIGRATION_DIRECTORY = 'migrations'  # This is the default directory for Flask-Migrate to store migrations

    # Default currency setting
    DEFAULT_CURRENCY = os.environ.get('DEFAULT_CURRENCY', 'INR')

    # You can add more configuration variables here if needed