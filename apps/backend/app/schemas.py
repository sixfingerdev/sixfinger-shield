from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FingerprintComponents(BaseModel):
    canvas: str
    webgl: str
    audio: str
    fonts: str
    hardware: str
    screen: str
    browser: str
    timezone: str
    plugins: str
    touch: str
    battery: str
    network: str
    media: str
    colorDepth: str
    doNotTrack: str

class FingerprintRequest(BaseModel):
    hash: str = Field(..., min_length=32, max_length=32)
    components: FingerprintComponents

class FingerprintResponse(BaseModel):
    hash: str
    risk_score: float
    is_bot: bool
    visit_count: int
    first_seen: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RiskScoreResponse(BaseModel):
    hash: str
    risk_score: float
    is_bot: bool
    confidence: float
    factors: dict
