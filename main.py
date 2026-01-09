import asyncio
from scanner_async import fetch_top_symbols, scan_symbol
from telegram_utils import send_signal
from config import TIMEFRAMES, TOP_COINS_LIMIT

SCAN_INTERVAL = 3600  # seconds


async def scan_all():
    symbols = await fetch_top_symbols(TOP_COINS_LIMIT)

    while True:
        for tf in TIMEFRAMES:
            tasks = [
                scan_symbol(symbol, tf)
                for symbol in symbols
            ]

            results = await asyncio.gather(*tasks)

            for signal in results:
                if signal:
                    send_signal(signal)

        await asyncio.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    asyncio.run(scan_all())
