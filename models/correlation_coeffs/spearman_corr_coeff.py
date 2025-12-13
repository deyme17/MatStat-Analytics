from models.correlation_coeffs._significance_test_result import SignificanceTestResult
from .corr_coeff import ICorrelationCoefficient
from scipy import stats
import numpy as np
from typing import Tuple

class SpearmanCorrelation(ICorrelationCoefficient):
    """
    Implements Spearman's Rho rank correlation coefficient.
    Uses the asymptotic t-test for significance and bootstrap for CI.
    """
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Compute Spearman's Rho correlation coefficient.
        """
        self.r, self.p_value = stats.spearmanr(x, y)
        self.x, self.y = np.asarray(x), np.asarray(y)
        self.n = len(x)
        return self.r
    
    def significance_test(self, alpha: float = 0.05) -> SignificanceTestResult:
        """
        Performs the t-test for Spearman's Rho significance (H0: rho=0).
        Uses the p-value directly from the fit method (scipy).
        """
        if self.r is None or self.n is None:
            raise ValueError("Call fit() first")
        
        df = self.n - 2
        t_stat = self.r * np.sqrt(df) / np.sqrt(1 - self.r**2 + self.EPSILON)
        
        p_value = self.p_value
        is_significant = p_value < alpha
        t_crit = stats.t.ppf(1 - alpha / 2, df)

        return SignificanceTestResult(
            r=self.r,
            statistic=t_stat,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            test_name=self.name(),
            critical_value=t_crit,
            CI=self._interval(alpha) \
                    if is_significant \
                    else None,
            extra={
                "df": df
            }
        )
    
    def _interval(self, alpha: float = 0.05, n_bootstrap: int = 1000) -> Tuple[float, float]:
        """
        Compute the confidence interval using the Bootstrap method (percentile method).
        """
        if self.r is None or self.n is None: 
            raise ValueError("Call fit() first")
            
        n = self.n
        boot = np.empty(n_bootstrap)

        for i in range(n_bootstrap):
            idx = np.random.randint(0, n, n)
            x_r, y_r = self.x[idx], self.y[idx]
            r, _ = stats.spearmanr(x_r, y_r)
            boot[i] = r

        low_percentile = (1 - alpha) / 2 * 100
        high_percentile = (1 + alpha) / 2 * 100
        
        low, high = np.percentile(boot, [low_percentile, high_percentile])
        return float(low), float(high)
    
    def name(self) -> str:
        return "Spearman"