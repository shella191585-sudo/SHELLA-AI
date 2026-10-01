from app.risk.engine import assess_risk


def test_bearish_high_volatility_is_high_risk():
    risk = assess_risk({"trend": "BEARISH", "realized_vol_20d_pct": 45, "max_drawdown_pct": -25, "rsi14": 20}, {"status": "unavailable"})
    assert risk.level == "HIGH" and risk.score == 100 and risk.confidence == 0.70
