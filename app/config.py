from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "AI Voice Detection API"
    API_VERSION: str = "1.0.0"
    API_KEY: str = "your-secure-api-key-here"
    
    # Model Settings
    MODEL_PATH: str = "models/classifier.pkl"
    SCALER_PATH: str = "models/scaler.pkl"
    
    # Audio Settings
    SAMPLE_RATE: int = 16000
    MAX_AUDIO_LENGTH: int = 30  # seconds
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Feature Extraction
    N_MFCC: int = 40
    N_MELS: int = 128
    HOP_LENGTH: int = 512
    
    # Performance
    CACHE_TTL: int = 3600
    MAX_WORKERS: int = 4
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
