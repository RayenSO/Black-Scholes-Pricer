from src.market_data import search_ticker, get_last_price

def test_search_ticker():
    """Test de la recherche de tickers."""
    results = search_ticker("Apple")
    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], list) and len(results[0]) == 2  # Doit contenir (ticker, nom)

def test_get_last_price():
    """Test de récupération du prix."""
    price = get_last_price("AAPL")
    assert isinstance(price, float)
    assert price > 0  # Un prix d'action doit être positif
