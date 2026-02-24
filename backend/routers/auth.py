from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models_db.user_model import User
from schemas.user_schema import UserCreate
from utils.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()


# =========================
# Register
# =========================

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# =========================
# Login (OAuth2 Password Flow)
# =========================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# Get Current User
# =========================

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }


# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session
# # from database import get_db
# # from models_db.user_model import User
# # from schemas.user_schema import UserCreate
# # from schemas.user_schema import UserLogin
# # from utils.auth_utils import create_access_token
# # from utils.auth_utils import hash_password, verify_password
# # from utils.auth_utils import get_current_user
# # from models_db.history_model import PredictionHistory

# # router = APIRouter()

# # @router.post("/register")
# # def register(user: UserCreate, db: Session = Depends(get_db)):
# #     existing = db.query(User).filter(User.email == user.email).first()
# #     if existing:
# #         raise HTTPException(status_code=400, detail="Email already registered")

# #     hashed = hash_password(user.password)

# #     new_user = User(
# #         name=user.name,
# #         email=user.email,
# #         password=hashed,
# #         role=user.role
# #     )

# #     db.add(new_user)
# #     db.commit()
# #     db.refresh(new_user)

# #     return {"message": "User registered successfully"}

# # @router.post("/login")
# # def login(user: UserLogin, db: Session = Depends(get_db)):

# #     db_user = db.query(User).filter(User.email == user.email).first()

# #     if not db_user:
# #         raise HTTPException(status_code=400, detail="Invalid email")

# #     if not verify_password(user.password, db_user.password):
# #         raise HTTPException(status_code=400, detail="Invalid password")

# #     token = create_access_token({
# #         "sub": db_user.email,
# #         "role": db_user.role
# #     })

# #     return {
# #         "access_token": token,
# #         "role": db_user.role
# #     }

# # @router.get("/me")
# # def get_me(current_user: User = Depends(get_current_user)):
# #     return {
# #         "email": current_user.email,
# #         "role": current_user.role
# #     }