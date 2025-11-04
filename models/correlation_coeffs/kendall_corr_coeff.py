from .corr_coeff import ICorrelationCoefficient
from scipy import stats
import numpy as np

class KendallCorrelation(ICorrelationCoefficient):
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        self.r, _ = stats.kendalltau(x, y)
        self.n = len(x)
        return self.r
    
    def interval(self, confidence: float = 0.95) -> tuple[float, float]:
        if self.r is None: raise ValueError("Call fit() first")
        EPSILON = 1e-11
        var = 2 * (2 * self.n + 5) / (9 * self.n * (self.n - 1 + EPSILON))
        se = np.sqrt(var)
        z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
        return (self.r - z_crit * se, self.r + z_crit * se)
    
    def name(self) -> str:
        return "Kendall"
