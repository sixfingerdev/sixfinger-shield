"""Authentication views"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Credit
from ..database import db
from ..forms import LoginForm, SignupForm, ChangePasswordForm

auth_bp = Blueprint('auth_blueprint', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_blueprint.index'))
    
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                if not user.is_active:
                    flash('Your account has been deactivated.', 'error')
                    return render_template('auth/login.html', form=form)
                
                login_user(user, remember=form.remember_me.data)
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard_blueprint.index'))
            else:
                flash('Invalid email or password.', 'error')
        
        # If JSON request
        if request.is_json:
            return jsonify({"error": "Invalid credentials"}), 401
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_blueprint.index'))
    
    form = SignupForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                is_active=True
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.flush()  # Get user ID
            
            # Create credit record with initial free credits
            credit = Credit(
                user_id=user.id,
                balance=100,  # 100 free credits for new users
                total_purchased=100
            )
            db.session.add(credit)
            
            db.session.commit()
            
            flash('Registration successful! You received 100 free credits.', 'success')
            
            # Auto login
            login_user(user)
            return redirect(url_for('dashboard_blueprint.index'))
        
        # If JSON request
        if request.is_json:
            return jsonify({"error": "Validation failed", "details": form.errors}), 400
    
    return render_template('auth/signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_blueprint.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('dashboard_blueprint.index'))
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('auth/change_password.html', form=form)

# API endpoints for JSON responses
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API login endpoint"""
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        if not user.is_active:
            return jsonify({"error": "Account deactivated"}), 403
        
        login_user(user, remember=data.get('remember_me', False))
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/api/signup', methods=['POST'])
def api_signup():
    """API signup endpoint"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Username, email, and password required"}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        is_active=True
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.flush()
    
    # Create credit record
    credit = Credit(
        user_id=user.id,
        balance=100,
        total_purchased=100
    )
    db.session.add(credit)
    
    db.session.commit()
    
    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 201

@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    """API logout endpoint"""
    logout_user()
    return jsonify({"message": "Logout successful"}), 200
