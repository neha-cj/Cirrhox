from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ml.hybrid_predictor import HybridPredictor
from ml.clinical_predictor import ClinicalPredictor
from ml.ultrasound_predictor import UltrasoundPredictor

app = FastAPI(title="Cirrhox Backend")

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load predictors once (NOT on every request)
clinical_model = ClinicalPredictor()
ultra_model = UltrasoundPredictor()
hybrid_model = HybridPredictor()

# -------------------------------
#  Clinical Predictor Endpoint
# -------------------------------
@app.post("/predict/clinical")
async def clinical_predict(data: dict):
    try:
        prob = clinical_model.predict(data)
        return {
            "clinical_prob": prob,
            "label": "High Risk" if prob > 0.5 else "Low Risk"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
#  Ultrasound Predictor Endpoint
# -------------------------------
@app.post("/predict/ultrasound")
async def ultrasound_predict(file: UploadFile = File(...)):
    try:
        bytes_data = await file.read()
        prob = ultra_model.predict(bytes_data)
        return {
            "ultrasound_prob": prob,
            "label": "High Risk" if prob > 0.5 else "Low Risk"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
#  Hybrid Predictor Endpoint
# -------------------------------
@app.post("/predict/hybrid")
async def hybrid_predict(
    data: dict,
    file: UploadFile = File(...)
):
    try:
        img_bytes = await file.read()
        result = hybrid_model.predict(data, img_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def home():
    return {"message": "Cirrhox backend running!"}
