from .corr_coeff import ICorrelationCoefficient
from scipy import stats
import numpy as np

class PearsonCorrelation(ICorrelationCoefficient):
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        self.r, _ = stats.pearsonr(x, y)
        self.n = len(x)
        return self.r
    
    def interval(self, confidence: float = 0.95) -> tuple[float, float]:
        if self.r is None: raise ValueError("Call fit() first")
        z = 0.5 * np.log((1 + self.r) / (1 - self.r))
        se = 1 / np.sqrt(self.n - 3)
        z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
        low, high = z - z_crit * se, z + z_crit * se
        return np.tanh([low, high])
    
    def name(self) -> str:
        return "Pearson"