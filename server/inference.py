import os
import joblib
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class ModelRunner:
    """
    Loads and manages ML model inference with confidence scoring.
    """
    
    def __init__(self):
        """Initialize and load the ML model from MODEL_PATH environment variable."""
        model_path = os.getenv('MODEL_PATH', '/app/models/model.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def predict(self, feature_dict: dict) -> Tuple[str, float]:
        """
        Generate prediction and confidence score.
        
        Args:
            feature_dict: Dictionary of feature_name -> feature_value
            
        Returns:
            Tuple of (prediction_string, confidence_score)
            
        Raises:
            Exception on inference failure
        """
        try:
            features_list = list(feature_dict.values())
            prediction = self.model.predict([features_list])[0]
            
            try:
                probas = self.model.predict_proba([features_list])[0]
                confidence = float(max(probas))
            except (AttributeError, IndexError):
                confidence = 1.0
            
            return str(prediction), confidence
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise