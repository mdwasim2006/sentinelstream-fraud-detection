def evaluate_risk(amount: float, location: str, merchant: str) -> tuple:
    risk_score = 0.0
    reasons = []

    # Rule 1: High amount
    if amount > 5000:
        risk_score += 0.6
        reasons.append("High transaction amount")

    # Rule 2: Unknown location
    if location.lower() in ["unknown", "foreign", "untrusted"]:
        risk_score += 0.3
        reasons.append("Untrusted location")

    # Rule 3: Suspicious merchant
    if merchant.lower() in ["fakeShop", "shadyStore"]:
        risk_score += 0.4
        reasons.append("Risky merchant")

    # Final status
    if risk_score >= 0.7:
        status = "HIGH_RISK"
    elif risk_score >= 0.3:
        status = "MEDIUM_RISK"
    else:
        status = "LOW_RISK"

    return status, min(risk_score, 1.0), reasons
