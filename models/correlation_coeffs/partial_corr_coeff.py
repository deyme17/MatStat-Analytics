from models.correlation_coeffs._significance_test_result import SignificanceTestResult
from typing import List
from .corr_coeff import ICorrelationCoefficient
from scipy import stats
import numpy as np


class PartialCorrelation(ICorrelationCoefficient):
    """
    Implements Partial correlation coefficient (r) for two variables controlling for multiple control variables.
    Uses the t-test for significance and confidence intervals based on Fisher's z-transform.
    """
    def fit(self, x: np.ndarray, y: np.ndarray, controls: List[np.ndarray]) -> float:
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        self.controls = controls
        self.r, _ = self._calc_partial_correlation(x, y, controls)
        self.n = len(x)
        return self.r

    def _calc_partial_correlation(self, x: np.ndarray, y: np.ndarray, controls: List[np.ndarray]) -> tuple[float, float]:
        X = np.column_stack(controls)
        beta_x = np.linalg.lstsq(X, x, rcond=None)[0]
        beta_y = np.linalg.lstsq(X, y, rcond=None)[0]
        res_x = x - X @ beta_x
        res_y = y - X @ beta_y
        r, p_value = stats.pearsonr(res_x, res_y)
        return r, p_value
    
    def significance_test(self, alpha: float = 0.05) -> SignificanceTestResult:
        """
        Test the significance of the partial correlation.
        """
        if self.r is None or self.n is None:
            raise ValueError("Call fit() first")

        k = len(self.controls)
        df = self.n - k - 2

        t_stat = self.r * np.sqrt(df) / np.sqrt(1 - self.r ** 2)
        p_value = 2 * stats.t.sf(np.abs(t_stat), df=df)
        t_crit = stats.t.ppf(1 - alpha / 2, df=df)
        is_significant = abs(t_stat) > t_crit

        return SignificanceTestResult(
            r=self.r,
            statistic=t_stat,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            test_name=self.name(),
            critical_value=t_crit,
            CI=self._interval(alpha) if is_significant else None,
            extra={
                'df': df,
                'controls_count': k,
            }
        )
    
    def _interval(self, alpha: float = 0.05) -> tuple[float, float]:
        k = len(self.controls)
        df = self.n - k - 2
        # fisher z-transform
        z = np.arctanh(self.r)
        se = 1 / np.sqrt(df - 1)
        z_crit = stats.norm.ppf(1 - alpha / 2)
        low = np.tanh(z - z_crit * se)
        high = np.tanh(z + z_crit * se)
        return (float(low), float(high))
    
    def name(self) -> str:
        return "Partial"