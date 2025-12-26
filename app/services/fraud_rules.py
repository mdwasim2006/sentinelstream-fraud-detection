def evaluate_fraud(transaction):
    risk_score = 0.0
    reasons = []

    # Rule 1: High amount
    if transaction.amount > 5000:
        risk_score += 0.5
        reasons.append("High transaction amount")

    # Rule 2: Location risk
    trusted_locations = ["Chennai", "Bangalore", "Hyderabad"]
    if transaction.location not in trusted_locations:
        risk_score += 0.3
        reasons.append("Untrusted location")

    # Rule 3: Risky merchant
    risky_merchants = ["UnknownStore", "FakeShop"]
    if transaction.merchant in risky_merchants:
        risk_score += 0.2
        reasons.append("Risky merchant")

    status = "HIGH_RISK" if risk_score >= 0.7 else "LOW_RISK"

    return status, round(risk_score, 2), reasons
