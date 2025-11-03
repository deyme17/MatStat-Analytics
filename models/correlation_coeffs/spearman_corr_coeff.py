from .corr_coeff import ICorrelationCoefficient
from scipy import stats
import numpy as np

class SpearmanCorrelation(ICorrelationCoefficient):
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        self.r, _ = stats.spearmanr(x, y)
        self.x, self.y = np.asarray(x), np.asarray(y)
        return self.r
    
    def interval(self, confidence: float = 0.95, n_bootstrap: int = 1000) -> tuple[float, float]:
        if self.r is None: raise ValueError("Call fit() first")
        n = len(self.x)
        boot = np.empty(n_bootstrap)

        for i in range(n_bootstrap):
            idx = np.random.randint(0, n, n)
            x_r, y_r = self.x[idx], self.y[idx]
            r, _ = stats.spearmanr(x_r, y_r)
            boot[i] = r

        low, high = np.percentile(boot, [(1 - confidence) / 2 * 100,
                                      (1 + confidence) / 2 * 100])
        return low, high
    
    def name(self) -> str:
        return "Spearman"