import pandas as pd
from data.loader import validate
from data.resample import resample
from strategy.sma_cross import add_smas, add_signals
from strategy.ema_cross import add_emas, add_ema_signals
from backtest.engine import run_backtest
from backtest.benchmark import run_buy_and_hold
from metrics.performance import total_return, max_drawdown, trade_stats


def test_strategy(label, df):
    trades, equity_curve = run_backtest(df, fee_rate=0.001, slippage=0.0005)
    ret = total_return(equity_curve, 10000)
    dd = max_drawdown(equity_curve)
    stats = trade_stats(trades)
    print(f"{label:16s}  return: {ret*100:8.2f}%   drawdown: {dd*100:7.2f}%   "
          f"trades: {stats['trade_count']:5d}   win rate: {stats['win_rate']*100:5.1f}%")


raw = pd.read_csv("data/r100_1m.csv")
df_1m = validate(raw)

timeframes = {
    "1-minute": df_1m,
    "5-minute": resample(raw, "5min"),
    "15-minute": resample(raw, "15min"),
    "1-hour": resample(raw, "1h"),
    "4-hour": resample(raw, "4h"),
}

for name, tf_df in timeframes.items():
    sma_df = add_signals(add_smas(tf_df.copy()))
    test_strategy(f"SMA {name}", sma_df)

    ema_df = add_ema_signals(add_emas(tf_df.copy()))
    test_strategy(f"EMA {name}", ema_df)

    print()

benchmark_curve = run_buy_and_hold(df_1m, fee_rate=0.001, slippage=0.0005)
print(f"Buy&Hold          return: {total_return(benchmark_curve, 10000)*100:8.2f}%   "
      f"drawdown: {max_drawdown(benchmark_curve)*100:7.2f}%")