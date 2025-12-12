import numpy as np
import xgboost as xgb

class ClinicalPredictor:
    def __init__(self, model_path="models/xgboost_model.json"):
        self.model = xgb.Booster()
        self.model.load_model(model_path)

        # These are the REAL training feature names
        self.features = ["bili", "albumin", "protime", "sgot"]

    def preprocess(self, data: dict):
        try:
            x = [float(data[f]) for f in self.features]
            return np.array(x).reshape(1, -1)
        except KeyError as e:
            raise ValueError(f"Missing clinical feature: {e}")

    def predict(self, data: dict):
        X = self.preprocess(data)

        # 🟢 FIX: Pass feature names into DMatrix explicitly
        dmatrix = xgb.DMatrix(X, feature_names=self.features)

        prob = float(self.model.predict(dmatrix)[0])
        return prob
