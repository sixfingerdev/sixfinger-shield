"""Database configuration - import db from models"""
# For backward compatibility
from .models import db

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
