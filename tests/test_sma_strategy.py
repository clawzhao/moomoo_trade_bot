"""Tests for SMAStrategy."""
import pytest
from datetime import datetime
from strategy.sma_strategy import SMAStrategy
from utils import config


@pytest.fixture
def sample_config():
    return config.Config(
        account_id="test",
        api_key="key",
        api_secret="secret",
        env="SIMULATION",
    )


def test_sma_buy_signal(sample_config):
    strat = SMAStrategy(sample_config, fast=2, slow=3)
    strat.initialize()
    # Feed 3 bars with rising prices
    bars = [
        {"timestamp": datetime(2025, 1, 1, 0, 0), "open": 100, "high": 101, "low": 99, "close": 100, "volume": 1000},
        {"timestamp": datetime(2025, 1, 1, 1, 0), "open": 101, "high": 102, "low": 100, "close": 101, "volume": 1100},
        {"timestamp": datetime(2025, 1, 1, 2, 0), "open": 102, "high": 103, "low": 101, "close": 102, "volume": 1200},
    ]
    signal = strat.on_bar(bars[0])
    assert signal is None
    signal = strat.on_bar(bars[1])
    assert signal is None
    signal = strat.on_bar(bars[2])
    assert signal is not None
    assert signal["action"] == "BUY"
    assert signal["symbol"] == "AAPL"


def test_sma_sell_signal(sample_config):
    strat = SMAStrategy(sample_config, fast=2, slow=3)
    strat.initialize()
    # First build a long position
    bars_up = [
        {"timestamp": datetime(2025, 1, 1, 0, 0), "open": 100, "high": 101, "low": 99, "close": 100, "volume": 1000},
        {"timestamp": datetime(2025, 1, 1, 1, 0), "open": 101, "high": 102, "low": 100, "close": 101, "volume": 1100},
        {"timestamp": datetime(2025, 1, 1, 2, 0), "open": 102, "high": 103, "low": 101, "close": 102, "volume": 1200},
    ]
    for b in bars_up:
        strat.on_bar(b)
    # Now price drops
    bars_down = [
        {"timestamp": datetime(2025, 1, 1, 3, 0), "open": 103, "high": 104, "low": 101, "close": 101, "volume": 1300},
        {"timestamp": datetime(2025, 1, 1, 4, 0), "open": 101, "high": 102, "low": 99, "close": 99, "volume": 1400},
        {"timestamp": datetime(2025, 1, 1, 5, 0), "open": 99, "high": 100, "low": 98, "close": 98, "volume": 1500},
    ]
    for b in bars_down:
        signal = strat.on_bar(b)
        if signal:
            assert signal["action"] == "SELL"
            return
    assert False, "Expected sell signal but none generated"
