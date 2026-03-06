import pickle
import numpy as np
import pandas as pd


class ClinicalPredictor:

    def __init__(
        self,
        model_path="models/clinical_ensemble.pkl",
        imputer_path="models/clinical_imputer.pkl",
        scaler_path="models/clinical_scaler.pkl"
    ):
        # Load RF + XGBoost voting ensemble
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        # Load imputer (handles any missing input values)
        with open(imputer_path, "rb") as f:
            self.imputer = pickle.load(f)

        # Load scaler (must match training-time scaling)
        with open(scaler_path, "rb") as f:
            self.scaler = pickle.load(f)

        # Updated feature set — matches combined dataset training
        self.features = [
            "bilirubin",
            "albumin",
            "ast",
            "alt",
            "alp"
        ]

        # Sanity check on load
        print(
            "Clinical ensemble loaded. Test proba shape:",
            self.model.predict_proba(
                self.scaler.transform(
                    self.imputer.transform(
                        pd.DataFrame([[1, 1, 1, 1, 1]], columns=self.features)
                    )
                )
            ).shape
        )

        self.class_names = [
            "Cirrhosis",
            "Fibrosis",
            "No_Fibrosis"
        ]

        self.severity_map = {
            "Cirrhosis":   "High",
            "Fibrosis":    "Moderate",
            "No_Fibrosis": "Low"
        }

    def preprocess(self, data: dict):

        try:
            values = [float(data[f]) for f in self.features]
        except KeyError as e:
            raise ValueError(f"Missing required clinical feature: {e}")

        X = pd.DataFrame([values], columns=self.features)

        # Step 1 — impute (handles NaN if any field is missing)
        X = pd.DataFrame(
            self.imputer.transform(X),
            columns=self.features
        )

        # Step 2 — scale (must match training-time scaler)
        X = pd.DataFrame(
            self.scaler.transform(X),
            columns=self.features
        )

        return X

    def predict(self, data: dict):

        X = self.preprocess(data)

        probs = np.array(self.model.predict_proba(X)[0])

        pred_index = int(np.argmax(probs))
        prediction = self.class_names[pred_index]

        result = {
            "prediction":   prediction,
            "severity":     self.severity_map[prediction],
            "confidence":   float(probs[pred_index]),
            "probabilities": {
                self.class_names[i]: float(probs[i])
                for i in range(len(self.class_names))
            }
        }

        return result