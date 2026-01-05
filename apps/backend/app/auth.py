"""Authentication and authorization utilities"""
from functools import wraps
from flask import jsonify, request, session
from flask_login import current_user
from .models import User, APIKey, Credit
from .database import db
import secrets

def generate_api_key():
    """Generate a secure API key"""
    return secrets.token_urlsafe(48)

def require_api_key(f):
    """Decorator to require API key for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({"error": "API key required"}), 401
        
        # Check API key
        key_obj = APIKey.query.filter_by(key=api_key, is_active=True).first()
        if not key_obj:
            return jsonify({"error": "Invalid API key"}), 401
        
        # Update last used
        key_obj.last_used = db.func.now()
        db.session.commit()
        
        # Check user is active
        user = User.query.get(key_obj.user_id)
        if not user or not user.is_active:
            return jsonify({"error": "User account is not active"}), 401
        
        # Attach user to request
        request.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_credits(cost=1):
    """Decorator to require credits for API usage"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(request, 'current_user', None)
            
            if not user:
                return jsonify({"error": "Authentication required"}), 401
            
            # Check credit balance
            credit = Credit.query.filter_by(user_id=user.id).first()
            if not credit or credit.balance < cost:
                return jsonify({
                    "error": "Insufficient credits",
                    "required": cost,
                    "balance": credit.balance if credit else 0
                }), 402
            
            # Deduct credits
            credit.balance -= cost
            credit.total_used += cost
            
            # Record transaction
            from .models import Transaction
            transaction = Transaction(
                user_id=user.id,
                amount=-cost,
                transaction_type='usage',
                description=f'API call: {request.endpoint}'
            )
            db.session.add(transaction)
            db.session.commit()
            
            # Attach credit info to request
            request.credits_used = cost
            request.credits_remaining = credit.balance
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "Authentication required"}), 401
        
        if not current_user.is_admin:
            return jsonify({"error": "Admin privileges required"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
