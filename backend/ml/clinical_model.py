import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pickle

# Load dataset
df = pd.read_csv("../../datasets/clinical/pbc.csv")

# Choose clinical features
features = ["bilirubin", "albumin", "protime", "ast"]
X = df[features]
y = (df["stage"] >= 3).astype(int)  # fibrosis severe vs non-severe

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = XGBClassifier()
model.fit(X_train, y_train)

# Save
pickle.dump(model, open("../models/xgboost_model.pkl", "wb"))

print("Model saved!")
