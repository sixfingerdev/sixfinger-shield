"""API endpoints for fingerprint analysis"""
from flask import Blueprint, request, jsonify, current_app
from ..models import Fingerprint, db
from ..risk_scoring import calculate_risk_score
from ..auth import require_api_key, require_credits
from ..schemas import FingerprintRequest, FingerprintResponse, RiskScoreResponse

api_bp = Blueprint('api_blueprint', __name__)

@api_bp.route('/fingerprint', methods=['POST'])
@require_api_key
@require_credits(cost=1)
def submit_fingerprint():
    """
    Submit a fingerprint for analysis
    Requires API key and deducts 1 credit
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'hash' not in data or 'components' not in data:
            return jsonify({"error": "Invalid request format"}), 400
        
        fingerprint_hash = data['hash']
        components = data['components']
        
        # Validate hash length
        if len(fingerprint_hash) != 32:
            return jsonify({"error": "Hash must be 32 characters"}), 400
        
        # Check if fingerprint exists
        fp = Fingerprint.query.filter_by(hash=fingerprint_hash).first()
        
        if fp:
            # Update existing fingerprint
            fp.visit_count += 1
            
            # Recalculate risk score
            risk_score, is_bot, _ = calculate_risk_score(components, fp.visit_count)
            fp.risk_score = risk_score
            fp.is_bot = is_bot
        else:
            # Create new fingerprint
            risk_score, is_bot, _ = calculate_risk_score(components, 1)
            
            fp = Fingerprint(
                hash=fingerprint_hash,
                risk_score=risk_score,
                is_bot=is_bot,
                visit_count=1,
                canvas=components.get("canvas"),
                webgl=components.get("webgl"),
                audio=components.get("audio"),
                fonts=components.get("fonts"),
                hardware=components.get("hardware"),
                screen=components.get("screen"),
                browser=components.get("browser"),
                timezone=components.get("timezone"),
                plugins=components.get("plugins"),
                touch=components.get("touch"),
                battery=components.get("battery"),
                network=components.get("network"),
                media=components.get("media"),
                color_depth=components.get("colorDepth"),
                do_not_track=components.get("doNotTrack")
            )
            db.session.add(fp)
        
        db.session.commit()
        
        # Return response
        response = {
            "hash": fp.hash,
            "risk_score": fp.risk_score,
            "is_bot": fp.is_bot,
            "visit_count": fp.visit_count,
            "first_seen": fp.first_seen.isoformat() if fp.first_seen else None,
            "credits_used": request.credits_used,
            "credits_remaining": request.credits_remaining
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        current_app.logger.error(f"Error processing fingerprint: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/fingerprint/<hash>', methods=['GET'])
@require_api_key
def get_fingerprint(hash):
    """
    Get fingerprint information by hash
    Requires API key (no credit cost for lookup)
    """
    if len(hash) != 32:
        return jsonify({"error": "Hash must be 32 characters"}), 400
    
    fp = Fingerprint.query.filter_by(hash=hash).first()
    
    if not fp:
        return jsonify({"error": "Fingerprint not found"}), 404
    
    response = {
        "hash": fp.hash,
        "risk_score": fp.risk_score,
        "is_bot": fp.is_bot,
        "visit_count": fp.visit_count,
        "first_seen": fp.first_seen.isoformat() if fp.first_seen else None,
        "last_seen": fp.last_seen.isoformat() if fp.last_seen else None
    }
    
    return jsonify(response), 200

@api_bp.route('/risk-score/<hash>', methods=['GET'])
@require_api_key
def get_risk_score(hash):
    """
    Get detailed risk score analysis for a fingerprint
    Requires API key (no credit cost for lookup)
    """
    if len(hash) != 32:
        return jsonify({"error": "Hash must be 32 characters"}), 400
    
    fp = Fingerprint.query.filter_by(hash=hash).first()
    
    if not fp:
        return jsonify({"error": "Fingerprint not found"}), 404
    
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
    
    response = {
        "hash": fp.hash,
        "risk_score": risk_score,
        "is_bot": is_bot,
        "confidence": confidence,
        "factors": factors
    }
    
    return jsonify(response), 200
