import json
import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


class Database:
    def __init__(self, path: Path | str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS candles (
          timestamp TEXT NOT NULL, symbol TEXT NOT NULL, open REAL, high REAL, low REAL, close REAL NOT NULL,
          volume REAL, source TEXT NOT NULL, PRIMARY KEY(timestamp, symbol, source));
        CREATE TABLE IF NOT EXISTS analyses (
          id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, asset TEXT NOT NULL, symbol TEXT NOT NULL, source TEXT NOT NULL,
          input_values_json TEXT NOT NULL, indicators_json TEXT NOT NULL, macro_json TEXT NOT NULL, analysis_json TEXT NOT NULL,
          risk_score INTEGER NOT NULL, risk_level TEXT NOT NULL, confidence REAL NOT NULL, reasoning_json TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS outcomes (
          analysis_id INTEGER NOT NULL, horizon_days INTEGER NOT NULL, observed_at TEXT NOT NULL, close REAL NOT NULL,
          return_pct REAL NOT NULL, PRIMARY KEY(analysis_id, horizon_days), FOREIGN KEY(analysis_id) REFERENCES analyses(id));
        CREATE TABLE IF NOT EXISTS feedback (
          id INTEGER PRIMARY KEY, analysis_id INTEGER NOT NULL, created_at TEXT NOT NULL, rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
          note TEXT, FOREIGN KEY(analysis_id) REFERENCES analyses(id));
        """)
        self.connection.commit()

    def store_candles(self, frame: "pd.DataFrame") -> None:
        rows = [(row.timestamp.isoformat(), row.symbol, row.open, row.high, row.low, row.close, row.volume, row.source) for row in frame.itertuples(index=False)]
        self.connection.executemany("INSERT OR REPLACE INTO candles VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)
        self.connection.commit()

    def store_analysis(self, *, timestamp: str, asset: str, symbol: str, source: str, inputs: dict, indicators: dict, macro: dict, analysis: dict, risk: dict) -> int:
        cursor = self.connection.execute("""INSERT INTO analyses VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            timestamp, asset, symbol, source, json.dumps(inputs), json.dumps(indicators), json.dumps(macro), json.dumps(analysis),
            risk["score"], risk["level"], risk["confidence"], json.dumps(risk["reasons"])))
        self.connection.commit(); return int(cursor.lastrowid)

    def add_feedback(self, analysis_id: int, rating: int, note: str | None, created_at: str) -> None:
        self.connection.execute("INSERT INTO feedback VALUES (NULL,?,?,?,?)", (analysis_id, created_at, rating, note)); self.connection.commit()

    def pending_outcomes(self, horizon_days: int):
        return self.connection.execute("""SELECT a.* FROM analyses a LEFT JOIN outcomes o ON o.analysis_id=a.id AND o.horizon_days=? WHERE o.analysis_id IS NULL""", (horizon_days,)).fetchall()

    def close_for_symbol_on_or_after(self, symbol: str, timestamp: str):
        return self.connection.execute("SELECT timestamp, close FROM candles WHERE symbol=? AND timestamp>=? ORDER BY timestamp LIMIT 1", (symbol, timestamp)).fetchone()

    def store_outcome(self, analysis_id: int, horizon_days: int, observed_at: str, close: float, return_pct: float) -> None:
        self.connection.execute("INSERT OR REPLACE INTO outcomes VALUES (?,?,?,?,?)", (analysis_id, horizon_days, observed_at, close, return_pct)); self.connection.commit()
