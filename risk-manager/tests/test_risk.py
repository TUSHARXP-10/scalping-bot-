from main import fetch_open_trades, compute_drawdown

def test_fetch_trades_returns_list():
    trades = fetch_open_trades()
    assert isinstance(trades, list)

def test_drawdown_returns_number():
    drawdown = compute_drawdown()
    assert isinstance(drawdown, (int, float))