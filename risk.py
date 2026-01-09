def calculate_targets(entry, pattern, direction):
    height = pattern["height"]

    if direction == "BUY":
        tp = entry + height
        sl = entry - height * 0.5
    else:
        tp = entry - height
        sl = entry + height * 0.5

    return round(tp, 4), round(sl, 4)
