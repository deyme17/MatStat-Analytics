from .corr_coeff import ICorrelationCoefficient
from models.correlation_coeffs._sagnificance_test_result import SignificanceTestResult
from scipy import stats
import numpy as np
from typing import Tuple

class KendallCorrelation(ICorrelationCoefficient):
    """
    Implements Kendall's Tau correlation coefficient.
    Uses the normal approximation (Z-test) for significance and CI.
    """
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Compute Kendall's Tau correlation coefficient.
        """
        self.r, self.p_value = stats.kendalltau(x, y)
        self.n = len(x)
        return self.r
    
    def significance_test(self, alpha: float = 0.05) -> SignificanceTestResult:
        """
        Performs the Z-test for Kendall's Tau significance (H0: tau=0)
        using the asymptotic normal approximation (provided by scipy in fit).
        """
        if self.r is None or self.n is None:
            raise ValueError("Call fit() first")
        
        _, se = self._get_asymptotic_stats()
        z_stat = self.r / (se + self.EPSILON)
        
        p_value = self.p_value
        is_significant = p_value < alpha
        z_crit = stats.norm.ppf(1 - alpha / 2)

        return SignificanceTestResult(
            r=self.r,
            statistic=z_stat,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            test_name=self.name(),
            critical_value=z_crit,
            CI=self._interval(alpha) \
                    if is_significant \
                    else None
        )

    def _get_asymptotic_stats(self):
        """Helper to compute the variance and SE for Kendall's Tau asymptotic test."""
        if self.n is None or self.n < 3:
            raise ValueError("Sample size too small for asymptotic variance calculation")
        var = 2 * (2 * self.n + 5) / (9 * self.n * (self.n - 1 + self.EPSILON))
        se = np.sqrt(var)
        return var, se

    def _interval(self, alpha: float = 0.05) -> Tuple[float, float]:
        """
        Compute the confidence interval using the asymptotic normal approximation.
        """
        if self.r is None or self.n is None: 
            raise ValueError("Call fit() first")
        _, se = self._get_asymptotic_stats()
        z_crit = stats.norm.ppf(alpha / 2)
        return (self.r - z_crit * se, self.r + z_crit * se)
    
    def name(self) -> str:
        return "Kendall"