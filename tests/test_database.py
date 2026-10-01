from app.database import Database


def test_database_stores_analysis_and_feedback(tmp_path):
    db = Database(tmp_path / "market.db")
    analysis_id = db.store_analysis(timestamp="2026-01-01T00:00:00+00:00", asset="BTC", symbol="BTC-USD", source="test", inputs={"close": 1}, indicators={}, macro={}, analysis={}, risk={"score": 30, "level": "MODERATE", "confidence": .7, "reasons": []})
    db.add_feedback(analysis_id, 5, "clear", "2026-01-01T01:00:00+00:00")
    assert db.connection.execute("SELECT rating FROM feedback").fetchone()[0] == 5
