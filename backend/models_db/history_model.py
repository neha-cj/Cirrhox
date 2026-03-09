from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class PredictionHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    prediction  = Column(String)
    probability = Column(Float)
    severity    = Column(String)

    bilirubin = Column(Float)
    albumin   = Column(Float)
    ast       = Column(Float)
    alt       = Column(Float)
    alp       = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="history")
    doctor = relationship("User", foreign_keys=[doctor_id])