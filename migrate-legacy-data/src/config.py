"""
Database configuration and app factory for migration scripts
"""
import os
from flask import Flask
from app.models import db

def create_app():
    """Create and configure Flask application for migration scripts"""
    app = Flask(__name__)
    
    # Database configuration - use the same database as the main app
    database_path = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'fishao.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    return app
