# ml/ultrasound_predictor.py
import tensorflow as tf
import numpy as np
from .preprocess_image import preprocess_ultrasound

class UltrasoundPredictor:
    def __init__(self, model_path="models/densenet_model.h5"):
        try:
            # 🔥 Keras 3 models MUST be loaded with compile=False
            self.model = tf.keras.models.load_model(
                model_path,
                compile=False
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load ultrasound model: {e}")

        # GPU fallback check
        gpus = tf.config.list_physical_devices("GPU")
        self.device = "GPU" if gpus else "CPU"

    def predict(self, file_bytes: bytes):
        try:
            # Preprocess image → returns (1, 224, 224, 3)
            img_tensor = preprocess_ultrasound(file_bytes)

            # Ensure it's float32 (Keras 3 strict mode)
            img_tensor = tf.cast(img_tensor, tf.float32)

            # Predict
            pred = self.model.predict(img_tensor)[0]

            # Some models output shape (1,) others (1,1)
            prob = float(pred[0]) if isinstance(pred, (list, np.ndarray)) else float(pred)

            return prob

        except Exception as e:
            raise RuntimeError(f"Ultrasound prediction failed: {e}")
