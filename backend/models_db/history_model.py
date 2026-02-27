from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class PredictionHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    prediction = Column(String)
    probability = Column(Float)
    severity = Column(String)   # ✅ NEW COLUMN

    bilirubin = Column(Float)
    albumin = Column(Float)
    protime = Column(Float)
    ast = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="history")