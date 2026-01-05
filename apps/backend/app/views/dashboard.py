"""Dashboard views"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from ..models import Credit, Transaction, APIKey, Fingerprint
from ..database import db
from ..auth import generate_api_key
from ..forms import APIKeyForm
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard_blueprint', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard"""
    # Get user's credit info
    credit = Credit.query.filter_by(user_id=current_user.id).first()
    
    if not credit:
        credit = Credit(user_id=current_user.id, balance=0, total_purchased=0, total_used=0)
        db.session.add(credit)
        db.session.commit()
    
    # Get recent transactions
    recent_transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(Transaction.created_at.desc()).limit(10).all()
    
    # Get API keys
    api_keys = APIKey.query.filter_by(user_id=current_user.id).all()
    
    # Get usage statistics
    total_api_calls = Transaction.query.filter_by(
        user_id=current_user.id,
        transaction_type='usage'
    ).count()
    
    return render_template(
        'dashboard/index.html',
        credit=credit,
        recent_transactions=recent_transactions,
        api_keys=api_keys,
        total_api_calls=total_api_calls
    )

@dashboard_bp.route('/api-keys', methods=['GET', 'POST'])
@login_required
def api_keys():
    """Manage API keys"""
    form = APIKeyForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # Create new API key
        new_key = APIKey(
            user_id=current_user.id,
            key=generate_api_key(),
            name=form.name.data,
            is_active=True
        )
        db.session.add(new_key)
        db.session.commit()
        
        return render_template('dashboard/api_key_created.html', api_key=new_key)
    
    keys = APIKey.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard/api_keys.html', keys=keys, form=form)

@dashboard_bp.route('/api-keys/<int:key_id>/delete', methods=['POST'])
@login_required
def delete_api_key(key_id):
    """Delete an API key"""
    api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
    
    if api_key:
        db.session.delete(api_key)
        db.session.commit()
        return jsonify({"message": "API key deleted"}), 200
    
    return jsonify({"error": "API key not found"}), 404

@dashboard_bp.route('/api-keys/<int:key_id>/toggle', methods=['POST'])
@login_required
def toggle_api_key(key_id):
    """Toggle API key active status"""
    api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
    
    if api_key:
        api_key.is_active = not api_key.is_active
        db.session.commit()
        return jsonify({
            "message": "API key updated",
            "is_active": api_key.is_active
        }), 200
    
    return jsonify({"error": "API key not found"}), 404

@dashboard_bp.route('/usage', methods=['GET'])
@login_required
def usage():
    """View detailed usage statistics"""
    # Get usage by day (last 30 days)
    usage_data = db.session.query(
        func.date(Transaction.created_at).label('date'),
        func.sum(Transaction.amount).label('credits_used')
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'usage',
        Transaction.created_at >= func.date('now', '-30 days')
    ).group_by(func.date(Transaction.created_at)).all()
    
    return render_template('dashboard/usage.html', usage_data=usage_data)

# API endpoints
@dashboard_bp.route('/api/stats', methods=['GET'])
@login_required
def api_stats():
    """Get dashboard statistics (API endpoint)"""
    credit = Credit.query.filter_by(user_id=current_user.id).first()
    
    total_api_calls = Transaction.query.filter_by(
        user_id=current_user.id,
        transaction_type='usage'
    ).count()
    
    active_api_keys = APIKey.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).count()
    
    return jsonify({
        "credits": {
            "balance": credit.balance if credit else 0,
            "total_purchased": credit.total_purchased if credit else 0,
            "total_used": credit.total_used if credit else 0
        },
        "api_calls": total_api_calls,
        "active_keys": active_api_keys
    }), 200
