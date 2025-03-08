import numpy as np
import scipy.stats as si

class BlackScholesPricer:
    """
    Implémentation du modèle Black-Scholes pour le pricing des options européennes.
    Permet de calculer le prix des options Call et Put ainsi que les Greeks.
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        """
        Initialise le pricer avec les paramètres nécessaires.
        
        :param S: Prix actuel de l'actif sous-jacent
        :param K: Prix d'exercice (Strike)
        :param T: Temps jusqu'à l'échéance (en années)
        :param r: Taux d'intérêt sans risque (en décimal)
        :param sigma: Volatilité de l'actif sous-jacent (en décimal)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def d1(self) -> float:
        """Calcule d1 utilisé dans la formule de Black-Scholes."""
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self) -> float:
        """Calcule d2 utilisé dans la formule de Black-Scholes."""
        return self.d1() - self.sigma * np.sqrt(self.T)

    def call_price(self) -> float:
        """Calcule le prix de l'option Call selon Black-Scholes."""
        d1, d2 = self.d1(), self.d2()
        return self.S * si.norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * si.norm.cdf(d2)

    def put_price(self) -> float:
        """Calcule le prix de l'option Put selon Black-Scholes."""
        d1, d2 = self.d1(), self.d2()
        return self.K * np.exp(-self.r * self.T) * si.norm.cdf(-d2) - self.S * si.norm.cdf(-d1)

    def delta(self, option_type: str = "call") -> float:
        """Calcule Delta (sensibilité du prix de l'option au sous-jacent)."""
        d1 = self.d1()
        if option_type == "call":
            return si.norm.cdf(d1)
        elif option_type == "put":
            return si.norm.cdf(d1) - 1
        else:
            raise ValueError("option_type doit être 'call' ou 'put'")

    def gamma(self) -> float:
        """Calcule Gamma (sensibilité de Delta au sous-jacent)."""
        d1 = self.d1()
        return si.norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self) -> float:
        """Calcule Vega (sensibilité du prix de l'option à la volatilité)."""
        d1 = self.d1()
        return self.S * si.norm.pdf(d1) * np.sqrt(self.T)

    def theta(self, option_type: str = "call") -> float:
        """Calcule Theta (perte de valeur temps de l'option)."""
        d1, d2 = self.d1(), self.d2()
        term1 = - (self.S * si.norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
        if option_type == "call":
            return term1 - self.r * self.K * np.exp(-self.r * self.T) * si.norm.cdf(d2)
        elif option_type == "put":
            return term1 + self.r * self.K * np.exp(-self.r * self.T) * si.norm.cdf(-d2)
        else:
            raise ValueError("option_type doit être 'call' ou 'put'")

    def rho(self, option_type: str = "call") -> float:
        """Calcule Rho (sensibilité du prix de l'option au taux d'intérêt)."""
        d2 = self.d2()
        if option_type == "call":
            return self.K * self.T * np.exp(-self.r * self.T) * si.norm.cdf(d2)
        elif option_type == "put":
            return -self.K * self.T * np.exp(-self.r * self.T) * si.norm.cdf(-d2)
        else:
            raise ValueError("option_type doit être 'call' ou 'put'")
