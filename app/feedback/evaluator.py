from datetime import datetime, timedelta, timezone

from app.database.db import Database


def record_available_outcomes(db: Database, horizon_days: int) -> int:
    """Attach observed returns only after the requested calendar horizon has elapsed."""
    now = datetime.now(timezone.utc)
    count = 0
    for row in db.pending_outcomes(horizon_days):
        start = datetime.fromisoformat(row["timestamp"])
        if now < start + timedelta(days=horizon_days):
            continue
        observed = db.close_for_symbol_on_or_after(row["symbol"], (start + timedelta(days=horizon_days)).isoformat())
        if observed is None:
            continue
        inputs = __import__("json").loads(row["input_values_json"])
        return_pct = (float(observed["close"]) / float(inputs["close"]) - 1) * 100
        db.store_outcome(row["id"], horizon_days, observed["timestamp"], observed["close"], return_pct)
        count += 1
    return count
