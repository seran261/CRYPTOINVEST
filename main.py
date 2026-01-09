import asyncio
from scanner_async import fetch_top_symbols, scan_symbol
from signal_sender import send_signal
from tracker import add_trade
from price_watcher import monitor_trades
from telegram_utils import build_app
from config import TIMEFRAMES, TOP_COINS_LIMIT

SCAN_INTERVAL = 3600


# ---------- BACKGROUND ASYNC TASKS ----------

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


async def async_tasks():
    await asyncio.gather(
        scan_loop(),
        monitor_trades()
    )


# ---------- TELEGRAM POST-INIT HOOK ----------

async def post_init(app):
    app.create_task(async_tasks())


# ---------- MAIN ENTRY ----------

def main():
    app = build_app()

    # ✅ THIS IS THE FIX
    app.post_init = post_init

    # ✅ Starts event loop safely
    app.run_polling()


if __name__ == "__main__":
    main()
