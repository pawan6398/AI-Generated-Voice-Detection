"""
Test client for the Voice Detection API
This script tests the API endpoints with sample audio
"""

import requests
import base64
import numpy as np
import soundfile as sf
import io
import json

# Configuration
API_URL = "https://ai-generated-voice-detection-0ra8.onrender.com"
API_KEY = "dev-api-key-12345"

def create_test_audio(duration=2.0, sample_rate=16000, frequency=440):
    """Create a test audio signal (sine wave)"""
    print(f"[INFO] Generating {duration}s test audio at {frequency}Hz...")
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.sin(2 * np.pi * frequency * t) * 0.5  # 440 Hz sine wave
    
    # Convert to WAV format in memory
    audio_io = io.BytesIO()
    sf.write(audio_io, audio, sample_rate, format='WAV')
    audio_bytes = audio_io.getvalue()
    
    # Encode to base64
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return audio_base64

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_voice_detection(language="English"):
    """Test the voice detection endpoint"""
    print("\n" + "="*60)
    print(f"Testing Voice Detection - Language: {language}")
    print("="*60)
    
    try:
        # Create test audio
        audio_base64 = create_test_audio()
        
        # Make request
        print(f"[INFO] Sending request to {API_URL}/detect...")
        response = requests.post(
            f"{API_URL}/detect",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "audio_data": audio_base64,
                "language": language
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "─"*60)
            print("RESULT")
            print("─"*60)
            print(f"Classification:  {result['classification']}")
            print(f"Confidence:      {result['confidence']:.2%}")
            print(f"Explanation:     {result['explanation']}")
            print(f"Language:        {result['language']}")
            print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
            print("─"*60)
            return True
        else:
            print(f"[ERROR] {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_all_languages():
    """Test all supported languages"""
    print("\n" + "="*60)
    print("Testing All Supported Languages")
    print("="*60)
    
    languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    results = {}
    
    for lang in languages:
        print(f"\n[INFO] Testing {lang}...")
        success = test_voice_detection(lang)
        results[lang] = "✓ PASS" if success else "✗ FAIL"
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for lang, status in results.items():
        print(f"{lang:15} {status}")
    print("="*60)

def test_authentication():
    """Test API authentication"""
    print("\n" + "="*60)
    print("Testing Authentication")
    print("="*60)
    
    audio_base64 = create_test_audio()
    
    # Test without auth
    print("\n[TEST] Request without authentication...")
    response = requests.post(
        f"{API_URL}/detect",
        json={
            "audio_data": audio_base64,
            "language": "English"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Expected: 401 - {'✓ PASS' if response.status_code == 401 else '✗ FAIL'}")
    
    # Test with wrong auth
    print("\n[TEST] Request with invalid API key...")
    response = requests.post(
        f"{API_URL}/detect",
        headers={"Authorization": "Bearer wrong-key"},
        json={
            "audio_data": audio_base64,
            "language": "English"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Expected: 403 - {'✓ PASS' if response.status_code == 403 else '✗ FAIL'}")
    
    # Test with correct auth
    print("\n[TEST] Request with valid API key...")
    response = requests.post(
        f"{API_URL}/detect",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "audio_data": audio_base64,
            "language": "English"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Expected: 200 - {'✓ PASS' if response.status_code == 200 else '✗ FAIL'}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI VOICE DETECTION API - TEST CLIENT")
    print("="*60)
    print(f"API URL: {API_URL}")
    print(f"API Key: {API_KEY[:20]}...")
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n[WARNING] API might not be running!")
        print("Please start the API server with:")
        print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Test 2: Authentication
    test_authentication()
    
    # Test 3: Voice Detection (Single)
    test_voice_detection("English")
    
    # Test 4: All Languages
    test_all_languages()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    main()
