from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import TransactionRequest, TransactionResponse
from app.models.transaction_db import Transaction
from app.db.session import get_db

router = APIRouter()

@router.post("/transaction", response_model=TransactionResponse)
async def process_transaction(
    txn: TransactionRequest,
    db: AsyncSession = Depends(get_db)
):
    record = Transaction(
        user_id=txn.user_id,
        amount=txn.amount,
        location=txn.location,
        merchant=txn.merchant,
        timestamp=txn.timestamp,
        idempotency_key=txn.idempotency_key
    )
    db.add(record)
    await db.commit()

    return TransactionResponse(
        status="APPROVED",
        risk_score=0.10,
        message="Transaction stored successfully"
    )
