from fastapi import FastAPI
from app.api.transaction import router as transaction_router
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="SentinelStream Fraud Detection Engine")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
def health():
    return {"status": "UP", "service": "SentinelStream"}

app.include_router(transaction_router)
