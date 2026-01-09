import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is not set")

if not CHAT_ID:
    raise RuntimeError("CHAT_ID is not set")

TIMEFRAMES = ["1d", "1w"]
TOP_COINS_LIMIT = 200

BREAKOUT_CONFIRM_CANDLES = 1
RETEST_LOOKAHEAD = 3

VOLUME_MULTIPLIER = 1.5
