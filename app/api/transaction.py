from fastapi import APIRouter

from app.schemas.transaction import TransactionRequest, TransactionResponse
from app.services.idempotency import is_duplicate, mark_processed
from app.features.transaction_features import extract_transaction_features
from app.risk.scorer import score_transaction
from app.services.velocity_check import check_velocity

router = APIRouter()


@router.post("/transaction", response_model=TransactionResponse)
def process_transaction(txn: TransactionRequest):
    try:
        # 🔐 Idempotency check (always first)
        if is_duplicate(txn.idempotency_key):
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

        # 🧮 Base risk scoring
        risk_result = score_transaction(features)

        # 🚨 Velocity / behavior check
        velocity_risk = check_velocity(txn.user_id)

        if velocity_risk > 0:
            risk_result["risk_score"] = round(
                min(risk_result["risk_score"] + velocity_risk, 1.0), 2
            )
            risk_result["reasons"].append("High transaction frequency")

            # Re-evaluate risk level after velocity impact
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

        # ✅ Mark transaction as processed (idempotency memory)
        mark_processed(txn.idempotency_key, response)

        return response

    except Exception as e:
        # 🛡️ Hardened fallback (no API crash)
        return TransactionResponse(
            status="ERROR",
            risk_score=0.0,
            message="Transaction processing failed safely"
        )
