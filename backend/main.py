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





# from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from ml.hybrid_predictor import HybridPredictor
# from ml.clinical_predictor import ClinicalPredictor
# from ml.ultrasound_predictor import UltrasoundPredictor
# from database import engine, Base
# from models_db import user_model, history_model
# from routers import auth, history, predict


# app = FastAPI(title="Cirrhox Backend")


# Base.metadata.create_all(bind=engine)

# app.include_router(auth.router)
# app.include_router(history.router)
# app.include_router(predict.router)

# # Allow frontend to call this API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# # Load predictors once (NOT on every request)
# clinical_model = ClinicalPredictor()
# ultra_model = UltrasoundPredictor()
# hybrid_model = HybridPredictor()

# # -------------------------------
# #  Clinical Predictor Endpoint
# # -------------------------------
# @app.post("/predict/clinical")
# async def clinical_predict(data: dict):
#     try:
#         prob = clinical_model.predict(data)
#         return {
#             "clinical_prob": prob,
#             "label": "High Risk" if prob > 0.5 else "Low Risk"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# # -------------------------------
# #  Ultrasound Predictor Endpoint
# # -------------------------------
# @app.post("/predict/ultrasound")
# async def ultrasound_predict(file: UploadFile = File(...)):
#     try:
#         bytes_data = await file.read()
#         prob = ultra_model.predict(bytes_data)
#         return {
#             "ultrasound_prob": prob,
#             "label": "High Risk" if prob > 0.5 else "Low Risk"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# # -------------------------------
# #  Hybrid Predictor Endpoint
# # -------------------------------
# @app.post("/predict/hybrid")
# async def hybrid_predict(
#     bilirubin: float = Form(...),
#     albumin: float = Form(...),
#     protime: float = Form(...),
#     ast: float = Form(...),
#     file: UploadFile = File(...)
# ):
#     clinical_data = {
#         "bili": bilirubin,
#         "albumin": albumin,
#         "protime": protime,
#         "sgot": ast
#     }

#     try:
#         img_bytes = await file.read()
#         print("Clinical data:", clinical_data)
#         print("Image bytes length:", len(img_bytes))

#         result = hybrid_model.predict(clinical_data, img_bytes)
#         return result

#     except Exception as e:
#         print("HYBRID ERROR:", e)   # 👈 THIS LINE
#         raise HTTPException(status_code=400, detail=str(e))
    

# @app.get("/")
# def home():
#     return {"message": "Cirrhox backend running!"}
