import pandas as pd

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def trend_filter(df, direction):
    close = df["close"]

    ema50 = ema(close, 50).iloc[-1]
    ema200 = ema(close, 200).iloc[-1]
    rsi_val = rsi(close).iloc[-1]

    if direction == "BUY":
        return ema50 > ema200 and 50 < rsi_val < 70

    if direction == "SELL":
        return ema50 < ema200 and 30 < rsi_val < 50

    return False
