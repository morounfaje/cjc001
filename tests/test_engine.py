import pandas as pd
from backtest.engine import run_backtest


def make_df_with_one_buy_signal():
    """5 rows. Signal says BUY at row 1. Execution must happen at row 2, not row 1."""
    return pd.DataFrame({
        "timestamp": [str(i) for i in range(5)],
        "open":   [10, 10, 11, 12, 13],
        "high":   [10, 10, 11, 12, 13],
        "low":    [10, 10, 11, 12, 13],
        "close":  [10, 10, 11, 12, 13],
        "signal": ["HOLD", "BUY", "HOLD", "HOLD", "HOLD"],
    })


def test_execution_happens_on_next_bar_not_same_bar():
    df = make_df_with_one_buy_signal()
    trades, equity_curve = run_backtest(df, starting_cash=1000)

    assert len(trades) == 1
    assert trades[0]["row"] == 2        # NOT row 1, where the signal appeared
    assert trades[0]["price"] == 11     # the OPEN price of row 2


def test_no_trade_happens_before_a_signal_exists():
    df = make_df_with_one_buy_signal()
    trades, equity_curve = run_backtest(df, starting_cash=1000)

    for t in trades:
        assert t["row"] >= 2