from datetime import datetime

HIGH_AMOUNT_THRESHOLD = 5000
NIGHT_HOURS = range(0, 6)

KNOWN_CITIES = {"Chennai", "Bangalore", "Hyderabad"}
KNOWN_MERCHANTS = {"Amazon", "Flipkart", "Swiggy"}


def extract_transaction_features(txn: dict) -> dict:
    amount = txn["amount"]
    timestamp = datetime.fromisoformat(txn["timestamp"])
    city = txn["location"]
    merchant = txn["merchant"]

    features = {
        "is_high_amount": amount > HIGH_AMOUNT_THRESHOLD,
        "is_night_transaction": timestamp.hour in NIGHT_HOURS,
        "is_unknown_city": city not in KNOWN_CITIES,
        "is_unknown_merchant": merchant not in KNOWN_MERCHANTS,
    }

    return features
