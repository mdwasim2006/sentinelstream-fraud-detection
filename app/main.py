from fastapi import FastAPI
from app.api.transaction import router as transaction_router

app = FastAPI(title="SentinelStream – Fraud Detection Engine")

@app.get("/health")
def health():
    return {"status": "UP", "service": "SentinelStream"}

app.include_router(transaction_router)
