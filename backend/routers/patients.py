from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models_db.user_model import User
from utils.auth_utils import doctor_only

router = APIRouter(tags=["Patients"])

@router.get("/patients")
def get_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(doctor_only)
):

    patients = db.query(User).filter(User.role == "patient").all()

    return patients