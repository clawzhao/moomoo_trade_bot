"""Simple SMA Crossover strategy."""
from collections import deque
from typing import Deque, Dict, Any, Optional

from .base_strategy import BaseStrategy
import config


class SMAStrategy(BaseStrategy):
    """Moving average crossover strategy."""

    def __init__(self, cfg: config.Config, fast: int = 10, slow: int = 30):
        super().__init__(cfg)
        self.fast_period = fast
        self.slow_period = slow
        self.closes: Deque[float] = deque(maxlen=slow)
        self.position: Optional[str] = None  # "LONG" or "SHORT"

    def initialize(self) -> None:
        self.closes.clear()
        self.position = None
        if self.logger:
            self.logger.info(
                f"SMAStrategy initialized: fast={self.fast_period}, slow={self.slow_period}"
            )

    def on_bar(self, bar: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        close = bar["close"]
        self.closes.append(close)

        if len(self.closes) < self.slow_period:
            return None

        fast_ma = sum(list(self.closes)[-self.fast_period :]) / self.fast_period
        slow_ma = sum(self.closes) / self.slow_period

        signal = None
        if fast_ma > slow_ma and self.position != "LONG":
            signal = {"action": "BUY", "symbol": "AAPL", "qty": 100, "price": close}
            self.position = "LONG"
        elif fast_ma < slow_ma and self.position == "LONG":
            signal = {"action": "SELL", "symbol": "AAPL", "qty": 100, "price": close}
            self.position = None

        return signal

    def on_trade(self, trade: Dict[str, Any]) -> None:
        if self.logger:
            self.logger.info(f"Trade executed: {trade}")

    def shutdown(self) -> None:
        if self.logger:
            self.logger.info("SMAStrategy shutting down")
