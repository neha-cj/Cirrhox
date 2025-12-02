import pickle
import numpy as np
import tensorflow as tf

# Load both models
clinical = pickle.load(open("../models/xgboost_model.pkl", "rb"))
ultra = tf.keras.models.load_model("../models/densenet_model.h5")

def predict_hybrid(clinical_features, image_array):
    p1 = clinical.predict_proba([clinical_features])[0][1]
    p2 = float(ultra.predict(image_array)[0][0])

    # Weighted soft voting
    final = 0.6*p1 + 0.4*p2

    return {
        "clinical": float(p1),
        "ultrasound": float(p2),
        "final": float(final),
        "label": "High Risk" if final > 0.5 else "Low Risk"
    }
