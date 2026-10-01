from pathlib import Path

from .formatter import pct


def build_daily_report(timestamp: str, entries: list[dict], output_dir: Path) -> Path:
    lines = [f"# Daily Market Intelligence Report — {timestamp[:10]}", "", "Research only; not investment advice.", ""]
    for item in entries:
        i, r = item["indicators"], item["risk"]
        lines += [f"## {item['asset']}", f"- **Risk:** {r['level']} ({r['score']}/100); confidence {r['confidence']:.0%}",
                  f"- **Trend:** {i['trend']}; RSI(14): {i.get('rsi14') if i.get('rsi14') is not None else 'unavailable'}; 20-day change: {pct(i.get('change_20d_pct'))}",
                  f"- **Reasoning:** {' '.join(r['reasons'])}", f"- **Analysis:** {item['analysis']['narrative']}", f"- **X draft:** {item['x_post']}", ""]
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"daily-{timestamp[:10]}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
