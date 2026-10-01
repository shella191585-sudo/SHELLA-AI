from app.llm.client import LLMClient


def analyze_market(asset: str, indicators: dict, macro: dict, llm: LLMClient) -> dict:
    """Generate interpretation only. The deterministic engine owns the final score."""
    facts = f"{asset}: trend={indicators['trend']}, RSI14={indicators.get('rsi14')}, 20d change={indicators.get('change_20d_pct')}%, volatility={indicators.get('volatility')}."
    fallback = f"Market state for {facts} Macro status: {macro['status']}."
    narrative = llm.complete(facts) or fallback
    return {"narrative": narrative, "provider": llm.provider, "input_facts": facts}
