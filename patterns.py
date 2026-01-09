import numpy as np
from scipy.signal import argrelextrema

def detect_falling_wedge(df):
    highs = df['high'].values
    lows = df['low'].values

    high_idx = argrelextrema(highs, np.greater, order=5)[0]
    low_idx = argrelextrema(lows, np.less, order=5)[0]

    if len(high_idx) < 3 or len(low_idx) < 3:
        return None

    high_slope = np.polyfit(high_idx, highs[high_idx], 1)[0]
    low_slope = np.polyfit(low_idx, lows[low_idx], 1)[0]

    if high_slope < 0 and low_slope < 0 and low_slope > high_slope:
        return {
            "type": "Falling Wedge",
            "resistance": max(highs[high_idx]),
            "support": min(lows[low_idx]),
            "height": max(highs[high_idx]) - min(lows[low_idx])
        }
    return None


def detect_sym_triangle(df):
    highs = df['high']
    lows = df['low']

    high_slope = np.polyfit(range(len(highs)), highs, 1)[0]
    low_slope = np.polyfit(range(len(lows)), lows, 1)[0]

    if high_slope < 0 and low_slope > 0:
        return {
            "type": "Symmetrical Triangle",
            "resistance": highs.max(),
            "support": lows.min(),
            "height": highs.max() - lows.min()
        }
    return None
