from pydantic import BaseModel

class TransactionRequest(BaseModel):
    user_id: str
    amount: float
    location: str
    merchant: str
    timestamp: str
    idempotency_key: str

class TransactionResponse(BaseModel):
    status: str
    risk_score: float
    message: str
