import math

def total_return(equity_curve, starting_cash):
    """Overall percentage gain or loss from start to end."""
    ending_equity = equity_curve[-1]["equity"]
    return (ending_equity - starting_cash) / starting_cash


def max_drawdown(equity_curve):
    """The worst peak-to-trough decline seen anywhere in the equity curve."""
    peak = equity_curve[0]["equity"]
    worst_drawdown = 0.0

    for point in equity_curve:
        equity = point["equity"]
        if equity > peak:
            peak = equity
        drawdown = (equity - peak) / peak
        if drawdown < worst_drawdown:
            worst_drawdown = drawdown

    return worst_drawdown

def trade_stats(trades):
    """Pair up BUY/SELL trades and calculate win rate and average win/loss."""
    profits = []

    for i in range(0, len(trades) - 1, 2):
        buy = trades[i]
        sell = trades[i + 1]
        if buy["action"] != "BUY" or sell["action"] != "SELL":
            continue
        cost = buy["price"] * buy["shares"]
        proceeds = sell["cash"]
        profit = proceeds - cost
        profits.append(profit)

    if not profits:
        return {"trade_count": 0, "win_rate": 0.0, "avg_win": 0.0, "avg_loss": 0.0}

    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]

    return {
        "trade_count": len(profits),
        "win_rate": len(wins) / len(profits),
        "avg_win": sum(wins) / len(wins) if wins else 0.0,
        "avg_loss": sum(losses) / len(losses) if losses else 0.0,
    }

def sharpe_ratio(equity_curve):
    """Risk-adjusted return: average bar-to-bar return divided by its volatility."""
    equities = [point["equity"] for point in equity_curve]

    returns = []
    for i in range(1, len(equities)):
        prev = equities[i - 1]
        curr = equities[i]
        returns.append((curr - prev) / prev)

    avg_return = sum(returns) / len(returns)

    variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return 0.0

    return avg_return / std_dev