from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    location = Column(String)
    merchant = Column(String)
    status = Column(String)
    risk_score = Column(Float)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
