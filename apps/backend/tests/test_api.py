import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def sample_fingerprint():
    return {
        "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
        "components": {
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
    }

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_submit_fingerprint(sample_fingerprint):
    response = client.post("/api/fingerprint", json=sample_fingerprint)
    assert response.status_code == 200
    data = response.json()
    assert data["hash"] == sample_fingerprint["hash"]
    assert "risk_score" in data
    assert "is_bot" in data
    assert data["visit_count"] == 1

def test_get_fingerprint(sample_fingerprint):
    # First submit
    client.post("/api/fingerprint", json=sample_fingerprint)
    
    # Then get
    response = client.get(f"/api/fingerprint/{sample_fingerprint['hash']}")
    assert response.status_code == 200
    data = response.json()
    assert data["hash"] == sample_fingerprint["hash"]

def test_get_risk_score(sample_fingerprint):
    # First submit
    client.post("/api/fingerprint", json=sample_fingerprint)
    
    # Then get risk score
    response = client.get(f"/api/risk-score/{sample_fingerprint['hash']}")
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "is_bot" in data
    assert "confidence" in data
    assert "factors" in data

def test_fingerprint_visit_count(sample_fingerprint):
    # Use a different hash to avoid conflicts with other tests
    sample_fingerprint["hash"] = "unique_visit_count_test_hash_32c"
    
    # Submit twice
    response1 = client.post("/api/fingerprint", json=sample_fingerprint)
    response2 = client.post("/api/fingerprint", json=sample_fingerprint)
    
    assert response1.json()["visit_count"] == 1
    assert response2.json()["visit_count"] == 2

def test_get_nonexistent_fingerprint():
    response = client.get("/api/fingerprint/nonexistenthash12345678901234")
    assert response.status_code == 404
