import pytest
from fastapi.testclient import TestClient
import base64
import numpy as np
import soundfile as sf
import io
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.config import get_settings

settings = get_settings()
client = TestClient(app)

def create_dummy_audio_base64(duration=1.0, sample_rate=16000):
    """Create a dummy audio file and return base64 encoding"""
    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    # Convert to bytes
    audio_io = io.BytesIO()
    sf.write(audio_io, audio, sample_rate, format='WAV')
    audio_bytes = audio_io.getvalue()
    
    # Encode to base64
    return base64.b64encode(audio_bytes).decode('utf-8')

class TestAPI:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_detect_without_auth(self):
        """Test detection without authentication"""
        audio_base64 = create_dummy_audio_base64()
        response = client.post(
            "/detect",
            json={
                "audio_data": audio_base64,
                "language": "English"
            }
        )
        assert response.status_code == 401
    
    def test_detect_with_invalid_auth(self):
        """Test detection with invalid authentication"""
        audio_base64 = create_dummy_audio_base64()
        response = client.post(
            "/detect",
            json={
                "audio_data": audio_base64,
                "language": "English"
            },
            headers={"Authorization": "Bearer wrong-key"}
        )
        assert response.status_code == 403
    
    def test_detect_with_valid_auth(self):
        """Test detection with valid authentication"""
        audio_base64 = create_dummy_audio_base64()
        response = client.post(
            "/detect",
            json={
                "audio_data": audio_base64,
                "language": "English"
            },
            headers={"Authorization": f"Bearer {settings.API_KEY}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert "confidence" in data
        assert "explanation" in data
        assert data["language"] == "English"
        assert 0 <= data["confidence"] <= 1
    
    def test_all_languages(self):
        """Test all supported languages"""
        languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
        audio_base64 = create_dummy_audio_base64()
        
        for lang in languages:
            response = client.post(
                "/detect",
                json={
                    "audio_data": audio_base64,
                    "language": lang
                },
                headers={"Authorization": f"Bearer {settings.API_KEY}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["language"] == lang
    
    def test_invalid_base64(self):
        """Test with invalid base64 data"""
        response = client.post(
            "/detect",
            json={
                "audio_data": "not-valid-base64!!!",
                "language": "English"
            },
            headers={"Authorization": f"Bearer {settings.API_KEY}"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_invalid_language(self):
        """Test with invalid language"""
        audio_base64 = create_dummy_audio_base64()
        response = client.post(
            "/detect",
            json={
                "audio_data": audio_base64,
                "language": "InvalidLanguage"
            },
            headers={"Authorization": f"Bearer {settings.API_KEY}"}
        )
        assert response.status_code == 422  # Validation error
