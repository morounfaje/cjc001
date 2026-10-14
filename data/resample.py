import pandas as pd


def resample(df, rule):
    """Compress 1-minute candles into larger bars (e.g. '5min', '15min')."""
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    out = df.resample(rule).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
    })

    out = out.dropna()
    out = out.reset_index()
    return out