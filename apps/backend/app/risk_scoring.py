"""
Risk scoring algorithm for fingerprint analysis
"""

def calculate_risk_score(components: dict, visit_count: int) -> tuple[float, bool, dict]:
    """
    Calculate risk score based on fingerprint components
    Returns: (risk_score, is_bot, factors)
    """
    factors = {}
    score = 0.0
    
    # Check for automation indicators
    if components.get("webgl") in ["unsupported", "error"]:
        score += 15
        factors["webgl_missing"] = True
    
    if components.get("audio") in ["unsupported", "error"]:
        score += 10
        factors["audio_missing"] = True
    
    if components.get("canvas") in ["unsupported", "error"]:
        score += 15
        factors["canvas_missing"] = True
    
    # Check for suspicious hardware
    hardware = components.get("hardware", "")
    if "unknown" in hardware.lower():
        score += 10
        factors["hardware_unknown"] = True
    
    # Check for headless browser indicators
    plugins = components.get("plugins", "")
    if plugins in ["none", "error", ""]:
        score += 5
        factors["no_plugins"] = True
    
    # Check for touch support on desktop
    touch = components.get("touch", "")
    if touch.startswith("0_"):
        score += 2
        factors["no_touch"] = True
    
    # Check for unusual screen resolution
    screen = components.get("screen", "")
    if "800x600" in screen or "1024x768" in screen:
        score += 8
        factors["suspicious_screen"] = True
    
    # Battery API missing (common in headless)
    if components.get("battery") in ["unsupported", "error"]:
        score += 5
        factors["battery_missing"] = True
    
    # Media devices missing
    if components.get("media") in ["unsupported", "error", ""]:
        score += 10
        factors["media_missing"] = True
    
    # Font detection issues
    fonts = components.get("fonts", "")
    if not fonts or fonts == "unsupported":
        score += 10
        factors["fonts_missing"] = True
    
    # Do Not Track enabled (privacy conscious or bot)
    dnt = components.get("doNotTrack", "")
    if dnt == "1":
        score += 3
        factors["dnt_enabled"] = True
    
    # Rapid visits indicator
    if visit_count > 10:
        score += min(visit_count, 30)
        factors["rapid_visits"] = visit_count
    
    # Cap score at 100
    risk_score = min(score, 100.0)
    
    # Determine if bot (threshold at 60)
    is_bot = risk_score >= 60.0
    
    return risk_score, is_bot, factors
