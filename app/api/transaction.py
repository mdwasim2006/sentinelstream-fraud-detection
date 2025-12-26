from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.transaction import TransactionRequest, TransactionResponse
from app.models.transaction_db import Transaction
from app.db.session import get_db

router = APIRouter()

@router.post("/transaction", response_model=TransactionResponse)
async def process_transaction(
    txn: TransactionRequest,
    db: AsyncSession = Depends(get_db)
):
    # 1️⃣ Check idempotency key
    query = select(Transaction).where(
        Transaction.idempotency_key == txn.idempotency_key
    )
    result = await db.execute(query)
    existing_txn = result.scalar_one_or_none()

    if existing_txn:
        # Duplicate request detected
        return TransactionResponse(
            status="DUPLICATE",
            risk_score=0.10,
            message="Duplicate transaction ignored"
        )

    # 2️⃣ Save new transaction
    new_txn = Transaction(
        user_id=txn.user_id,
        amount=txn.amount,
        location=txn.location,
        merchant=txn.merchant,
        timestamp=txn.timestamp,
        idempotency_key=txn.idempotency_key
    )

    db.add(new_txn)
    await db.commit()

    return TransactionResponse(
        status="APPROVED",
        risk_score=0.10,
        message="Transaction processed successfully"
    )
