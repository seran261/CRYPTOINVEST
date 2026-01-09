def confirm_retest(df, breakout_level, direction, lookahead=3):
    recent = df.iloc[-lookahead:]

    for _, row in recent.iterrows():
        if direction == "BUY":
            if row["low"] <= breakout_level and row["close"] > breakout_level:
                return True

        if direction == "SELL":
            if row["high"] >= breakout_level and row["close"] < breakout_level:
                return True

    return False
