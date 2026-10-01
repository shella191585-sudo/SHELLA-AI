def cross_asset_returns(indicators_by_asset: dict) -> dict:
    """Expose known 20-day changes without inferring relationships from missing data."""
    return {asset: values.get("change_20d_pct") for asset, values in indicators_by_asset.items()}
