import time

# Temporary in-memory store (Phase 2 version)
# In Phase 3, this will move fully to Redis
USER_TXN_WINDOW = {}
WINDOW_SECONDS = 60
MAX_TXNS = 3


def check_velocity(user_id: str) -> float:
    now = time.time()

    if user_id not in USER_TXN_WINDOW:
        USER_TXN_WINDOW[user_id] = []

    # Keep only recent timestamps
    USER_TXN_WINDOW[user_id] = [
        t for t in USER_TXN_WINDOW[user_id]
        if now - t <= WINDOW_SECONDS
    ]

    USER_TXN_WINDOW[user_id].append(now)

    if len(USER_TXN_WINDOW[user_id]) > MAX_TXNS:
        return 0.3  # add extra risk

    return 0.0
