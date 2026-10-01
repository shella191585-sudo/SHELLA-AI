from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: str
    confidence: float
    reasons: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def assess_risk(indicators: dict, macro: dict) -> RiskAssessment:
    """Deterministic, explainable 0–100 risk framework; it does not predict prices."""
    score, reasons = 30, ["Baseline market uncertainty."]
    if indicators.get("trend") == "BEARISH":
        score += 25; reasons.append("Price is below all available trend moving averages.")
    elif indicators.get("trend") == "NEUTRAL":
        score += 10; reasons.append("Trend signals are mixed.")
    if (vol := indicators.get("realized_vol_20d_pct")) is not None and vol >= 35:
        score += 20; reasons.append(f"20-day realized volatility is elevated ({vol:.1f}%).")
    if (drawdown := indicators.get("max_drawdown_pct")) is not None and drawdown <= -20:
        score += 15; reasons.append(f"Observed maximum drawdown is severe ({drawdown:.1f}%).")
    if (rsi := indicators.get("rsi14")) is not None and (rsi >= 75 or rsi <= 25):
        score += 10; reasons.append(f"RSI is at an extreme ({rsi:.1f}); treated as context, not a trade signal.")
    confidence = 0.85 if macro.get("status") != "unavailable" else 0.70
    if macro.get("status") == "unavailable":
        reasons.append("Confidence reduced because macro inputs are unavailable.")
    score = min(score, 100)
    level = "HIGH" if score >= 70 else "ELEVATED" if score >= 50 else "MODERATE" if score >= 30 else "LOW"
    return RiskAssessment(score, level, confidence, reasons)
