# AI-Generated Voice Detection API

A FastAPI-based REST API that detects whether a voice sample is AI-generated or human-spoken. Supports multiple languages including Tamil, English, Hindi, Malayalam, and Telugu.

## 🚀 Features

- **Multi-language Support**: Tamil, English, Hindi, Malayalam, Telugu
- **Base64 Audio Input**: Easy integration with web/mobile apps
- **Advanced Feature Extraction**: MFCC, spectral, temporal features
- **REST API**: Simple HTTP endpoints
- **Authentication**: API key-based security
- **Docker Support**: Easy deployment
- **Comprehensive Testing**: pytest test suite

## 📋 System Architecture

```
Client → FastAPI → Audio Processor → Feature Extractor → ML Model → Response
```

## 🛠️ Installation

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd AI-Generated-Voice-Detection-Multi-Language-
```

2. **Create virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
copy .env.example .env
# Edit .env and set your API_KEY
```

5. **Train the model (generates dummy model)**
```bash
python scripts/train_model.py
```

6. **Run the server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Or build manually**
```bash
docker build -t voice-detection-api .
docker run -p 8000:8000 -e API_KEY="your-secret-key" voice-detection-api
```

## 📚 API Documentation

### Endpoints

#### Health Check
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

#### Voice Detection
```http
POST /detect
```

**Headers:**
```
Authorization: Bearer your-api-key
Content-Type: application/json
```

**Request Body:**
```json
{
  "audio_data": "base64-encoded-audio-file",
  "language": "English"
}
```

**Response:**
```json
{
  "classification": "AI-generated",
  "confidence": 0.87,
  "explanation": "Classified as AI-generated with high confidence (87.0%). Detected synthetic patterns in spectral features.",
  "language": "English",
  "processing_time_ms": 234.56
}
```

### Supported Languages
- Tamil
- English
- Hindi
- Malayalam
- Telugu

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🔧 Configuration

Edit `.env` file or set environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| API_KEY | - | Your secret API key |
| LOG_LEVEL | INFO | Logging level |
| SAMPLE_RATE | 16000 | Audio sample rate (Hz) |
| MAX_AUDIO_LENGTH | 30 | Max audio duration (seconds) |
| MAX_FILE_SIZE | 10485760 | Max file size (bytes) |

## 📦 Project Structure

```
AI-Generated-Voice-Detection-Multi-Language-/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration
│   ├── audio_processor.py   # Audio handling
│   ├── feature_extractor.py # Feature extraction
│   └── predictor.py         # ML inference
├── models/
│   ├── __init__.py
│   ├── classifier.pkl       # Trained model
│   └── scaler.pkl           # Feature scaler
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API tests
├── scripts/
│   └── train_model.py       # Model training
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🎯 Usage Example

### Python
```python
import requests
import base64

# Read audio file
with open("sample.mp3", "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Make request
response = requests.post(
    "http://localhost:8000/detect",
    headers={
        "Authorization": "Bearer your-api-key",
        "Content-Type": "application/json"
    },
    json={
        "audio_data": audio_base64,
        "language": "English"
    }
)

print(response.json())
```

### cURL
```bash
# Encode audio file
BASE64_AUDIO=$(base64 -w 0 sample.mp3)

# Make request
curl -X POST "http://localhost:8000/detect" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d "{\"audio_data\": \"$BASE64_AUDIO\", \"language\": \"English\"}"
```

### JavaScript (Browser/Node.js)
```javascript
// Read file and convert to base64
const fileInput = document.getElementById('audioFile');
const file = fileInput.files[0];
const reader = new FileReader();

reader.onloadend = async () => {
  const base64Audio = reader.result.split(',')[1];
  
  const response = await fetch('http://localhost:8000/detect', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer your-api-key',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      audio_data: base64Audio,
      language: 'English'
    })
  });
  
  const result = await response.json();
  console.log(result);
};

reader.readAsDataURL(file);
```

## 🔐 Security

- API key authentication required for all endpoints
- Input validation for audio data and language
- File size limits to prevent DoS attacks
- CORS enabled (configure for production)

## 🚀 Deployment

### Cloud Platforms

#### Railway.app
```bash
railway login
railway init
railway up
```

#### Render.com
1. Connect GitHub repository
2. Select "Docker" as environment
3. Set environment variables
4. Deploy

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/voice-detection-api
gcloud run deploy voice-detection-api \
  --image gcr.io/PROJECT_ID/voice-detection-api \
  --platform managed \
  --allow-unauthenticated
```

## 📈 Performance

- Average processing time: ~200-500ms
- Supports concurrent requests
- Automatic request validation
- Error handling and logging

## 🔄 Model Training

The current model is a placeholder. To train with real data:

1. Collect labeled dataset (Human vs AI voices)
2. Extract features using `feature_extractor.py`
3. Update `scripts/train_model.py` with your dataset
4. Train and evaluate:
```bash
python scripts/train_model.py
```

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, Librosa, and Scikit-learn**
