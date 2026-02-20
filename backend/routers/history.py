from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models_db.history_model import PredictionHistory
from models_db.user_model import User
from utils.auth_utils import get_current_user, doctor_only

router = APIRouter()

@router.get("/my-history")
def my_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(PredictionHistory).filter(
        PredictionHistory.user_id == current_user.id
    ).all()


@router.get("/all-history")
def all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(doctor_only)
):
    return db.query(PredictionHistory).all()