# 🚀 Quick Start Guide

## Local Development in 5 Minutes

### Step 1: Setup Environment
```bash
# Navigate to project
cd AI-Generated-Voice-Detection-Multi-Language-

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy environment template
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env and set your API_KEY
# API_KEY=your-secret-key-here
```

### Step 3: Train Model
```bash
python scripts\train_model.py
```

Expected output:
```
============================================================
AI Voice Detection Model Training
============================================================
[INFO] Generating dummy training data...
[INFO] Dataset shape: (1000, 100)
[INFO] Training Random Forest Classifier...
[INFO] Training completed!

Model Performance
Accuracy: 0.5150 (51.50%)
[SUCCESS] Model saved!
[SUCCESS] Scaler saved!
============================================================
```

### Step 4: Start Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 5: Test API
Open a new terminal and run:
```bash
python test_client.py
```

Or test manually:
```bash
curl http://localhost:8000/health
```

---

## 🧪 Testing the API

### Method 1: Using the Test Client
```bash
# Activate virtual environment
venv\Scripts\activate

# Run comprehensive tests
python test_client.py
```

### Method 2: Using pytest
```bash
pytest tests/ -v
```

### Method 3: Using cURL
```bash
# Health check
curl http://localhost:8000/health

# Voice detection (you'll need actual audio base64)
curl -X POST http://localhost:8000/detect \
  -H "Authorization: Bearer dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d "{\"audio_data\": \"...\", \"language\": \"English\"}"
```

### Method 4: Using Python
```python
import requests
import base64

# Read your audio file
with open("sample.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

# Make request
response = requests.post(
    "http://localhost:8000/detect",
    headers={"Authorization": "Bearer dev-api-key-12345"},
    json={
        "audio_data": audio_base64,
        "language": "English"
    }
)

print(response.json())
```

---

## 🎯 Expected Response Format

```json
{
  "classification": "AI-generated",
  "confidence": 0.8542,
  "explanation": "Classified as AI-generated with high confidence (85.4%). Detected synthetic patterns in spectral features.",
  "language": "English",
  "processing_time_ms": 234.56
}
```

---

## 🐳 Docker Quick Start

### Build and Run
```bash
# Build image
docker build -t voice-detection-api .

# Run container
docker run -p 8000:8000 -e API_KEY="your-key" voice-detection-api
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🌐 API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### 2. Root Endpoint
```http
GET /
```
Same as health check.

### 3. Voice Detection
```http
POST /detect
```

**Headers:**
- `Authorization: Bearer your-api-key`
- `Content-Type: application/json`

**Body:**
```json
{
  "audio_data": "base64-encoded-audio",
  "language": "English"
}
```

**Supported Languages:**
- Tamil
- English
- Hindi
- Malayalam
- Telugu

---

## 🔥 Common Issues & Solutions

### Issue 1: Port Already in Use
```bash
# Windows - Find process using port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Issue 2: Module Not Found
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: Model Not Loaded
```bash
# Retrain the model
python scripts\train_model.py
```

### Issue 4: Authentication Failed
Check your `.env` file and ensure `API_KEY` matches the one in your request headers.

---

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| Average Processing Time | 200-500ms |
| Max Audio Length | 30 seconds |
| Max File Size | 10 MB |
| Supported Formats | MP3, WAV, FLAC |
| Concurrent Requests | Unlimited |

---

## 🎓 Next Steps

1. **Collect Real Data**: Replace dummy model with trained model on real AI/Human voice dataset
2. **Improve Model**: Experiment with different algorithms (XGBoost, Neural Networks)
3. **Add Features**: Language detection, speaker identification
4. **Deploy**: Deploy to cloud platform (Railway, Render, GCP)
5. **Monitor**: Add logging and monitoring
6. **Scale**: Add caching, load balancing

---

## 📞 Need Help?

- Check the main `README.md` for detailed documentation
- Run `python test_client.py` to verify setup
- Check logs for error messages
- Open an issue on GitHub

---

**Happy Coding! 🎉**
