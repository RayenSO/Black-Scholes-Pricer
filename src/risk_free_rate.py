import yfinance as yf

def get_risk_free_rate(source: str = "US Treasury 10Y") -> float:
    """
    Récupère le taux sans risque basé sur la source sélectionnée.
    
    :param source: "US Treasury 10Y" pour récupérer automatiquement le taux, sinon "Manual".
    :return: Le taux sans risque en décimal (ex: 0.05 pour 5%).
    """
    if source == "US Treasury 10Y":
        try:
            treasury_10y = yf.Ticker("^TNX")
            risk_free_rate = treasury_10y.history(period="1d")["Close"].iloc[-1] / 100  # Conversion en décimal
            return risk_free_rate
        except Exception as e:
            print(f"Erreur lors de la récupération du taux sans risque : {e}")
            return 0.05  # Valeur par défaut en cas d'erreur (5%)
    return None  # Indique que l'utilisateur doit entrer manuellement son taux
