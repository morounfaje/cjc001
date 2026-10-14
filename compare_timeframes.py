import pandas as pd
from data.loader import validate
from data.resample import resample
from strategy.sma_cross import add_smas, add_signals
from backtest.engine import run_backtest
from backtest.benchmark import run_buy_and_hold
from metrics.performance import total_return, max_drawdown, trade_stats


def test_timeframe(label, df):
    df = df.copy()
    df = add_signals(add_smas(df))
    trades, equity_curve = run_backtest(df, fee_rate=0.001, slippage=0.0005)
    ret = total_return(equity_curve, 10000)
    dd = max_drawdown(equity_curve)
    stats = trade_stats(trades)
    print(f"{label:10s}  return: {ret*100:8.2f}%   drawdown: {dd*100:7.2f}%   "
          f"trades: {stats['trade_count']:5d}   win rate: {stats['win_rate']*100:5.1f}%")


raw = pd.read_csv("data/r100_1m.csv")
df_1m = validate(raw)

test_timeframe("1-minute", df_1m)
test_timeframe("5-minute", resample(raw, "5min"))
test_timeframe("15-minute", resample(raw, "15min"))
test_timeframe("1-hour", resample(raw, "1h"))
test_timeframe("4-hour", resample(raw, "4h"))

benchmark_curve = run_buy_and_hold(df_1m, fee_rate=0.001, slippage=0.0005)
print(f"Buy&Hold    return: {total_return(benchmark_curve, 10000)*100:8.2f}%   "
      f"drawdown: {max_drawdown(benchmark_curve)*100:7.2f}%")