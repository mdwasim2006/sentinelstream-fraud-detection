from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import Transaction
from app.core.logger import get_logger


logger = get_logger("db-repository")


def save_transaction(
    db: Session,
    user_id: str,
    amount: float,
    location: str,
    merchant: str,
    status: str,
    risk_score: float,
    message: str
):
    """
    Persist a processed transaction into PostgreSQL.
    """

    try:
        txn = Transaction(
            user_id=user_id,
            amount=amount,
            location=location,
            merchant=merchant,
            status=status,
            risk_score=risk_score,
            message=message
        )

        db.add(txn)
        db.commit()
        db.refresh(txn)

        logger.info(
            f"Transaction stored | user={user_id} | status={status} | score={risk_score}"
        )

        return txn

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(
            f"DB write failed | user={user_id} | error={str(e)}"
        )
        raise
