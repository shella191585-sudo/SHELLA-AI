import argparse
from datetime import date, datetime, timedelta, timezone

from app.analysis import analyze_market
from app.config import settings
from app.content import generate_x_post
from app.data import BtcProvider, GoldProvider, StocksProvider
from app.database import Database
from app.feedback import record_available_outcomes
from app.indicators import momentum_indicators, trend_indicators, unavailable_macro, volatility_indicators
from app.llm import LLMClient
from app.reports import build_daily_report
from app.risk import assess_risk

PROVIDERS = (BtcProvider(), GoldProvider(), StocksProvider())


def run(days: int) -> str:
    db, llm = Database(settings.database_path), LLMClient(settings.llm_provider, settings.llm_api_key, settings.llm_model)
    end, start, report_entries = date.today(), date.today() - timedelta(days=days), []
    for provider in PROVIDERS:
        frame = provider.get_price_history(provider.symbol, start, end)
        db.store_candles(frame)
        indicators = {**trend_indicators(frame["close"]), **momentum_indicators(frame["close"]), **volatility_indicators(frame)}
        macro = unavailable_macro()
        analysis = analyze_market(provider.asset, indicators, macro, llm)
        risk = assess_risk(indicators, macro).to_dict()
        latest = frame.iloc[-1]
        timestamp = latest.timestamp.isoformat()
        db.store_analysis(timestamp=timestamp, asset=provider.asset, symbol=provider.symbol, source=latest.source,
                          inputs={column: (None if latest[column] != latest[column] else latest[column]) for column in ("open", "high", "low", "close", "volume")},
                          indicators=indicators, macro=macro, analysis=analysis, risk=risk)
        report_entries.append({"asset": provider.asset, "indicators": indicators, "analysis": analysis, "risk": risk, "x_post": generate_x_post(provider.asset, risk, analysis)})
    return str(build_daily_report(datetime.now(timezone.utc).isoformat(), report_entries, settings.reports_dir))


def main() -> None:
    parser = argparse.ArgumentParser(description="Market-state research loop; never executes trades.")
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run"); run_parser.add_argument("--days", type=int, default=260)
    eval_parser = sub.add_parser("evaluate"); eval_parser.add_argument("--horizon-days", type=int, default=20)
    feedback = sub.add_parser("feedback"); feedback.add_argument("analysis_id", type=int); feedback.add_argument("--rating", type=int, required=True); feedback.add_argument("--note")
    args = parser.parse_args(); db = Database(settings.database_path)
    if args.command == "run": print(run(args.days))
    elif args.command == "evaluate": print(f"Recorded {record_available_outcomes(db, args.horizon_days)} outcomes.")
    else:
        db.add_feedback(args.analysis_id, args.rating, args.note, datetime.now(timezone.utc).isoformat()); print("Feedback saved.")


if __name__ == "__main__":
    main()
