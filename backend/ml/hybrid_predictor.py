# ml/hybrid_predictor.py
from .clinical_predictor import ClinicalPredictor
from .ultrasound_predictor import UltrasoundPredictor

class HybridPredictor:
    def __init__(self):
        self.clinical_model = ClinicalPredictor()
        self.ultrasound_model = UltrasoundPredictor()

        # weights from abstract/SRS accuracy comparison
        self.w_clinical = 0.6
        self.w_ultrasound = 0.4

    def predict(self, clinical_data: dict, image_bytes: bytes):
        p1 = self.clinical_model.predict(clinical_data)
        p2 = self.ultrasound_model.predict(image_bytes)

        final = (self.w_clinical * p1) + (self.w_ultrasound * p2)

        # Clinical severity mapping
        if final < 0.3:
            severity = "Low"
        elif final < 0.6:
            severity = "Moderate"
        else:
            severity = "High"

        return {
            "clinical_prob": p1,
            "ultrasound_prob": p2,
            "final_prob": final,
            "diagnosis": "High Fibrosis Risk" if final > 0.5 else "Low Fibrosis Risk",
            "severity": severity,
            "confidence": abs(final - 0.5) * 2
        }
