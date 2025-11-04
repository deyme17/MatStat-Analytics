from .corr_coeff import ICorrelationCoefficient
import numpy as np

class CorrelationRatio(ICorrelationCoefficient):
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        self.r = self._correlation_ratio(x, y)
        self.x, self.y = x, y
        return self.r

    def interval(self, confidence: float = 0.95, n_bootstrap: int = 1000) -> tuple[float, float]:
        if self.r is None: raise ValueError("Call fit() first")
        n = len(self.x)
        boot = []

        for _ in range(n_bootstrap):
            idx = np.random.randint(0, n, n)
            x_r, y_r = self.x[idx], self.y[idx]
            boot.append(self._correlation_ratio(x_r, y_r))

        low, high = np.percentile(boot, [(1 - confidence) / 2 * 100, (1 + confidence) / 2 * 100])
        return (float(low), float(high))

    def name(self) -> str:
        return "Correlation Ratio (η)"

    def _correlation_ratio(self, categories: np.ndarray, values: np.ndarray) -> float:
        cat_levels = np.unique(categories)
        y_mean = np.mean(values)

        ss_between = sum([
            len(values[categories == cat]) * (np.mean(values[categories == cat]) - y_mean) ** 2
            for cat in cat_levels
        ])
        ss_total = np.sum((values - y_mean) ** 2)
        
        return np.sqrt(ss_between / ss_total) if ss_total != 0 else 0