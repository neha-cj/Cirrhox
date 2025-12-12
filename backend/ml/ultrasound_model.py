# backend/ml/ultrasound_model.py
import tensorflow as tf
import os
import numpy as np

# 1. Setup the path to the .h5 file dynamically
# This ensures it finds the file on your teammate's computer too.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'densenet_model.h5')

class UltrasoundPredictor:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads the model from disk. Handles errors gracefully."""
        if os.path.exists(MODEL_PATH):
            try:
                print(f"Loading DenseNet model from {MODEL_PATH}...")
                self.model = tf.keras.models.load_model(MODEL_PATH)
                print("✅ DenseNet model loaded successfully.")
            except Exception as e:
                print(f"❌ ERROR: Failed to load DenseNet model: {e}")
        else:
            print(f"❌ ERROR: Model file not found at {MODEL_PATH}")
            print("Please download 'densenet_model.h5' and place it in backend/models/")

    def predict(self, preprocessed_image):
        """
        Runs inference and returns the diagnosis + probability.
        """
        if self.model is None:
            return {"error": "Model is not loaded. Check server logs."}

        try:
            # 1. Get raw prediction (Value between 0 and 1)
            prediction = self.model.predict(preprocessed_image)
            score = float(prediction[0][0])
            
            # 2. Interpret the Score
            # Since we trained with classes=['Normal', 'Fibrosis']:
            # 0.0 -> Normal
            # 1.0 -> Fibrosis
            
            diagnosis = "Fibrosis" if score > 0.5 else "Normal"
            
            # 3. Calculate Confidence (How sure is the AI?)
            # If score is 0.9 (Fibrosis), confidence is 0.9
            # If score is 0.1 (Normal), confidence is 0.9 (sure it's NOT fibrosis)
            confidence = score if score > 0.5 else 1 - score

            return {
                "diagnosis": diagnosis,
                "fibrosis_probability": score,  # Required for Soft Voting Ensemble
                "confidence": confidence
            }

        except Exception as e:
            return {"error": str(e)}

# Create a single instance to be imported by the API route
ultrasound_predictor = UltrasoundPredictor()
