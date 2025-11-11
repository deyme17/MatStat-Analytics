from .corr_coeff import ICorrelationCoefficient
from models.correlation_coeffs._sagnificance_test_result import SignificanceTestResult
import numpy as np
from scipy import stats
from typing import Tuple

class CorrelationRatio(ICorrelationCoefficient):
    """
    Implements the Correlation Ratio (eta) for quantitative variables.
    Measures non-linear association by grouping X into bins.
    """
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Compute the Correlation Ratio (eta) for Y given X.
        """
        self.x, self.y = np.asarray(x), np.asarray(y)
        self.n = len(x)
        k = int(np.sqrt(self.n))
        self.groups = np.digitize(self.x, np.percentile(self.x, np.linspace(0, 100, k + 1)[1 : -1]))
        self.r = self._correlation_ratio(self.groups, self.y)
        return self.r

    def significance_test(self, alpha: float = 0.05) -> SignificanceTestResult:
        """
        Performs F-test for significance of correlation ratio.
        H0: eta = 0 (no relationship between X and Y)
        H1: eta != 0 (relationship exists)
        """
        if self.r is None or self.n is None:
            raise ValueError("Call fit() first")

        k = len(np.unique(self.groups))
        
        # F-statistic
        df1 = k - 1         # between groups
        df2 = self.n - k    # within groups
        
        if df2 <= 0:
            raise ValueError(f"Not enough degrees of freedom (df2={df2}). Reduce n_bins.")
        
        eta_squared = self.r ** 2
        
        if eta_squared >= 1.0:
            f_stat = np.inf
            p_value = 0.0
        else:
            f_stat = (eta_squared / df1) / ((1 - eta_squared) / df2)
            p_value = 1 - stats.f.cdf(f_stat, df1, df2)
        
        f_crit = stats.f.ppf(1 - alpha, df1, df2)
        is_significant = p_value < alpha

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
                "df1": df1,
                "df2": df2,
                "eta_squared": eta_squared,
                "n_groups": k
            }
        )

    def _interval(self, alpha: float = 0.05, n_bootstrap: int = 1000) -> Tuple[float, float]:
        """
        Compute confidence interval using bootstrap percentile method.
        Note: No simple analytical CI exists for eta, so bootstrap is appropriate here.
        """
        if self.r is None or self.n is None: 
            raise ValueError("Call fit() first")
            
        boot = np.empty(n_bootstrap)

        for i in range(n_bootstrap):
            idx = np.random.choice(self.n, self.n, replace=True)
            x_boot, y_boot = self.x[idx], self.y[idx]
            
            k = int(np.sqrt(self.n))
            groups_boot = np.digitize(x_boot, np.percentile(x_boot, np.linspace(0, 100, k + 1)[1 : -1]))
            
            boot[i] = self._correlation_ratio(groups_boot, y_boot)

        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        low, high = np.percentile(boot, [lower_percentile, upper_percentile])
        return (float(low), float(high))

    def name(self) -> str:
        return "Correlation Ratio (η)"

    def _correlation_ratio(self, groups: np.ndarray, values: np.ndarray) -> float:
        """
        Calculate correlation ratio eta.
        eta^2 = SS_between / SS_total = 1 - SS_within / SS_total
        """
        y_mean = np.mean(values)
        ss_total = np.sum((values - y_mean) ** 2)
        
        if ss_total == 0:
            return 0.0
        
        unique_groups = np.unique(groups)
        ss_between = 0.0
        
        for group in unique_groups:
            group_mask = groups == group
            group_values = values[group_mask]
            n_i = len(group_values)
            
            if n_i > 0:
                group_mean = np.mean(group_values)
                ss_between += n_i * (group_mean - y_mean) ** 2
        
        eta_squared = ss_between / ss_total
        return np.sqrt(eta_squared)