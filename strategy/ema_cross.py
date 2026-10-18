def add_emas(df, fast_window=20, slow_window=50):
    """Add two exponential-moving-average columns to the price table."""
    df = df.copy()
    df["ema_fast"] = df["close"].ewm(span=fast_window, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=slow_window, adjust=False).mean()
    return df


def add_ema_signals(df):
    """Add a 'signal' column: BUY, SELL, or HOLD, based on EMA crossovers."""
    df = df.copy()

    fast = df["ema_fast"]
    slow = df["ema_slow"]
    fast_prev = fast.shift(1)
    slow_prev = slow.shift(1)

    crossed_up = (fast_prev <= slow_prev) & (fast > slow)
    crossed_down = (fast_prev >= slow_prev) & (fast < slow)

    df["signal"] = "HOLD"
    df.loc[crossed_up, "signal"] = "BUY"
    df.loc[crossed_down, "signal"] = "SELL"

    return df