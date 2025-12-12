# ml/clinical_predictor.py
import pickle
import numpy as np

class ClinicalPredictor:
    def __init__(self, model_path="../models/xgboost_model.pkl"):
        self.model = pickle.load(open(model_path, "rb"))
        self.features = ["bili", "albumin", "protime", "ast"]

    def preprocess(self, data: dict):
        """Convert input JSON into ordered feature array"""
        try:
            x = [float(data[f]) for f in self.features]
            return np.array(x)
        except KeyError as e:
            raise ValueError(f"Missing clinical feature: {e}")

    def predict(self, data: dict):
        x = self.preprocess(data)
        prob = float(self.model.predict_proba([x])[0][1])
        return prob
