import os
import pickle
import numpy as np
import pandas as pd


class ClinicalPredictor:

    def __init__(self, model_path="models/clinical_model.pkl"):

        # Load trained model
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        # Training feature order
        self.features = [
            "bili",
            "albumin",
            "protime",
            "sgot"
        ]

        print(
            "Test proba shape:",
            self.model.predict_proba(
                pd.DataFrame([[1,1,1,1]], columns=self.features)
            ).shape
        )

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

    def preprocess(self, data: dict):

        try:
            values = [float(data[f]) for f in self.features]
        except KeyError as e:
            raise ValueError(f"Missing required clinical feature: {e}")

        X = pd.DataFrame([values], columns=self.features)

        return X

    def predict(self, data: dict):

        X = self.preprocess(data)

        # probs = self.model.predict_proba(X)[0]
        probs = np.array(self.model.predict_proba(X)[0])
        

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