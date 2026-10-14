from portfolio.portfolio import Portfolio

def test_buy_spends_cash_on_shares_not_just_fee():
    """Regression test: buying should spend cash on (shares * price) + fee,
    not just the fee. This is the exact bug we found and fixed earlier."""
    p = Portfolio(starting_cash=1000)
    p.buy(price=10, shares=99, fee=1)  # 99 shares * $10 = $990, + $1 fee = $991 spent
    assert round(p.cash, 2) == 9.0


def test_sell_converts_shares_back_to_cash():
    p = Portfolio(starting_cash=1000)
    p.buy(price=10, shares=100, fee=0)
    p.sell(proceeds=1200, fee=0)
    assert p.cash == 1200
    assert p.shares == 0


def test_realized_pnl_tracks_profit():
    p = Portfolio(starting_cash=1000)
    p.buy(price=10, shares=100, fee=0)
    p.sell(proceeds=1200, fee=0)
    assert p.realized_pnl == 200


def test_snapshot_unrealized_pnl_while_holding():
    p = Portfolio(starting_cash=1000)
    p.buy(price=10, shares=100, fee=0)
    snap = p.snapshot(current_price=12)
    assert snap["unrealized_pnl"] == 200
    assert snap["equity"] == 1200