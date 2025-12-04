import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pickle

# Load dataset from .xls file
df = pd.read_excel("../../datasets/clinical/pbc.xls")


# Rename columns if needed (sometimes PBC XLS uses uppercase or different names)
df.columns = df.columns.str.lower()

# Check available columns
print("Columns:", df.columns.tolist())

# Choose clinical features (make sure names match your XLS file)
features = ["bili", "albumin", "protime", "ast"]  # adjust if needed

X = df[features]

# Target variable: stage (fibrosis stage)
# Some XLS versions use "stage" or "stage.1" or numeric
y = (df["stage"] >= 3).astype(int)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = XGBClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("../models/xgboost_model.pkl", "wb"))

print("Model saved successfully!")
