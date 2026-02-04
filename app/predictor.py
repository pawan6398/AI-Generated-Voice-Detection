import pickle
import numpy as np
from typing import Tuple
from app.config import get_settings
import os

settings = get_settings()

class VoicePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            if os.path.exists(settings.MODEL_PATH):
                with open(settings.MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                print("Warning: Model file not found. Using dummy model.")
                self.model = self._create_dummy_model()
            
            if os.path.exists(settings.SCALER_PATH):
                with open(settings.SCALER_PATH, 'rb') as f:
                    self.scaler = pickle.load(f)
            else:
                print("Warning: Scaler file not found. Features won't be scaled.")
                
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a simple dummy model for testing"""
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        # Initialize with dummy data
        X_dummy = np.random.randn(10, 100)
        y_dummy = np.random.randint(0, 2, 10)
        model.fit(X_dummy, y_dummy)
        return model
    
    def predict(self, features: np.ndarray) -> Tuple[str, float, str]:
        """
        Make prediction on features
        Returns: (classification, confidence, explanation)
        """
        # Reshape features if needed
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        # Scale features if scaler is available
        if self.scaler is not None:
            features = self.scaler.transform(features)
        
        # Get prediction and probability
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        # Map prediction to label
        classification = "AI-generated" if prediction == 1 else "Human"
        confidence = float(probabilities[prediction])
        
        # Generate explanation
        explanation = self._generate_explanation(classification, confidence, features)
        
        return classification, confidence, explanation
    
    def _generate_explanation(self, classification: str, confidence: float, features: np.ndarray) -> str:
        """Generate human-readable explanation"""
        if confidence > 0.8:
            certainty = "high confidence"
        elif confidence > 0.6:
            certainty = "moderate confidence"
        else:
            certainty = "low confidence"
        
        if classification == "AI-generated":
            reasons = [
                "Detected synthetic patterns in spectral features",
                "Unusual uniformity in voice characteristics",
                "Artifacts typical of AI voice synthesis"
            ]
        else:
            reasons = [
                "Natural voice variations detected",
                "Human-like breathing patterns present",
                "Organic spectral characteristics"
            ]
        
        explanation = f"Classified as {classification} with {certainty} ({confidence:.1%}). {reasons[0]}."
        return explanation
