import pandas as pd
from backtest.benchmark import run_buy_and_hold


def make_simple_df():
    return pd.DataFrame({
        "timestamp": [str(i) for i in range(5)],
        "open":  [10, 11, 12, 13, 14],
        "high":  [10, 11, 12, 13, 14],
        "low":   [10, 11, 12, 13, 14],
        "close": [10, 11, 12, 13, 14],
    })


def test_buy_and_hold_buys_once_at_first_price():
    df = make_simple_df()
    equity_curve = run_buy_and_hold(df, starting_cash=1000)

    first_snap = equity_curve[0]
    assert first_snap["entry_price"] == 10
    assert first_snap["cash"] == 0.0


def test_buy_and_hold_equity_rises_with_price():
    df = make_simple_df()
    equity_curve = run_buy_and_hold(df, starting_cash=1000)

    assert equity_curve[-1]["equity"] > equity_curve[0]["equity"]