from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from utils.auth_utils import get_current_user
from models_db.user_model import User
from models_db.history_model import PredictionHistory

from ml.hybrid_predictor import HybridPredictor
from ml.clinical_predictor import ClinicalPredictor
from ml.ultrasound_predictor import UltrasoundPredictor


router = APIRouter(prefix="/predict", tags=["Predict"])

# Load models once
clinical_model = ClinicalPredictor()
ultra_model = UltrasoundPredictor()
hybrid_model = HybridPredictor()


# -------------------------------
# Clinical Predictor
# -------------------------------
@router.post("/clinical")
async def clinical_predict(data: dict):
    try:
        result = clinical_model.predict(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# Ultrasound Predictor
# -------------------------------
@router.post("/ultrasound")
async def ultrasound_predict(file: UploadFile = File(...)):
    try:
        bytes_data = await file.read()
        result = ultra_model.predict(bytes_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# Hybrid Predictor (SAVES HISTORY)
# -------------------------------

@router.post("/hybrid")
async def hybrid_predict(
    bilirubin: float = Form(...),
    albumin:   float = Form(...),
    ast:       float = Form(...),
    alt:       float = Form(...),
    alp:       float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    clinical_data = {
        "bilirubin": bilirubin,
        "albumin":   albumin,
        "ast":       ast,
        "alt":       alt,
        "alp":       alp
    }

    try:
        img_bytes = await file.read()

        result = hybrid_model.predict(clinical_data, img_bytes)

        if not result:
            raise HTTPException(status_code=400, detail="Prediction failed")

        probability = result["confidence"]
        label       = result["prediction"]
        severity    = result["severity"]

        history_entry = PredictionHistory(
            user_id=current_user.id,
            prediction=label,
            probability=probability,
            severity=severity,
            bilirubin=bilirubin,
            albumin=albumin,
            ast=ast,
            alt=alt,
            alp=alp
        )

        db.add(history_entry)
        db.commit()
        db.refresh(history_entry)

        return result

    except Exception as e:
        print("🔥 HYBRID ERROR:", e)
        raise HTTPException(status_code=400, detail=str(e))