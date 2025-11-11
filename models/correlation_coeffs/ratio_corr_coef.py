from .corr_coeff import ICorrelationCoefficient
from models.correlation_coeffs._sagnificance_test_result import SignificanceTestResult
import numpy as np
from typing import Tuple

class CorrelationRatio(ICorrelationCoefficient):
    """
    Implements the Correlation Ratio (eta, η), a measure of association
    between a categorical variable (x) and a quantitative variable (y).
    Uses bootstrap for both significance testing and confidence interval.
    """
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Compute the Correlation Ratio (η).
        """
        self.x, self.y = np.asarray(x), np.asarray(y)
        self.n = len(x)
        self.r = self._correlation_ratio(self.x, self.y)
        return self.r

    def significance_test(self, alpha: float = 0.05, n_bootstrap: int = 1000) -> SignificanceTestResult:
        """
        Performs a non-parametric bootstrap test for significance (H0: η=0).
        This tests if the observed η is significantly greater than what is expected by chance.
        Uses permutation/bootstrap method to estimate the null distribution.
        """
        if self.r is None or self.n is None:
            raise ValueError("Call fit() first")

        null_distribution = np.empty(n_bootstrap)
        
        for i in range(n_bootstrap):
            permuted_y = np.random.permutation(self.y)
            null_distribution[i] = self._correlation_ratio(self.x, permuted_y)

        p_value = np.sum(null_distribution >= self.r) / n_bootstrap
        is_significant = p_value < alpha
        critical_value = np.percentile(null_distribution, (1 - alpha) * 100)

        return SignificanceTestResult(
            r=self.r,
            statistic=self.r,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            test_name=self.name() + " (Bootstrap)",
            critical_value=critical_value,
            CI=self._interval(alpha) \
                    if is_significant \
                    else None
        )

    def _interval(self, alpha: float = 0.05, n_bootstrap: int = 1000) -> Tuple[float, float]:
        """
        Compute the confidence interval using the Bootstrap percentile method.
        """
        if self.r is None or self.n is None: 
            raise ValueError("Call fit() first")
            
        n = self.n
        boot = []

        for _ in range(n_bootstrap):
            idx = np.random.randint(0, n, n)
            x_r, y_r = self.x[idx], self.y[idx]
            boot.append(self._correlation_ratio(x_r, y_r))

        low_percentile = (1 - alpha) / 2 * 100
        high_percentile = (1 + alpha) / 2 * 100
        
        low, high = np.percentile(boot, [low_percentile, high_percentile])
        return (float(low), float(high))

    def name(self) -> str:
        return "Correlation Ratio (η)"

    def _correlation_ratio(self, categories: np.ndarray, values: np.ndarray) -> float:
        """Helper to compute the correlation ratio η."""
        cat_levels = np.unique(categories)
        y_mean = np.mean(values)

        ss_between = sum([
            len(values[categories == cat]) * (np.mean(values[categories == cat]) - y_mean) ** 2
            for cat in cat_levels
        ])
        ss_total = np.sum((values - y_mean) ** 2)
        
        return np.sqrt(ss_between / ss_total) if ss_total != 0 else 0