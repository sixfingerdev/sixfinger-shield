import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Raise error if SECRET_KEY not set in production
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set")
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/sixfinger"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    RATELIMIT_DEFAULT = "100/minute"
    
    # Session
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    # Stripe
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Credit pricing (credits per dollar)
    CREDITS_PER_DOLLAR = 100
    CREDIT_PACKAGES = {
        "starter": {"credits": 1000, "price": 10},
        "pro": {"credits": 5000, "price": 40},
        "business": {"credits": 20000, "price": 150},
    }
    
    # API
    API_VERSION = "1.0.0"
    API_COST_PER_REQUEST = 1  # credits
    
    # Flask-Admin
    FLASK_ADMIN_SWATCH = "cerulean"
    
    # WTForms
    WTF_CSRF_TIME_LIMIT = None

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    # Allow default SECRET_KEY in development
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    # SECRET_KEY validation already in base Config

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv("FLASK_ENV", "development")
    return config.get(env, config["default"])
