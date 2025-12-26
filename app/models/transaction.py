from pydantic import BaseModel
from datetime import datetime

class TransactionRequest(BaseModel):
    user_id: str
    amount: float
    location: str
    merchant: str
    timestamp: datetime
    idempotency_key: str


class TransactionResponse(BaseModel):
    status: str
    risk_score: float
    message: str
