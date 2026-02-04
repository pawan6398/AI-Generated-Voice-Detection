import base64
import io
import librosa
import soundfile as sf
import numpy as np
from typing import Tuple
from app.config import get_settings

settings = get_settings()

class AudioProcessor:
    def __init__(self):
        self.sample_rate = settings.SAMPLE_RATE
        self.max_length = settings.MAX_AUDIO_LENGTH
        self.max_file_size = settings.MAX_FILE_SIZE
    
    def decode_base64_audio(self, base64_string: str) -> Tuple[np.ndarray, int]:
        """Decode base64 string to audio array"""
        try:
            # Decode base64
            audio_bytes = base64.b64decode(base64_string)
            
            # Check file size
            if len(audio_bytes) > self.max_file_size:
                raise ValueError(f"Audio file too large. Max size: {self.max_file_size} bytes")
            
            # Load audio from bytes
            audio_io = io.BytesIO(audio_bytes)
            audio, sr = sf.read(audio_io)
            
            # Convert stereo to mono if needed
            if len(audio.shape) > 1:
                audio = librosa.to_mono(audio.T)
            
            # Resample to target sample rate
            if sr != self.sample_rate:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=self.sample_rate)
            
            # Trim or pad to max length
            max_samples = self.sample_rate * self.max_length
            if len(audio) > max_samples:
                audio = audio[:max_samples]
            
            return audio, self.sample_rate
            
        except Exception as e:
            raise ValueError(f"Error processing audio: {str(e)}")
    
    def validate_audio(self, audio: np.ndarray) -> bool:
        """Validate audio array"""
        if audio is None or len(audio) == 0:
            return False
        
        # Check for silence (all zeros or very low amplitude)
        if np.max(np.abs(audio)) < 0.001:
            return False
        
        # Check for NaN or Inf
        if np.any(np.isnan(audio)) or np.any(np.isinf(audio)):
            return False
        
        return True
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1] range"""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        return audio
