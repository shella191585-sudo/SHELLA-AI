def pct(value: float | None) -> str:
    return "unavailable" if value is None else f"{value:.2f}%"
