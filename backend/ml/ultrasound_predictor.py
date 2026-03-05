# ml/ultrasound_predictor.py

import tensorflow as tf
import numpy as np
from .preprocess_image import preprocess_ultrasound


class UltrasoundPredictor:

    def __init__(self, model_path="models/liver_ultrasound_densenet.h5"):

        try:
            # Load model (Keras 3 requires compile=False)
            self.model = tf.keras.models.load_model(
                model_path,
                compile=False
            )

            print("Ultrasound model output shape:", self.model.output_shape)

        except Exception as e:
            raise RuntimeError(f"Failed to load ultrasound model: {e}")

        # Class order MUST match training
        self.class_names = [
            "Cirrhosis",
            "Fibrosis",
            "No_Fibrosis"
        ]

        self.severity_map = {
            "Cirrhosis": "High",
            "Fibrosis": "Moderate",
            "No_Fibrosis": "Low"
        }

        # GPU check
        gpus = tf.config.list_physical_devices("GPU")
        self.device = "GPU" if gpus else "CPU"

    def predict(self, file_bytes: bytes):

        try:
            # Preprocess ultrasound image
            img_tensor = preprocess_ultrasound(file_bytes)

            # Ensure float32 for TensorFlow
            img_tensor = tf.cast(img_tensor, tf.float32)

            # Model prediction (softmax output)
            preds = self.model.predict(img_tensor, verbose=0)[0]


            probs = preds.astype(float)

            # Get predicted class
            pred_index = int(np.argmax(probs))
            prediction = self.class_names[pred_index]

            result = {
                "prediction": prediction,
                "severity": self.severity_map[prediction],
                "confidence": float(probs[pred_index]),
                "probabilities": {
                    self.class_names[i]: float(probs[i])
                    for i in range(len(self.class_names))
                }
            }

            return result

        except Exception as e:
            raise RuntimeError(f"Ultrasound prediction failed: {e}")