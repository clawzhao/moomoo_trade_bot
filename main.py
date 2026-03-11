"""Main entry point for the moomoo trading bot."""
import argparse
import asyncio
import csv
import logging
from datetime import datetime
from pathlib import Path

from utils.config import Config
from utils.logger import setup_logger
from utils.telegram import send_telegram_message
from strategy.sma_strategy import SMAStrategy


async def main():
    parser = argparse.ArgumentParser(description="Moomoo Trading Bot")
    parser.add_argument(
        "--data",
        type=str,
        default="data/sample_ohlc.csv",
        help="Path to CSV file with OHLC data",
    )
    parser.add_argument(
        "--fast", type=int, default=10, help="Fast SMA period"
    )
    parser.add_argument(
        "--slow", type=int, default=30, help="Slow SMA period"
    )
    args = parser.parse_args()

    # Load config
    try:
        cfg = Config.from_env()
        cfg.validate()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        return

    logger = setup_logger(
        log_file=Path("logs", "bot.log"),
        level=cfg.log_level,
    )
    logger.info("Starting moomoo_trade_bot")

    # Telegram startup notification
    if cfg.telegram_bot_token and cfg.telegram_chat_id:
        await send_telegram_message(
            f"<b>🚀 Bot Started</b>\nEnv: {cfg.env}\nStrategy: SMA Crossover ({args.fast}/{args.slow})"
        )

    # Initialize strategy
    strategy = SMAStrategy(cfg, fast=args.fast, slow=args.slow)
    strategy.logger = logger
    strategy.initialize()

    # Load and iterate over CSV data
    data_path = Path(args.data)
    if not data_path.exists():
        logger.error(f"Data file not found: {data_path}")
        return

    trades = []
    with open(data_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bar = {
                "timestamp": datetime.fromisoformat(row["timestamp"]),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": int(row["volume"]),
            }
            signal = strategy.on_bar(bar)
            if signal:
                logger.info(f"Signal: {signal}")
                trades.append(signal)
                # Here you would send order via Moomoo API
                # await send_order(signal)

    strategy.shutdown()
    logger.info(f"Backtest complete. {len(trades)} signals generated.")

    if cfg.telegram_bot_token and cfg.telegram_chat_id:
        await send_telegram_message(
            f"<b>✅ Backtest Finished</b>\nSignals: {len(trades)}\nCheck logs for details."
        )


if __name__ == "__main__":
    asyncio.run(main())
