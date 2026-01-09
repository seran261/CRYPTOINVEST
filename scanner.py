import ccxt.async_support as ccxt
import pandas as pd
from patterns import detect_falling_wedge, detect_sym_triangle
from indicators import trend_filter
from retest import confirm_retest
from confidence import confidence_score
from risk import calculate_targets

exchange = ccxt.binance({
    "enableRateLimit": True,
    "options": {"defaultType": "spot"}
})

async def fetch_top_symbols(limit=200):
    markets = await exchange.load_markets()
    usdt_pairs = [
        s for s in markets
        if s.endswith("/USDT") and markets[s]["active"]
    ]
    return usdt_pairs[:limit]


async def scan_symbol(symbol, timeframe):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=200)
        df = pd.DataFrame(
            ohlcv,
            columns=["ts","open","high","low","close","volume"]
        )

        pattern = detect_falling_wedge(df) or detect_sym_triangle(df)
        if not pattern:
            return None

        last = df.iloc[-1]
        volume_ok = last["volume"] > df["volume"].mean() * 1.5

        direction = "BUY"
        breakout = last["close"] > pattern["resistance"]
        if not breakout:
            return None

        trend_ok = trend_filter(df, direction)
        retest_ok = confirm_retest(df, pattern["resistance"], direction)

        score = confidence_score(
            pattern=True,
            ema_trend=trend_ok,
            rsi_ok=trend_ok,
            volume=volume_ok,
            retest=retest_ok
        )

        if score < 70:
            return None

        tp, sl = calculate_targets(last["close"], pattern, direction)

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "pattern": pattern["type"],
            "entry": last["close"],
            "tp": tp,
            "sl": sl,
            "confidence": score
        }

    except Exception:
        return None
