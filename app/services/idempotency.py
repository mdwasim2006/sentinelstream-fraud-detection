processed_transactions = {}

def is_duplicate(idempotency_key: str):
    return idempotency_key in processed_transactions

def mark_processed(idempotency_key: str, response):
    processed_transactions[idempotency_key] = response
