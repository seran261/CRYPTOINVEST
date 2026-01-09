import ccxt.async_support as ccxt
import asyncio
from storage import load_data
from tracker import close_trade

exchange = ccxt.binance({"enableRateLimit": True})

async def monitor_trades():
    while True:
        data = load_data()
        open_trades = data["open"]

        for trade in open_trades:
            symbol = trade["symbol"]
            ticker = await exchange.fetch_ticker(symbol)
            price = ticker["last"]

            if price >= trade["tp"]:
                close_trade(trade, "WIN")

            elif price <= trade["sl"]:
                close_trade(trade, "LOSS")

        await asyncio.sleep(30)
