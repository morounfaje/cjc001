def add_smas(df, fast_window=20, slow_window=50):
    """Add two moving-average columns to the price table."""
    df = df.copy()
    df["sma_fast"] = df["close"].rolling(window=fast_window).mean()
    df["sma_slow"] = df["close"].rolling(window=slow_window).mean()
    return df

def add_signals(df):
    """Add a 'signal' column: BUY, SELL, or HOLD, based on SMA crossovers."""
    df = df.copy()

    fast = df["sma_fast"]
    slow = df["sma_slow"]
    fast_prev = fast.shift(1)
    slow_prev = slow.shift(1)

    crossed_up = (fast_prev <= slow_prev) & (fast > slow)
    crossed_down = (fast_prev >= slow_prev) & (fast < slow)

    df["signal"] = "HOLD"
    df.loc[crossed_up, "signal"] = "BUY"
    df.loc[crossed_down, "signal"] = "SELL"

    return df