def score_transaction(features: dict) -> dict:
    score = 0.0
    reasons = []

    if features["is_high_amount"]:
        score += 0.4
        reasons.append("High transaction amount")

    if features["is_night_transaction"]:
        score += 0.2
        reasons.append("Night-time transaction")

    if features["is_unknown_city"]:
        score += 0.25
        reasons.append("Unknown city")

    if features["is_unknown_merchant"]:
        score += 0.15
        reasons.append("Unknown merchant")

    # Clamp score to max 1.0
    score = min(score, 1.0)

    if score >= 0.7:
        level = "HIGH_RISK"
    elif score >= 0.4:
        level = "MEDIUM_RISK"
    else:
        level = "LOW_RISK"

    return {
        "risk_score": round(score, 2),
        "risk_level": level,
        "reasons": reasons
    }
