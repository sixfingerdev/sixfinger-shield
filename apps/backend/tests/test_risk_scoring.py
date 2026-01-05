import pytest
from app.risk_scoring import calculate_risk_score

def test_calculate_risk_score_normal():
    components = {
        "canvas": "data:image/png;base64,mock",
        "webgl": "Intel Inc.~ANGLE",
        "audio": "48000_2048",
        "fonts": "Arial,Verdana",
        "hardware": "cores:8_mem:8_gpu:Intel",
        "screen": "1920x1080_1920x1040_24",
        "browser": "Mozilla/5.0",
        "timezone": "America/New_York_300",
        "plugins": "Chrome PDF Plugin",
        "touch": "0_false",
        "battery": "true_100",
        "network": "4g_10_50",
        "media": "audioinput,videoinput",
        "colorDepth": "24_2",
        "doNotTrack": "unknown"
    }
    
    score, is_bot, factors = calculate_risk_score(components, 1)
    
    assert score < 60
    assert not is_bot
    assert isinstance(factors, dict)

def test_calculate_risk_score_bot_indicators():
    components = {
        "canvas": "unsupported",
        "webgl": "unsupported",
        "audio": "error",
        "fonts": "",
        "hardware": "unknown",
        "screen": "800x600_800x600_24",
        "browser": "HeadlessChrome",
        "timezone": "UTC_0",
        "plugins": "none",
        "touch": "0_false",
        "battery": "unsupported",
        "network": "unsupported",
        "media": "error",
        "colorDepth": "24_1",
        "doNotTrack": "1"
    }
    
    score, is_bot, factors = calculate_risk_score(components, 1)
    
    assert score >= 60
    assert is_bot
    assert len(factors) > 0

def test_calculate_risk_score_rapid_visits():
    components = {
        "canvas": "data:image/png;base64,mock",
        "webgl": "Intel Inc.~ANGLE",
        "audio": "48000_2048",
        "fonts": "Arial",
        "hardware": "cores:8",
        "screen": "1920x1080",
        "browser": "Mozilla/5.0",
        "timezone": "America/New_York",
        "plugins": "plugin",
        "touch": "0_false",
        "battery": "true_100",
        "network": "4g",
        "media": "audioinput",
        "colorDepth": "24_2",
        "doNotTrack": "0"
    }
    
    score1, _, _ = calculate_risk_score(components, 1)
    score2, _, factors2 = calculate_risk_score(components, 20)
    
    assert score2 > score1
    assert "rapid_visits" in factors2
