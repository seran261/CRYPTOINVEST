import asyncio
from scanner_async import fetch_top_symbols, scan_symbol
from telegram_utils import send_signal, app
from tracker import add_trade
from price_watcher import monitor_trades
from config import TIMEFRAMES, TOP_COINS_LIMIT

SCAN_INTERVAL = 3600

async def scan_loop():
    symbols = await fetch_top_symbols(TOP_COINS_LIMIT)

    while True:
        for tf in TIMEFRAMES:
            tasks = [scan_symbol(symbol, tf) for symbol in symbols]
            results = await asyncio.gather(*tasks)

            for signal in results:
                if signal:
                    await send_signal(signal)
                    add_trade(signal)

        await asyncio.sleep(SCAN_INTERVAL)

async def main():
    await asyncio.gather(
        scan_loop(),
        monitor_trades(),
        app.initialize(),
        app.start(),
        app.bot.initialize()
    )

if __name__ == "__main__":
    asyncio.run(main())
