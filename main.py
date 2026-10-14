import pandas as pd
from data.loader import validate, file_version
from strategy.sma_cross import add_smas, add_signals
from backtest.engine import run_backtest
from backtest.benchmark import run_buy_and_hold
from metrics.performance import total_return, max_drawdown, trade_stats, sharpe_ratio

DATA_PATH = "data/r100_1m.csv"
STARTING_CASH = 10_000
FEE_RATE = 0.001
SLIPPAGE = 0.0005


def main():
    raw = pd.read_csv(DATA_PATH)
    df = validate(raw)
    version = file_version(DATA_PATH)

    df = add_signals(add_smas(df))

    trades, equity_curve = run_backtest(
        df, starting_cash=STARTING_CASH, fee_rate=FEE_RATE, slippage=SLIPPAGE
    )
    benchmark_curve = run_buy_and_hold(
        df, starting_cash=STARTING_CASH, fee_rate=FEE_RATE, slippage=SLIPPAGE
    )

    pd.DataFrame(trades).to_csv("reports/trade_ledger.csv", index=False)
    pd.DataFrame(equity_curve).to_csv("reports/equity_curve.csv", index=False)
    pd.DataFrame(benchmark_curve).to_csv("reports/benchmark_curve.csv", index=False)

    print(f"Dataset version: {version}")
    print(f"Strategy  return: {total_return(equity_curve, STARTING_CASH) * 100:.2f}%  "
          f"drawdown: {max_drawdown(equity_curve) * 100:.2f}%  "
          f"sharpe: {sharpe_ratio(equity_curve):.3f}")
    print(f"Benchmark return: {total_return(benchmark_curve, STARTING_CASH) * 100:.2f}%  "
          f"drawdown: {max_drawdown(benchmark_curve) * 100:.2f}%")
    print(f"Trade stats: {trade_stats(trades)}")
    print("Saved: reports/trade_ledger.csv, reports/equity_curve.csv, reports/benchmark_curve.csv")


if __name__ == "__main__":
    main()