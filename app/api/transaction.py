from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.schemas.transaction import TransactionRequest, TransactionResponse
from app.services.idempotency import is_duplicate, mark_processed
from app.features.transaction_features import extract_transaction_features
from app.risk.scorer import score_transaction
from app.services.velocity_check import check_velocity
from app.db.session import get_db
from app.db.repository import save_transaction

router = APIRouter()
logger = get_logger("transaction-api")


@router.post("/transaction", response_model=TransactionResponse)
def process_transaction(
    txn: TransactionRequest,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Transaction received | user={txn.user_id}")

        # 🔐 Idempotency
        if is_duplicate(txn.idempotency_key):
            logger.warning("Duplicate transaction blocked")
            return TransactionResponse(
                status="DUPLICATE",
                risk_score=0.0,
                message="Duplicate transaction ignored"
            )

        # 🧠 Feature extraction
        features = extract_transaction_features({
            "amount": txn.amount,
            "timestamp": txn.timestamp,
            "location": txn.location,
            "merchant": txn.merchant
        })

        # 🧮 Risk scoring
        risk_result = score_transaction(features)

        # 🚨 Velocity check
        velocity_risk = check_velocity(txn.user_id)
        if velocity_risk > 0:
            risk_result["risk_score"] = round(
                min(risk_result["risk_score"] + velocity_risk, 1.0), 2
            )
            risk_result["reasons"].append("High transaction frequency")

            if risk_result["risk_score"] >= 0.7:
                risk_result["risk_level"] = "HIGH_RISK"
            elif risk_result["risk_score"] >= 0.4:
                risk_result["risk_level"] = "MEDIUM_RISK"
            else:
                risk_result["risk_level"] = "LOW_RISK"

        response = TransactionResponse(
            status=risk_result["risk_level"],
            risk_score=risk_result["risk_score"],
            message=", ".join(risk_result["reasons"]) or "Transaction safe"
        )

        # 💾 Save to DB
        save_transaction(
            db=db,
            user_id=txn.user_id,
            amount=txn.amount,
            location=txn.location,
            merchant=txn.merchant,
            status=response.status,
            risk_score=response.risk_score,
            message=response.message
        )

        mark_processed(txn.idempotency_key, response)

        logger.info(
            f"Transaction processed | status={response.status} | score={response.risk_score}"
        )

        return response

    except Exception as e:
        logger.error(f"Transaction failed: {str(e)}")
        return TransactionResponse(
            status="ERROR",
            risk_score=0.0,
            message="Transaction processing failed safely"
        )
