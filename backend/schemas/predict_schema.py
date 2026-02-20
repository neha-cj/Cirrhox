from pydantic import BaseModel

class PredictInput(BaseModel):
    bilirubin: float
    albumin: float
    protime: float
    ast: float