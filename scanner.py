import ccxt
import pandas as pd
from patterns import detect_falling_wedge, detect_sym_triangle
from risk import calculate_targets

exchange = ccxt.binance()

def fetch_top_symbols(limit=200):
    markets = exchange.load_markets()
    usdt_pairs = [s for s in markets if s.endswith("/USDT")]
    return usdt_pairs[:limit]


def scan_symbol(symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=120)
    df = pd.DataFrame(ohlcv, columns=["ts","open","high","low","close","volume"])

    pattern = (
        detect_falling_wedge(df) or
        detect_sym_triangle(df)
    )

    if not pattern:
        return None

    last_close = df.iloc[-1]['close']
    volume_ok = df.iloc[-1]['volume'] > df['volume'].mean() * 1.5

    if last_close > pattern["resistance"] and volume_ok:
        tp, sl = calculate_targets(last_close, pattern, "BUY")
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "pattern": pattern["type"],
            "entry": last_close,
            "tp": tp,
            "sl": sl
        }
    return None
