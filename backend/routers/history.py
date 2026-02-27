from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models_db.history_model import PredictionHistory
from models_db.user_model import User
from utils.auth_utils import get_current_user, doctor_only

router = APIRouter(tags=["History"])

@router.get("/my-history")
def my_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(PredictionHistory)\
        .filter(PredictionHistory.user_id == current_user.id)\
        .order_by(PredictionHistory.created_at.desc())\
        .all()

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "prediction": record.prediction,
            "probability": record.probability,
            "severity": record.severity,       # ✅ ADD
            "bilirubin": record.bilirubin,
            "albumin": record.albumin,
            "protime": record.protime,
            "ast": record.ast,
            "created_at": record.created_at
        })

    return result

@router.get("/all-history")
def all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(doctor_only)
):
    records = db.query(PredictionHistory)\
        .join(User, PredictionHistory.user_id == User.id)\
        .order_by(PredictionHistory.created_at.desc())\
        .all()

    result = []

    for record in records:
        user = db.query(User).filter(User.id == record.user_id).first()

        result.append({
            "id": record.id,
            "prediction": record.prediction,
            "probability": record.probability,
            "severity": record.severity,          # ✅ ADD THIS
            "bilirubin": record.bilirubin,        # ✅ ADD
            "albumin": record.albumin,            # ✅ ADD
            "protime": record.protime,            # ✅ ADD
            "ast": record.ast,                    # ✅ ADD
            "created_at": record.created_at,
            "patient_name": record.user.name
        })

    return result
