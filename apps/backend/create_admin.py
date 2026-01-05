#!/usr/bin/env python3
"""
Create an admin user for SixFinger Shield Flask application
"""
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import create_app
from app.models import db, User, Credit

def create_admin():
    """Create admin user"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@sixfinger.dev').first()
        if admin:
            print("Admin user already exists!")
            print(f"Email: admin@sixfinger.dev")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@sixfinger.dev',
            is_admin=True,
            is_active=True
        )
        admin.set_password('admin123')  # Change this password!
        
        db.session.add(admin)
        db.session.flush()
        
        # Create credit record with initial credits
        credit = Credit(
            user_id=admin.id,
            balance=10000,
            total_purchased=10000,
            total_used=0
        )
        db.session.add(credit)
        
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print(f"Email: admin@sixfinger.dev")
        print(f"Password: admin123")
        print(f"Initial Credits: 10,000")
        print("\n⚠️  IMPORTANT: Change the password after first login!")

if __name__ == '__main__':
    create_admin()
