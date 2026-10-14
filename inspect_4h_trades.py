import pandas as pd
from data.resample import resample
from strategy.sma_cross import add_smas, add_signals
from backtest.engine import run_backtest

raw = pd.read_csv("data/r100_1m.csv")
df_4h = resample(raw, "4h")
df_4h = add_signals(add_smas(df_4h))

trades, equity_curve = run_backtest(df_4h, fee_rate=0.001, slippage=0.0005)

print(f"Total trades recorded: {len(trades)}\n")

profits = []
for i in range(0, len(trades) - 1, 2):
    buy = trades[i]
    sell = trades[i + 1]
    if buy["action"] != "BUY" or sell["action"] != "SELL":
        continue
    cost = buy["price"] * buy["shares"]
    proceeds = sell["cash"]
    profit = proceeds - cost
    profit_pct = (profit / cost) * 100
    profits.append(profit)
    print(f"Trade {len(profits):2d}: buy row {buy['row']:4d} @ {buy['price']:7.2f}  "
          f"-> sell row {sell['row']:4d} @ {sell['price']:7.2f}   "
          f"profit: {profit:9.2f}  ({profit_pct:+6.2f}%)")

total_profit = sum(profits)
print(f"\nTotal profit from closed trades: {total_profit:.2f}")
print(f"Biggest single win:  {max(profits):.2f}")
print(f"Biggest single loss: {min(profits):.2f}")

sorted_profits = sorted(profits, reverse=True)
top_3_sum = sum(sorted_profits[:3])
print(f"\nSum of top 3 winning trades: {top_3_sum:.2f}")
print(f"That's {top_3_sum / total_profit * 100:.1f}% of total profit" if total_profit != 0 else "")