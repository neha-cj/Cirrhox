from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class PredictionHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prediction = Column(String)
    probability = Column(Float)
