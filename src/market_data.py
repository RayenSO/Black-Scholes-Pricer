import yfinance as yf
import pandas as pd

def search_ticker(query: str, max_results: int = 5) -> list:
    """
    Recherche un ticker en fonction d'un nom d'entreprise.
    
    :param query: Nom de l'entreprise ou de l'actif recherché.
    :param max_results: Nombre maximum de résultats à afficher.
    :return: Liste de tuples (ticker, nom complet).
    """
    try:
        # Alternative à `search()` : utilisation de `Ticker` pour récupérer le nom et valider l'existence
        stock = yf.Ticker(query)
        info = stock.info
        
        # Vérifier si l'actif a bien des informations valides
        if "shortName" in info and "symbol" in info:
            return [(info["symbol"], info["shortName"])]
        else:
            return []

    except Exception as e:
        print(f"Erreur lors de la recherche du ticker : {e}")
        return []


def get_last_price(ticker: str) -> float:
    """
    Récupère le dernier prix disponible pour un ticker donné.
    
    :param ticker: Symbole boursier (ex: 'AAPL' pour Apple).
    :return: Dernier prix connu de l'actif.
    """
    try:
        stock = yf.Ticker(ticker)
        last_price = stock.history(period="1d")["Close"].iloc[-1]  # Dernier prix de clôture
        return last_price
    
    except Exception as e:
        print(f"Erreur lors de la récupération du prix pour {ticker}: {e}")
        return None
