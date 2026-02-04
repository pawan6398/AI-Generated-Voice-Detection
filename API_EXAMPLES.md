# 🔧 API Usage Examples

Complete examples for integrating with the AI Voice Detection API.

---

## 📋 Table of Contents

1. [Python Examples](#python-examples)
2. [JavaScript Examples](#javascript-examples)
3. [cURL Examples](#curl-examples)
4. [Postman Examples](#postman-examples)
5. [Integration Patterns](#integration-patterns)

---

## 🐍 Python Examples

### Example 1: Basic Usage

```python
import requests
import base64

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "dev-api-key-12345"

# Read audio file
with open("sample.mp3", "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Make request
response = requests.post(
    f"{API_URL}/detect",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "audio_data": audio_base64,
        "language": "English"
    }
)

# Handle response
if response.status_code == 200:
    result = response.json()
    print(f"Classification: {result['classification']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Explanation: {result['explanation']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Example 2: Batch Processing

```python
import requests
import base64
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "http://localhost:8000"
API_KEY = "dev-api-key-12345"

def process_audio_file(file_path, language="English"):
    """Process a single audio file"""
    with open(file_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    response = requests.post(
        f"{API_URL}/detect",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"audio_data": audio_base64, "language": language}
    )
    
    return {
        "file": file_path.name,
        "result": response.json() if response.status_code == 200 else None,
        "error": None if response.status_code == 200 else response.text
    }

def batch_process(audio_folder, language="English", max_workers=5):
    """Process multiple audio files concurrently"""
    audio_files = list(Path(audio_folder).glob("*.mp3"))
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_audio_file, file, language): file 
            for file in audio_files
        }
        
        for future in as_completed(futures):
            results.append(future.result())
    
    return results

# Usage
results = batch_process("audio_samples/", language="English")
for result in results:
    print(f"{result['file']}: {result['result']['classification']}")
```

### Example 3: With Error Handling

```python
import requests
import base64
import logging
from typing import Optional, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceDetectionClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    def detect(self, audio_file: str, language: str = "English") -> Optional[Dict]:
        """
        Detect if audio is AI-generated or human
        
        Args:
            audio_file: Path to audio file
            language: Language of audio
            
        Returns:
            Detection result or None if error
        """
        try:
            # Read and encode audio
            with open(audio_file, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Make request
            logger.info(f"Processing {audio_file}...")
            response = requests.post(
                f"{self.api_url}/detect",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "audio_data": audio_base64,
                    "language": language
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(
                f"Result: {result['classification']} "
                f"({result['confidence']:.2%} confidence)"
            )
            
            return result
            
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
        except FileNotFoundError:
            logger.error(f"File not found: {audio_file}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        return None

# Usage
client = VoiceDetectionClient(
    api_url="http://localhost:8000",
    api_key="dev-api-key-12345"
)

result = client.detect("sample.mp3", language="English")
if result:
    print(f"Classification: {result['classification']}")
```

---

## 🌐 JavaScript Examples

### Example 1: Browser (Vanilla JS)

```javascript
// HTML
<input type="file" id="audioFile" accept="audio/*">
<button onclick="detectVoice()">Detect Voice</button>
<div id="result"></div>

// JavaScript
const API_URL = "http://localhost:8000";
const API_KEY = "dev-api-key-12345";

async function detectVoice() {
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select an audio file');
        return;
    }
    
    try {
        // Convert file to base64
        const base64Audio = await fileToBase64(file);
        
        // Make API request
        const response = await fetch(`${API_URL}/detect`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                audio_data: base64Audio,
                language: 'English'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        // Display result
        document.getElementById('result').innerHTML = `
            <h3>Result:</h3>
            <p><strong>Classification:</strong> ${result.classification}</p>
            <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(2)}%</p>
            <p><strong>Explanation:</strong> ${result.explanation}</p>
            <p><strong>Language:</strong> ${result.language}</p>
            <p><strong>Processing Time:</strong> ${result.processing_time_ms.toFixed(2)}ms</p>
        `;
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            // Remove data URL prefix
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}
```

### Example 2: Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

const API_URL = "http://localhost:8000";
const API_KEY = "dev-api-key-12345";

async function detectVoice(audioFilePath, language = 'English') {
    try {
        // Read and encode audio file
        const audioBuffer = fs.readFileSync(audioFilePath);
        const audioBase64 = audioBuffer.toString('base64');
        
        // Make API request
        const response = await axios.post(
            `${API_URL}/detect`,
            {
                audio_data: audioBase64,
                language: language
            },
            {
                headers: {
                    'Authorization': `Bearer ${API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        
        console.log('Classification:', response.data.classification);
        console.log('Confidence:', (response.data.confidence * 100).toFixed(2) + '%');
        console.log('Explanation:', response.data.explanation);
        
        return response.data;
        
    } catch (error) {
        if (error.response) {
            console.error('API Error:', error.response.status, error.response.data);
        } else {
            console.error('Error:', error.message);
        }
        throw error;
    }
}

// Usage
detectVoice('sample.mp3', 'English')
    .then(result => console.log('Success:', result))
    .catch(error => console.error('Failed:', error));
```

### Example 3: React

```javascript
import React, { useState } from 'react';
import axios from 'axios';

const API_URL = "http://localhost:8000";
const API_KEY = "dev-api-key-12345";

function VoiceDetector() {
    const [file, setFile] = useState(null);
    const [language, setLanguage] = useState('English');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setResult(null);
        setError(null);
    };
    
    const detectVoice = async () => {
        if (!file) {
            setError('Please select a file');
            return;
        }
        
        setLoading(true);
        setError(null);
        
        try {
            // Convert file to base64
            const base64 = await fileToBase64(file);
            
            // Make API request
            const response = await axios.post(
                `${API_URL}/detect`,
                {
                    audio_data: base64,
                    language: language
                },
                {
                    headers: {
                        'Authorization': `Bearer ${API_KEY}`,
                        'Content-Type': 'application/json'
                    }
                }
            );
            
            setResult(response.data);
            
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
        } finally {
            setLoading(false);
        }
    };
    
    const fileToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    };
    
    return (
        <div>
            <h2>AI Voice Detection</h2>
            
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                <option value="Tamil">Tamil</option>
                <option value="English">English</option>
                <option value="Hindi">Hindi</option>
                <option value="Malayalam">Malayalam</option>
                <option value="Telugu">Telugu</option>
            </select>
            
            <button onClick={detectVoice} disabled={loading || !file}>
                {loading ? 'Processing...' : 'Detect Voice'}
            </button>
            
            {error && <div style={{color: 'red'}}>{error}</div>}
            
            {result && (
                <div>
                    <h3>Result:</h3>
                    <p><strong>Classification:</strong> {result.classification}</p>
                    <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>
                    <p><strong>Explanation:</strong> {result.explanation}</p>
                    <p><strong>Processing Time:</strong> {result.processing_time_ms.toFixed(2)}ms</p>
                </div>
            )}
        </div>
    );
}

export default VoiceDetector;
```

---

## 💻 cURL Examples

### Example 1: Health Check

```bash
curl http://localhost:8000/health
```

### Example 2: Basic Detection

```bash
# Encode audio file
BASE64_AUDIO=$(base64 -w 0 sample.mp3)  # Linux
# BASE64_AUDIO=$(base64 -i sample.mp3)  # Mac

# Make request
curl -X POST "http://localhost:8000/detect" \
  -H "Authorization: Bearer dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d "{
    \"audio_data\": \"$BASE64_AUDIO\",
    \"language\": \"English\"
  }"
```

### Example 3: Pretty Print Response

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Authorization: Bearer dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d @request.json | jq .
```

---

## 📮 Postman Examples

### Collection Setup

1. **Create Collection:** "Voice Detection API"

2. **Add Environment Variables:**
   - `api_url`: `http://localhost:8000`
   - `api_key`: `dev-api-key-12345`

3. **Add Request: Health Check**
   - Method: GET
   - URL: `{{api_url}}/health`

4. **Add Request: Voice Detection**
   - Method: POST
   - URL: `{{api_url}}/detect`
   - Headers:
     - `Authorization`: `Bearer {{api_key}}`
     - `Content-Type`: `application/json`
   - Body (raw JSON):
     ```json
     {
       "audio_data": "BASE64_ENCODED_AUDIO_HERE",
       "language": "English"
     }
     ```

---

## 🔄 Integration Patterns

### Pattern 1: Webhook Integration

```python
# Your webhook handler
from flask import Flask, request
import requests
import base64

app = Flask(__name__)

@app.route('/webhook/audio', methods=['POST'])
def handle_audio_webhook():
    # Receive audio from external service
    audio_file = request.files['audio']
    
    # Encode to base64
    audio_base64 = base64.b64encode(audio_file.read()).decode()
    
    # Send to voice detection API
    response = requests.post(
        "http://localhost:8000/detect",
        headers={"Authorization": "Bearer dev-api-key-12345"},
        json={
            "audio_data": audio_base64,
            "language": request.form.get('language', 'English')
        }
    )
    
    # Return result
    return response.json()
```

### Pattern 2: Queue-Based Processing

```python
# Using Celery for async processing
from celery import Celery
import requests
import base64

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def process_audio(audio_path, language):
    with open(audio_path, 'rb') as f:
        audio_base64 = base64.b64encode(f.read()).decode()
    
    response = requests.post(
        "http://localhost:8000/detect",
        headers={"Authorization": "Bearer dev-api-key-12345"},
        json={"audio_data": audio_base64, "language": language}
    )
    
    return response.json()

# Usage
result = process_audio.delay('sample.mp3', 'English')
```

### Pattern 3: Streaming Audio

```python
# For real-time audio streams
import pyaudio
import wave
import base64
import requests
import io

def record_and_detect(duration=5, language="English"):
    # Record audio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    print("Recording...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Convert to WAV in memory
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    # Encode and send
    audio_base64 = base64.b64encode(wav_io.getvalue()).decode()
    
    response = requests.post(
        "http://localhost:8000/detect",
        headers={"Authorization": "Bearer dev-api-key-12345"},
        json={"audio_data": audio_base64, "language": language}
    )
    
    return response.json()

# Usage
result = record_and_detect(duration=3, language="English")
print(result)
```

---

## 📊 Response Handling

### Success Response (200)
```json
{
  "classification": "AI-generated",
  "confidence": 0.8542,
  "explanation": "Classified as AI-generated with high confidence (85.4%). Detected synthetic patterns in spectral features.",
  "language": "English",
  "processing_time_ms": 234.56
}
```

### Error Responses

**401 Unauthorized**
```json
{
  "detail": "Authorization header missing"
}
```

**403 Forbidden**
```json
{
  "detail": "Invalid API key"
}
```

**400 Bad Request**
```json
{
  "detail": "Invalid audio: file is silent, corrupted, or too short"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "language"],
      "msg": "unexpected value; permitted: 'Tamil', 'English', 'Hindi', 'Malayalam', 'Telugu'",
      "type": "value_error"
    }
  ]
}
```

---

## 🎯 Best Practices

1. **Always handle errors**
2. **Use timeouts** (30s recommended)
3. **Implement retry logic** for network issues
4. **Cache results** when appropriate
5. **Validate audio before sending**
6. **Use environment variables** for API keys
7. **Log requests** for debugging

---

**Need help?** Check the main README.md or open an issue!
