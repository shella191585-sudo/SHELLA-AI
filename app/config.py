from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_path: Path = Path(os.getenv("DATABASE_PATH", "data/market.db"))
    reports_dir: Path = Path(os.getenv("REPORTS_DIR", "reports"))
    market_data_provider: str = os.getenv("MARKET_DATA_PROVIDER", "yahoo")
    llm_provider: str = os.getenv("LLM_PROVIDER", "disabled")
    llm_api_key: str | None = os.getenv("LLM_API_KEY") or None
    llm_model: str | None = os.getenv("LLM_MODEL") or None


settings = Settings()
