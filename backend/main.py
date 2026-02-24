from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from models_db import user_model, history_model

from routers import auth, history, predict


app = FastAPI(title="Cirrhox Backend")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(history.router)
app.include_router(predict.router)

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {"message": "Cirrhox backend running!"}
