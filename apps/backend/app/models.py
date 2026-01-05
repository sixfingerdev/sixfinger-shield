from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    credits = relationship("Credit", back_populates="user", uselist=False, cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Set user password with hashing"""
        # Basic password validation
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.username}>"

class Credit(db.Model):
    __tablename__ = "credits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    balance = Column(Integer, default=0)
    total_purchased = Column(Integer, default=0)
    total_used = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="credits")
    
    def __repr__(self):
        return f"<Credit user_id={self.user_id} balance={self.balance}>"

class Transaction(db.Model):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String(50), nullable=False)  # 'purchase', 'usage', 'refund'
    description = Column(Text, nullable=True)
    stripe_payment_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction {self.transaction_type} amount={self.amount}>"

class APIKey(db.Model):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey {self.name}>"

class Fingerprint(db.Model):
    __tablename__ = "fingerprints"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String(32), unique=True, index=True, nullable=False)
    risk_score = Column(Float, default=0.0)
    is_bot = Column(Boolean, default=False)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), onupdate=func.now())
    visit_count = Column(Integer, default=1)
    
    # Component data (simplified storage)
    canvas = Column(String, nullable=True)
    webgl = Column(String, nullable=True)
    audio = Column(String, nullable=True)
    fonts = Column(String, nullable=True)
    hardware = Column(String, nullable=True)
    screen = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    plugins = Column(String, nullable=True)
    touch = Column(String, nullable=True)
    battery = Column(String, nullable=True)
    network = Column(String, nullable=True)
    media = Column(String, nullable=True)
    color_depth = Column(String, nullable=True)
    do_not_track = Column(String, nullable=True)
