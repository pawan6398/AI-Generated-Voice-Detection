import librosa
import numpy as np
from typing import Dict
from app.config import get_settings

settings = get_settings()

class FeatureExtractor:
    def __init__(self):
        self.sample_rate = settings.SAMPLE_RATE
        self.n_mfcc = settings.N_MFCC
        self.n_mels = settings.N_MELS
        self.hop_length = settings.HOP_LENGTH
    
    def extract_features(self, audio: np.ndarray) -> np.ndarray:
        """Extract comprehensive audio features"""
        features = {}
        
        # 1. MFCC Features (Mel-frequency cepstral coefficients)
        mfcc = librosa.feature.mfcc(
            y=audio, 
            sr=self.sample_rate, 
            n_mfcc=self.n_mfcc,
            hop_length=self.hop_length
        )
        features['mfcc_mean'] = np.mean(mfcc, axis=1)
        features['mfcc_std'] = np.std(mfcc, axis=1)
        features['mfcc_max'] = np.max(mfcc, axis=1)
        features['mfcc_min'] = np.min(mfcc, axis=1)
        
        # 2. Spectral Features
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio, 
            sr=self.sample_rate,
            hop_length=self.hop_length
        )
        features['spectral_centroid_mean'] = np.mean(spectral_centroid)
        features['spectral_centroid_std'] = np.std(spectral_centroid)
        
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=audio, 
            sr=self.sample_rate,
            hop_length=self.hop_length
        )
        features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
        features['spectral_rolloff_std'] = np.std(spectral_rolloff)
        
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=audio, 
            sr=self.sample_rate,
            hop_length=self.hop_length
        )
        features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
        features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
        
        # 3. Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(audio, hop_length=self.hop_length)
        features['zcr_mean'] = np.mean(zcr)
        features['zcr_std'] = np.std(zcr)
        
        # 4. Chroma Features
        chroma = librosa.feature.chroma_stft(
            y=audio, 
            sr=self.sample_rate,
            hop_length=self.hop_length
        )
        features['chroma_mean'] = np.mean(chroma, axis=1)
        features['chroma_std'] = np.std(chroma, axis=1)
        
        # 5. Mel Spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=audio, 
            sr=self.sample_rate,
            n_mels=self.n_mels,
            hop_length=self.hop_length
        )
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        features['mel_mean'] = np.mean(mel_spec_db)
        features['mel_std'] = np.std(mel_spec_db)
        
        # 6. Temporal Features
        features['duration'] = len(audio) / self.sample_rate
        features['rms_mean'] = np.mean(librosa.feature.rms(y=audio, hop_length=self.hop_length))
        
        # Flatten all features into a single vector
        feature_vector = []
        for key in sorted(features.keys()):
            value = features[key]
            if isinstance(value, np.ndarray):
                feature_vector.extend(value.tolist())
            else:
                feature_vector.append(value)
        
        #return np.array(feature_vector)[:100]
        # Feature vector ko exactly 100 dimensions ka banayein
        final_vector = np.array(feature_vector)
        if len(final_vector) > 100:
            final_vector = final_vector[:100]
        elif len(final_vector) < 100:
            final_vector = np.pad(final_vector, (0, 100 - len(final_vector)), 'constant')
            
        return final_vector
    
    def get_feature_names(self) -> list:
        """Return list of feature names for reference"""
        return [
            'mfcc_mean', 'mfcc_std', 'mfcc_max', 'mfcc_min',
            'spectral_centroid_mean', 'spectral_centroid_std',
            'spectral_rolloff_mean', 'spectral_rolloff_std',
            'spectral_bandwidth_mean', 'spectral_bandwidth_std',
            'zcr_mean', 'zcr_std',
            'chroma_mean', 'chroma_std',
            'mel_mean', 'mel_std',
            'duration', 'rms_mean'
        ]
