# ml/ultrasound_predictor.py
import tensorflow as tf
import numpy as np
from .preprocess_image import preprocess_ultrasound

class UltrasoundPredictor:
    def __init__(self, model_path="models/densenet_model.h5"):
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load ultrasound model: {e}")

        # GPU fallback check
        self.device = "GPU" if tf.config.list_physical_devices('GPU') else "CPU"

    def predict(self, file_bytes: bytes):
        try:
            img = preprocess_ultrasound(file_bytes)   # returns (1,224,224,3)
            prob = float(self.model.predict(img)[0][0])
            return prob
        except Exception as e:
            raise RuntimeError(f"Ultrasound prediction failed: {e}")
