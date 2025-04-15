# app/__init__.py
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Import config here to avoid circular imports
    from config import Config
    app.config.from_object(Config)

    # Initialize extensions
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to avoid circular imports
    from app.models import User, Trip, Budget, Activity, Expense, Setting

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.itinerary import itinerary_bp
    from app.routes.budget import budget_bp
    from app.routes.expenses import expenses_bp
    from app.routes.settings import settings_bp
    from app.routes.maps import maps_bp
    from app.routes.auth import auth_bp
    from app.routes.share import share_bp

    # Register all blueprints with the correct URL prefixes
    app.register_blueprint(main_bp)
    app.register_blueprint(itinerary_bp, url_prefix='/itinerary')
    app.register_blueprint(budget_bp, url_prefix='/budget')
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(maps_bp, url_prefix='/maps')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(share_bp, url_prefix='/share')

    return app