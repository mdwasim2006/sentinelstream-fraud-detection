from app.services.idempotency import is_duplicate, mark_processed
from app.rules.risk_rules import evaluate_risk
from app.schemas.transaction import TransactionRequest, TransactionResponse
from fastapi import APIRouter

router = APIRouter()

@router.post("/transaction", response_model=TransactionResponse)
def process_transaction(txn: TransactionRequest):

    # 🔐 Idempotency check
    if is_duplicate(txn.idempotency_key):
        return TransactionResponse(
            status="DUPLICATE",
            risk_score=0.0,
            message="Duplicate transaction ignored"
        )

    status, risk_score, reasons = evaluate_risk(
        txn.amount,
        txn.location,
        txn.merchant
    )

    response = TransactionResponse(
        status=status,
        risk_score=risk_score,
        message=", ".join(reasons) if reasons else "Transaction safe"
    )

    # Mark as processed
    mark_processed(txn.idempotency_key, response)

    return response
