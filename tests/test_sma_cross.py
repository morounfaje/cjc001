import pandas as pd
from sma_cross import add_smas, add_signals


def make_trending_df(n=60):
    """A simple upward-trending price series, long enough for both SMAs."""
    closes = [100 + i * 0.5 for i in range(n)]
    return pd.DataFrame({
        "timestamp": [str(i) for i in range(n)],
        "open": closes,
        "high": closes,
        "low": closes,
        "close": closes,
    })


def test_smas_are_nan_before_enough_history():
    df = add_smas(make_trending_df(), fast_window=20, slow_window=50)
    assert pd.isna(df.loc[0, "sma_fast"])
    assert pd.isna(df.loc[48, "sma_slow"])


def test_smas_have_values_once_enough_history():
    df = add_smas(make_trending_df(), fast_window=20, slow_window=50)
    assert not pd.isna(df.loc[49, "sma_slow"])


def test_no_lookahead_bias():
    """A signal at row N must not change depending on how much FUTURE data exists."""
    full_df = make_trending_df(n=60)
    full_result = add_signals(add_smas(full_df))

    cutoff = 55
    partial_df = make_trending_df(n=60).iloc[:cutoff]
    partial_result = add_signals(add_smas(partial_df))

    signal_with_future_data = full_result.loc[cutoff - 1, "signal"]
    signal_without_future_data = partial_result.loc[cutoff - 1, "signal"]

    assert signal_with_future_data == signal_without_future_data