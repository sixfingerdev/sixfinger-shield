"""Flask-Admin configuration"""
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
from .models import User, Credit, Transaction, APIKey, Fingerprint
from .database import db

class SecureModelView(ModelView):
    """Base model view with authentication"""
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_blueprint.login', next=request.url))

class SecureAdminIndexView(AdminIndexView):
    """Secure admin index view"""
    
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('auth_blueprint.login'))
        
        # Get statistics
        user_count = User.query.count()
        fingerprint_count = Fingerprint.query.count()
        total_credits_purchased = db.session.query(
            db.func.sum(Credit.total_purchased)
        ).scalar() or 0
        total_credits_used = db.session.query(
            db.func.sum(Credit.total_used)
        ).scalar() or 0
        
        return self.render(
            'admin/index.html',
            user_count=user_count,
            fingerprint_count=fingerprint_count,
            total_credits_purchased=total_credits_purchased,
            total_credits_used=total_credits_used
        )

class UserAdmin(SecureModelView):
    """User admin view"""
    column_list = ['id', 'username', 'email', 'is_admin', 'is_active', 'created_at']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_admin', 'is_active', 'created_at']
    form_excluded_columns = ['password_hash', 'credits', 'transactions', 'api_keys']
    
    can_create = True
    can_edit = True
    can_delete = True

class CreditAdmin(SecureModelView):
    """Credit admin view"""
    column_list = ['id', 'user_id', 'balance', 'total_purchased', 'total_used', 'updated_at']
    column_searchable_list = ['user_id']
    column_filters = ['balance', 'updated_at']
    
    can_create = False
    can_edit = True
    can_delete = False

class TransactionAdmin(SecureModelView):
    """Transaction admin view"""
    column_list = ['id', 'user_id', 'amount', 'transaction_type', 'description', 'created_at']
    column_searchable_list = ['user_id', 'description', 'stripe_payment_id']
    column_filters = ['transaction_type', 'created_at']
    
    can_create = False
    can_edit = False
    can_delete = False

class APIKeyAdmin(SecureModelView):
    """API Key admin view"""
    column_list = ['id', 'user_id', 'name', 'is_active', 'created_at', 'last_used']
    column_searchable_list = ['name', 'key']
    column_filters = ['is_active', 'created_at', 'last_used']
    
    can_create = False
    can_edit = True
    can_delete = True

class FingerprintAdmin(SecureModelView):
    """Fingerprint admin view"""
    column_list = ['id', 'hash', 'risk_score', 'is_bot', 'visit_count', 'first_seen', 'last_seen']
    column_searchable_list = ['hash']
    column_filters = ['is_bot', 'risk_score', 'first_seen']
    
    can_create = False
    can_edit = False
    can_delete = True

def init_admin(app):
    """Initialize Flask-Admin"""
    admin = Admin(
        app,
        name='SixFinger Admin',
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView()
    )
    
    # Add views
    admin.add_view(UserAdmin(User, db.session, name='Users'))
    admin.add_view(CreditAdmin(Credit, db.session, name='Credits'))
    admin.add_view(TransactionAdmin(Transaction, db.session, name='Transactions'))
    admin.add_view(APIKeyAdmin(APIKey, db.session, name='API Keys'))
    admin.add_view(FingerprintAdmin(Fingerprint, db.session, name='Fingerprints'))
    
    return admin
