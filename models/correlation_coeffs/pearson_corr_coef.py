from models.correlation_coeffs._sagnificance_test_result import SignificanceTestResult
from .corr_coeff import ICorrelationCoefficient
from scipy import stats
import numpy as np

class PearsonCorrelation(ICorrelationCoefficient):
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        if len(x) != len(y): raise ValueError("x and y must have the same length")
        self.r, _ = stats.pearsonr(x, y)
        self.n = len(x)
        return self.r
    
    def significance_test(self, alpha: float = 0.05) -> SignificanceTestResult:
        """
        t-test for Pearson correlation significance.
        """
        if self.r is None or self.n is None:
            raise ValueError("Call fit() first")
        
        df = self.n - 2
        t_stat = self.r * np.sqrt(df) / np.sqrt(1 - self.r**2 + self.EPSILON)
        
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
        t_crit = stats.t.ppf(1 - alpha / 2, df)
        is_significant = p_value < alpha
        
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
    
    def _interval(self, alpha: float = 0.05) -> tuple[float, float]:
        if self.r is None: raise ValueError("Call fit() first")
        z = 0.5 * np.log((1 + self.r) / (1 - self.r + self.EPSILON))
        se = 1 / np.sqrt(self.n - 3)
        z_crit = stats.norm.ppf(alpha / 2)
        low, high = z - z_crit * se, z + z_crit * se
        low, high = np.tanh([low, high])
        return (float(low), float(high))
    
    def name(self) -> str:
        return "Pearson"