from pydantic import BaseModel, Field, validator
from typing import Literal
from enum import Enum

class ClassificationLabel(str, Enum):
    AI_GENERATED = "AI-generated"
    HUMAN = "Human"

class AudioRequest(BaseModel):
    audio_data: str = Field(
        ..., 
        description="Base64-encoded MP3 audio file"
    )
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"] = Field(
        ...,
        description="Language of the audio sample"
    )
    
    @validator('audio_data')
    def validate_base64(cls, v):
        import base64
        try:
            # Try to decode to verify it's valid base64
            base64.b64decode(v, validate=True)
            return v
        except Exception:
            raise ValueError("Invalid Base64 encoding")

class AudioResponse(BaseModel):
    classification: ClassificationLabel = Field(
        ...,
        description="Whether the voice is AI-generated or Human"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )
    explanation: str = Field(
        ...,
        description="Brief explanation of the classification"
    )
    language: str = Field(
        ...,
        description="Detected/provided language"
    )
    processing_time_ms: float = Field(
        ...,
        description="Time taken to process the request"
    )

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
