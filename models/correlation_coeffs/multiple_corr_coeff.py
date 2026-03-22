from models.correlation_coeffs._significance_test_result import SignificanceTestResult
from typing import List
from .corr_coeff import ICorrelationCoefficient
from scipy import stats
import numpy as np


class MultipleCorrelation(ICorrelationCoefficient):
    """
    Implements Multiple correlation coefficient (R) for one dependent variable and multiple independent variables.
    Uses the F-test for significance and confidence intervals based on Fisher's z-transform.
    """
    def fit(self, y: np.ndarray, predictors: List[np.ndarray]) -> float:
        if any(len(p) != len(y) for p in predictors):
            raise ValueError("All arrays must have the same length")
        self.n = len(y)
        self.k = len(predictors)
        self.r = self._calc_multiple_correlation(y, predictors)
        return self.r

    def _calc_multiple_correlation(self, y: np.ndarray, predictors: List[np.ndarray]) -> float:
        X = np.column_stack([np.ones(self.n)] + predictors)
        y_hat = X @ np.linalg.lstsq(X, y, rcond=None)[0]
        r, _ = stats.pearsonr(y, y_hat)
        return abs(r)

    def significance_test(self, alpha: float = 0.05) -> SignificanceTestResult:
        """
        Test the significance of the multiple correlation.
        """
        if self.r is None or self.n is None:
            raise ValueError("Call fit() first")

        df1 = self.k
        df2 = self.n - self.k - 1

        r2 = self.r ** 2
        f_stat = (r2 / df1) / ((1 - r2) / df2)
        p_value = stats.f.sf(f_stat, df1, df2)
        f_crit = stats.f.ppf(1 - alpha, df1, df2)
        is_significant = f_stat > f_crit

        return SignificanceTestResult(
            r=self.r,
            statistic=f_stat,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            test_name=self.name(),
            critical_value=f_crit,
            CI=self._interval(alpha) if is_significant else None,
            extra={
                'df1': df1,
                'df2': df2,
                'R2': round(r2, 4),
            }
        )

    def _interval(self, alpha: float = 0.05) -> tuple[float, float]:
        # fisher z
        z = np.arctanh(self.r)
        se = 1 / np.sqrt(self.n - self.k - 2)
        z_crit = stats.norm.ppf(1 - alpha / 2)
        low = np.tanh(z - z_crit * se)
        high = np.tanh(z + z_crit * se)
        return (float(low), float(high))

    def name(self) -> str:
        return "Multiple"