from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .database import engine, get_db, Base
from .models import Fingerprint
from .schemas import FingerprintRequest, FingerprintResponse, RiskScoreResponse
from .risk_scoring import calculate_risk_score
from .config import settings

# Create tables
Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="SixFinger Shield API",
    description="Bot detection & device recognition API",
    version=settings.API_VERSION
)

# Add rate limit exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "name": "SixFinger Shield API",
        "version": settings.API_VERSION,
        "status": "operational"
    }

@app.post("/api/fingerprint", response_model=FingerprintResponse)
@limiter.limit(settings.RATE_LIMIT)
def submit_fingerprint(
    request: Request,
    fingerprint_data: FingerprintRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a fingerprint for analysis
    """
    # Check if fingerprint exists
    fp = db.query(Fingerprint).filter(Fingerprint.hash == fingerprint_data.hash).first()
    
    if fp:
        # Update existing fingerprint
        fp.visit_count += 1
        
        # Recalculate risk score
        components_dict = fingerprint_data.components.model_dump()
        risk_score, is_bot, _ = calculate_risk_score(components_dict, fp.visit_count)
        fp.risk_score = risk_score
        fp.is_bot = is_bot
    else:
        # Create new fingerprint
        components_dict = fingerprint_data.components.model_dump()
        risk_score, is_bot, _ = calculate_risk_score(components_dict, 1)
        
        fp = Fingerprint(
            hash=fingerprint_data.hash,
            risk_score=risk_score,
            is_bot=is_bot,
            visit_count=1,
            canvas=components_dict.get("canvas"),
            webgl=components_dict.get("webgl"),
            audio=components_dict.get("audio"),
            fonts=components_dict.get("fonts"),
            hardware=components_dict.get("hardware"),
            screen=components_dict.get("screen"),
            browser=components_dict.get("browser"),
            timezone=components_dict.get("timezone"),
            plugins=components_dict.get("plugins"),
            touch=components_dict.get("touch"),
            battery=components_dict.get("battery"),
            network=components_dict.get("network"),
            media=components_dict.get("media"),
            color_depth=components_dict.get("colorDepth"),
            do_not_track=components_dict.get("doNotTrack")
        )
        db.add(fp)
    
    db.commit()
    db.refresh(fp)
    
    return FingerprintResponse(
        hash=fp.hash,
        risk_score=fp.risk_score,
        is_bot=fp.is_bot,
        visit_count=fp.visit_count,
        first_seen=fp.first_seen
    )

@app.get("/api/fingerprint/{hash}", response_model=FingerprintResponse)
@limiter.limit(settings.RATE_LIMIT)
def get_fingerprint(request: Request, hash: str, db: Session = Depends(get_db)):
    """
    Get fingerprint information by hash
    """
    fp = db.query(Fingerprint).filter(Fingerprint.hash == hash).first()
    
    if not fp:
        raise HTTPException(status_code=404, detail="Fingerprint not found")
    
    return FingerprintResponse(
        hash=fp.hash,
        risk_score=fp.risk_score,
        is_bot=fp.is_bot,
        visit_count=fp.visit_count,
        first_seen=fp.first_seen
    )

@app.get("/api/risk-score/{hash}", response_model=RiskScoreResponse)
@limiter.limit(settings.RATE_LIMIT)
def get_risk_score(request: Request, hash: str, db: Session = Depends(get_db)):
    """
    Get detailed risk score analysis for a fingerprint
    """
    fp = db.query(Fingerprint).filter(Fingerprint.hash == hash).first()
    
    if not fp:
        raise HTTPException(status_code=404, detail="Fingerprint not found")
    
    # Get components
    components_dict = {
        "canvas": fp.canvas,
        "webgl": fp.webgl,
        "audio": fp.audio,
        "fonts": fp.fonts,
        "hardware": fp.hardware,
        "screen": fp.screen,
        "browser": fp.browser,
        "timezone": fp.timezone,
        "plugins": fp.plugins,
        "touch": fp.touch,
        "battery": fp.battery,
        "network": fp.network,
        "media": fp.media,
        "colorDepth": fp.color_depth,
        "doNotTrack": fp.do_not_track
    }
    
    risk_score, is_bot, factors = calculate_risk_score(components_dict, fp.visit_count)
    
    confidence = min(risk_score / 100.0, 1.0)
    
    return RiskScoreResponse(
        hash=fp.hash,
        risk_score=risk_score,
        is_bot=is_bot,
        confidence=confidence,
        factors=factors
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}
