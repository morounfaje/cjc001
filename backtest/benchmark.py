from portfolio.portfolio import Portfolio

def run_buy_and_hold(df, starting_cash=10_000, fee_rate=0.0, slippage=0.0):
    """Buy once at the first available price, hold to the end. No further trades."""
    portfolio = Portfolio(starting_cash)
    equity_curve = []

    first_price = df.iloc[0]["open"] * (1 + slippage)
    fee = portfolio.cash * fee_rate
    shares = (portfolio.cash - fee) / first_price
    portfolio.buy(first_price, shares, fee)

    for i, row in df.iterrows():
        snap = portfolio.snapshot(row["close"])
        snap["row"] = i
        equity_curve.append(snap)

    return equity_curve