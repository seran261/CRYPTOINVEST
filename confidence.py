def confidence_score(
    pattern=True,
    ema_trend=False,
    rsi_ok=False,
    volume=False,
    retest=False
):
    score = 0

    if pattern: score += 30
    if ema_trend: score += 20
    if rsi_ok: score += 15
    if volume: score += 15
    if retest: score += 20

    return score
