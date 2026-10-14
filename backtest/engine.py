from portfolio.portfolio import Portfolio

def run_backtest(df, starting_cash=10_000, fee_rate=0.0, slippage=0.0):
    """Walk through the data bar by bar and simulate trades, including costs.

    A signal from the PREVIOUS row is acted on using the CURRENT row's
    open price. This enforces next-bar execution.
    """
    portfolio = Portfolio(starting_cash)
    trades = []
    equity_curve = []

    prev_signal = "HOLD"

    for i, row in df.iterrows():
        price = row["open"]

        if prev_signal == "BUY" and portfolio.shares == 0:
            buy_price = price * (1 + slippage)
            fee = portfolio.cash * fee_rate
            shares = (portfolio.cash - fee) / buy_price
            portfolio.buy(buy_price, shares, fee)
            trades.append({"row": i, "action": "BUY", "price": buy_price, "shares": shares, "fee": fee})

        elif prev_signal == "SELL" and portfolio.shares > 0:
            sell_price = price * (1 - slippage)
            proceeds = portfolio.shares * sell_price
            fee = proceeds * fee_rate
            portfolio.sell(proceeds, fee)
            trades.append({"row": i, "action": "SELL", "price": sell_price, "cash": portfolio.cash, "fee": fee})

        snap = portfolio.snapshot(row["close"])
        snap["row"] = i
        equity_curve.append(snap)

        prev_signal = row["signal"]

    return trades, equity_curve