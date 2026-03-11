"""Telegram notification utility."""
import asyncio
import os
from typing import Optional

import aiohttp


async def send_telegram_message(
    text: str, parse_mode: str = "HTML", chat_id: Optional[str] = None
) -> bool:
    """
    Send a message to a Telegram chat.

    Args:
        text: The message text.
        parse_mode: 'HTML' or 'MarkdownV2'.
        chat_id: Override default chat ID if provided.

    Returns:
        True if sent successfully, False otherwise.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    default_chat = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not (chat_id or default_chat):
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "text": text,
        "parse_mode": parse_mode,
        "chat_id": chat_id or default_chat,
        "disable_web_page_preview": True,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as resp:
                return resp.status == 200
    except Exception:
        return False


# Synchronous wrapper for convenience
def send_telegram_sync(text: str, **kwargs) -> bool:
    """Blocking version of send_telegram_message."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Create a new event loop in a thread if needed; for simplicity, use asyncio.run
        return asyncio.run(send_telegram_message(text, **kwargs))
    else:
        return asyncio.run(send_telegram_message(text, **kwargs))
