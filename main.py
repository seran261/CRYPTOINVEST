from scanner import fetch_top_symbols, scan_symbol
from telegram_utils import send_signal
from config import TIMEFRAMES, TOP_COINS_LIMIT
import time

symbols = fetch_top_symbols(TOP_COINS_LIMIT)

while True:
    for tf in TIMEFRAMES:
        for symbol in symbols:
            try:
                signal = scan_symbol(symbol, tf)
                if signal:
                    send_signal(signal)
                    time.sleep(2)
            except Exception as e:
                print(symbol, e)

    time.sleep(3600)
