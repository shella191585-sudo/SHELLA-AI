from app.reports.daily import build_daily_report


def test_report_includes_risk_and_x_draft(tmp_path):
    path = build_daily_report("2026-01-01T00:00:00+00:00", [{"asset": "BTC", "indicators": {"trend": "BULLISH", "rsi14": 55, "change_20d_pct": 3}, "risk": {"level": "MODERATE", "score": 30, "confidence": .7, "reasons": ["baseline"]}, "analysis": {"narrative": "Stable."}, "x_post": "post"}], tmp_path)
    assert "BTC" in path.read_text() and "X draft" in path.read_text()
