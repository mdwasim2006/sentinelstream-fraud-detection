from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    location = Column(String)
    merchant = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    idempotency_key = Column(String, unique=True)
