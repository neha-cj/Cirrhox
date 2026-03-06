from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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
            "id":         record.id,
            "prediction": record.prediction,
            "probability": record.probability,
            "severity":   record.severity,
            "bilirubin":  record.bilirubin,
            "albumin":    record.albumin,
            "ast":        record.ast,
            "alt":        record.alt,
            "alp":        record.alp,
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
        result.append({
            "id":           record.id,
            "prediction":   record.prediction,
            "probability":  record.probability,
            "severity":     record.severity,
            "bilirubin":    record.bilirubin,
            "albumin":      record.albumin,
            "ast":          record.ast,
            "alt":          record.alt,
            "alp":          record.alp,
            "created_at":   record.created_at,
            "patient_name": record.user.name
        })

    return result