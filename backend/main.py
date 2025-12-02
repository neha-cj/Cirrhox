from fastapi import FastAPI, UploadFile
from ml.hybrid_predictor import predict_hybrid
import pandas as pd
from PIL import Image
import numpy as np

app = FastAPI()

@app.post("/predict")
async def predict(clinicalData: dict, file: UploadFile):
    # clinical features
    features = [clinicalData["bilirubin"], clinicalData["albumin"],
                clinicalData["protime"], clinicalData["ast"]]

    # image
    img = Image.open(file.file).resize((224,224))
    img = np.array(img)/255.0
    img = img.reshape(1,224,224,3)

    result = predict_hybrid(features, img)

    return result
