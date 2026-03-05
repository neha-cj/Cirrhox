# ml/hybrid_predictor.py

import numpy as np
from .clinical_predictor import ClinicalPredictor
from .ultrasound_predictor import UltrasoundPredictor


class HybridPredictor:

    def __init__(self):

        self.clinical_model = ClinicalPredictor()
        self.ultrasound_model = UltrasoundPredictor()

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


    def predict(self, clinical_data: dict, image_bytes: bytes):

        print("HYBRID PREDICT STARTED")

        # -----------------------------
        # Run individual models
        # -----------------------------

        clinical_result = self.clinical_model.predict(clinical_data)
        ultrasound_result = self.ultrasound_model.predict(image_bytes)

        print("Clinical result:", clinical_result)
        print("Ultrasound result:", ultrasound_result)

        # -----------------------------
        # Extract probability vectors
        # -----------------------------

        clinical_probs = np.array([
            clinical_result["probabilities"].get(c, 0.0)
            for c in self.class_names
        ])

        ultrasound_probs = np.array([
            ultrasound_result["probabilities"].get(c, 0.0)
            for c in self.class_names
        ])

        print("Clinical:", clinical_probs)
        print("Ultrasound:", ultrasound_probs)

        # -----------------------------
        # Confidence-based weights
        # -----------------------------

        clinical_conf = clinical_result["confidence"]
        ultrasound_conf = ultrasound_result["confidence"]

        total_conf = clinical_conf + ultrasound_conf

        w_clinical = clinical_conf / total_conf
        w_ultrasound = ultrasound_conf / total_conf

        print("Weights → Clinical:", w_clinical, " Ultrasound:", w_ultrasound)

        # -----------------------------
        # Weighted soft voting
        # -----------------------------

        final_probs = (
            w_clinical * clinical_probs +
            w_ultrasound * ultrasound_probs
        )

        # Normalize probabilities
        final_probs = final_probs / np.sum(final_probs)

        pred_index = int(np.argmax(final_probs))
        prediction = self.class_names[pred_index]

        result = {
            "prediction": prediction,
            "severity": self.severity_map[prediction],
            "confidence": float(final_probs[pred_index]),

            "probabilities": {
                self.class_names[i]: float(final_probs[i])
                for i in range(len(self.class_names))
            },

            "clinical_probabilities": clinical_result["probabilities"],
            "ultrasound_probabilities": ultrasound_result["probabilities"]
        }

        return result