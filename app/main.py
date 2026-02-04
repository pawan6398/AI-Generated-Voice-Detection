from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from typing import Optional

from app.models import AudioRequest, AudioResponse, HealthResponse, ClassificationLabel
from app.audio_processor import AudioProcessor
from app.feature_extractor import FeatureExtractor
from app.predictor import VoicePredictor
from app.config import get_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI-Generated Voice Detection API for Multi-Language Support"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
audio_processor = AudioProcessor()
feature_extractor = FeatureExtractor()
predictor = VoicePredictor()

# Authentication
async def verify_api_key(authorization: Optional[str] = Header(None)):
    """Verify API key from Authorization header"""
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Support both "Bearer TOKEN" and plain "TOKEN" formats
    token = authorization.replace("Bearer ", "").strip()
    
    if token != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return token

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy",
        model_loaded=predictor.model is not None,
        version=settings.API_VERSION
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=predictor.model is not None,
        version=settings.API_VERSION
    )

@app.post("/detect", response_model=AudioResponse)
async def detect_voice(
    request: AudioRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Detect if a voice sample is AI-generated or human
    
    - **audio_data**: Base64-encoded MP3 audio file
    - **language**: Language of the audio (Tamil, English, Hindi, Malayalam, Telugu)
    """
    start_time = time.time()
    
    try:
        # Step 1: Decode and process audio
        logger.info(f"Processing audio for language: {request.language}")
        audio, sr = audio_processor.decode_base64_audio(request.audio_data)
        
        # Step 2: Validate audio
        if not audio_processor.validate_audio(audio):
            raise HTTPException(
                status_code=400, 
                detail="Invalid audio: file is silent, corrupted, or too short"
            )
        
        # Step 3: Normalize audio
        audio = audio_processor.normalize_audio(audio)
        
        # Step 4: Extract features
        logger.info("Extracting audio features")
        features = feature_extractor.extract_features(audio)
        
        # Step 5: Make prediction
        logger.info("Running inference")
        classification, confidence, explanation = predictor.predict(features)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Build response
        response = AudioResponse(
            classification=ClassificationLabel(classification),
            confidence=round(confidence, 4),
            explanation=explanation,
            language=request.language,
            processing_time_ms=round(processing_time, 2)
        )
        
        logger.info(f"Classification: {classification}, Confidence: {confidence:.4f}, Time: {processing_time:.2f}ms")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Internal error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
