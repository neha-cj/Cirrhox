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


# Load models once (when server starts)
clinical_model = ClinicalPredictor()
ultra_model = UltrasoundPredictor()
hybrid_model = HybridPredictor()


# ----------------------------------
# Clinical Predictor
# ----------------------------------

@router.post("/clinical")
async def clinical_predict(data: dict):
    try:
        result = clinical_model.predict(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------------
# Ultrasound Predictor
# ----------------------------------

@router.post("/ultrasound")
async def ultrasound_predict(file: UploadFile = File(...)):
    try:
        bytes_data = await file.read()
        result = ultra_model.predict(bytes_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------------
# Hybrid Predictor (Saves History)
# ----------------------------------

@router.post("/hybrid")
async def hybrid_predict(
    bilirubin: float = Form(...),
    albumin:   float = Form(...),
    ast:       float = Form(...),
    alt:       float = Form(...),
    alp:       float = Form(...),

    patient_id: int = Form(None),  # used when doctor predicts

    file: UploadFile = File(...),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    clinical_data = {
        "bilirubin": bilirubin,
        "albumin": albumin,
        "ast": ast,
        "alt": alt,
        "alp": alp
    }

    try:
        # Read ultrasound image
        img_bytes = await file.read()

        # Run hybrid model
        result = hybrid_model.predict(clinical_data, img_bytes)

        if not result:
            raise HTTPException(status_code=400, detail="Prediction failed")

        probability = result["confidence"]
        label       = result["prediction"]
        severity    = result["severity"]

        # ----------------------------------
        # Determine patient for the record
        # ----------------------------------

        if current_user.role == "doctor":

            if not patient_id:
                raise HTTPException(
                    status_code=400,
                    detail="Patient ID required for doctor prediction"
                )

            patient = db.query(User).filter(User.id == patient_id).first()

            if not patient:
                raise HTTPException(
                    status_code=404,
                    detail="Patient not found"
                )

            user_id = patient.id
            doctor_id = current_user.id

        else:
            # patient self prediction
            user_id = current_user.id
            doctor_id = None


        # ----------------------------------
        # Save Prediction History
        # ----------------------------------

        history_entry = PredictionHistory(
            user_id=user_id,
            doctor_id=doctor_id,
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