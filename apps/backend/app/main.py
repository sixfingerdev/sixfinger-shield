"""Main Flask application"""
from flask import Flask, jsonify, request, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

from .config import get_config
from .models import db, User
from .admin import init_admin

# Initialize extensions
login_manager = LoginManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name=None):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name:
        app.config.from_object(config_name)
    else:
        app.config.from_object(get_config())
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app)
    
    # Initialize admin
    init_admin(app)
    
    # Configure login manager
    login_manager.login_view = 'auth_blueprint.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Context processor for templates
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.now()}
    
    # Register blueprints
    from .views.auth import auth_bp
    from .views.api import api_bp
    from .views.payment import payment_bp
    from .views.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(payment_bp, url_prefix='/payment')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    # Root routes
    @app.route('/')
    def index():
        return jsonify({
            "name": "SixFinger Shield API",
            "version": app.config.get('API_VERSION'),
            "status": "operational",
            "documentation": "/docs"
        })
    
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

# For backward compatibility and direct running
app = create_app()

if __name__ == '__main__':
    import os
    # Use FLASK_DEBUG environment variable (Flask 2.2+)
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, host='0.0.0.0', port=5000)
