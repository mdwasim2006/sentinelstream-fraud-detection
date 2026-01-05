from fastapi import FastAPI

# ✅ Correct DB imports
from app.db.database import engine
from app.db.models import Base

# ✅ API router
from app.api.transaction import router as transaction_router


# 🔹 Create DB tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SentinelStream – Fraud Detection Engine",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "UP", "service": "SentinelStream"}


# 🔌 Register routes
app.include_router(transaction_router)
