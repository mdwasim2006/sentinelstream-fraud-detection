from fastapi import FastAPI

# ✅ Database setup
from app.db.session import engine
from app.db.models import Base

# ✅ API routers
from app.api.transaction import router as transaction_router


# 🔹 Create DB tables at startup (idempotent & safe)
Base.metadata.create_all(bind=engine)


# 🚀 FastAPI app (Swagger ENABLED explicitly)
app = FastAPI(
    title="SentinelStream – Fraud Detection Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ❤️ Health check
@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "SentinelStream"
    }


# 🔌 Register API routes
app.include_router(transaction_router)
