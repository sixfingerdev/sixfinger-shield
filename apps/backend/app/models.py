from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class Fingerprint(Base):
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
