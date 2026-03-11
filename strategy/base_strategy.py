"""Abstract base class for trading strategies."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseStrategy(ABC):
    """Abstract strategy interface."""

    def __init__(self, config: "config.Config"):
        self.config = config
        self.logger = None  # Will be set by the engine

    @abstractmethod
    def initialize(self) -> None:
        """Called once before the first data bar."""
        pass

    @abstractmethod
    def on_bar(self, bar: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a new OHLC bar.

        Args:
            bar: dict with keys: timestamp, open, high, low, close, volume

        Returns:
            A signal dict: { "action": "BUY"|"SELL", "symbol": str, "qty": int, "price": float }
            or None if no signal.
        """
        pass

    @abstractmethod
    def on_trade(self, trade: Dict[str, Any]) -> None:
        """
        Called when an order is filled.
        """
        pass

    def shutdown(self) -> None:
        """Called before shutdown to cleanup resources."""
        pass
