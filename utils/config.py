"""Configuration loader for the trading bot."""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Holds all configuration values."""
    account_id: str
    api_key: str
    api_secret: str
    host: str = "127.0.0.1"
    port: int = 11111
    market: str = "US"
    env: str = "SIMULATION"  # SIMULATION or REAL
    log_level: str = "INFO"
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment variables."""
        return cls(
            account_id=os.getenv("MOOMOO_ACCOUNT_ID", ""),
            api_key=os.getenv("MOOMOO_API_KEY", ""),
            api_secret=os.getenv("MOOMOO_API_SECRET", ""),
            host=os.getenv("MOOMOO_HOST", "127.0.0.1"),
            port=int(os.getenv("MOOMOO_PORT", 11111)),
            market=os.getenv("MOOMOO_MARKET", "US"),
            env=os.getenv("MOOMOO_ENV", "SIMULATION"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        )

    def validate(self) -> None:
        """Ensure required fields are set."""
        required = ["account_id", "api_key", "api_secret"]
        missing = [f for f in required if not getattr(self, f)]
        if missing:
            raise ValueError(f"Missing required config fields: {missing}")
