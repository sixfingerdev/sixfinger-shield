#!/usr/bin/env python3
"""
Create an admin user for SixFinger Shield Flask application
"""
import os
import sys
import secrets
import string

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import create_app
from app.models import db, User, Credit

def generate_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

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
            print("\nTo reset password, delete the user from database and run this script again.")
            return
        
        # Generate secure random password
        password = generate_password()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@sixfinger.dev',
            is_admin=True,
            is_active=True
        )
        admin.set_password(password)
        
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
        print(f"Password: {password}")
        print(f"Initial Credits: 10,000")
        print("\n⚠️  IMPORTANT: Save this password securely! It won't be shown again.")
        print("⚠️  Change the password after first login!")

if __name__ == '__main__':
    create_admin()
