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
    return db.query(PredictionHistory)\
        .filter(PredictionHistory.user_id == current_user.id)\
        .order_by(PredictionHistory.created_at.desc())\
        .all()

@router.get("/all-history")
def all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(doctor_only)
):
    records = db.query(PredictionHistory)\
        .join(User, PredictionHistory.user_id == User.id)\
        .all()

    result = []
    for record in records:
        user = db.query(User).filter(User.id == record.user_id).first()

        result.append({
            "id": record.id,
            "prediction": record.prediction,
            "probability": record.probability,
            "created_at": record.created_at,
            "patient_name": user.name
        })

    return result

# @router.get("/all-history")
# def all_history(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(doctor_only)
# ):
#     return db.query(PredictionHistory).all()