from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisRecord:
    id: int
    asset: str
    timestamp: str
    risk_score: int
    risk_level: str
