class Portfolio:
    """Tracks cash, position, and profit/loss as the backtest runs."""

    def __init__(self, starting_cash=10_000):
        self.cash = starting_cash
        self.shares = 0.0
        self.entry_price = None
        self.realized_pnl = 0.0

    def buy(self, price, shares, fee):
        self.cash -= (shares * price) + fee
        self.shares = shares
        self.entry_price = price

    def sell(self, proceeds, fee):
        cost_basis = self.entry_price * self.shares
        self.realized_pnl += (proceeds - fee) - cost_basis
        self.cash = proceeds - fee
        self.shares = 0.0
        self.entry_price = None

    def snapshot(self, current_price):
        """Return a dict describing the portfolio's state right now."""
        if self.shares > 0:
            unrealized_pnl = (current_price - self.entry_price) * self.shares
        else:
            unrealized_pnl = 0.0

        equity = self.cash + self.shares * current_price

        return {
            "cash": self.cash,
            "shares": self.shares,
            "entry_price": self.entry_price,
            "current_price": current_price,
            "equity": equity,
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": unrealized_pnl,
        }