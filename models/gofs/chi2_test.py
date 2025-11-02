from scipy.stats import chi2
import numpy as np
from models.gofs.base_gof_test import BaseGOFTest
from models.stat_distributions.stat_distribution import StatisticalDistribution

class ChiSquaredGOFTest(BaseGOFTest):
    """Chi-squared goodness-of-fit test."""

    def name(self) -> str:
        """
        Returns: "chi2"
        """
        return "chi2"

    def run(self, data: np.ndarray, dist: StatisticalDistribution, bins: int = 10, alpha: float = 0.05) -> dict:
        """
        Perform the chi-squared goodness-of-fit test.
        Args:
            data: input data array
            dist: fitted StatisticalDistribution object
            bins: number of histogram bins
            alpha: significance level
        Returns:
            dictionary with test results (statistic, p-value, decision, extra info)
        """
        if data.ndim != 1:
            raise ValueError("Data must be a 1D array")

        
        hist, bin_edges = np.histogram(data, bins=bins)
        total = len(data)

        params = dist.fit(data)
        dist_obj = dist.get_distribution_object(params)

        cdf_vals = [dist_obj.cdf(edge) for edge in bin_edges]
        probs = np.diff(cdf_vals)
        expected = probs * total

        mask = expected > 1e-8
        hist_safe = hist[mask]
        expected_safe = expected[mask]

        chi2_stat = np.sum((hist_safe - expected_safe) ** 2 / expected_safe)
        df = np.sum(mask) - 1 - len(params)
        chi2_crit = chi2.ppf(1 - alpha, df)
        p_value = 1 - chi2.cdf(chi2_stat, df)

        return {
            "statistic": chi2_stat,
            "p_value": p_value,
            "passed": chi2_stat <= chi2_crit,
            "extra": {
                "df": df,
                "critical_value": chi2_crit,
                "expected_min": float(np.min(expected_safe)),
                "expected_max": float(np.max(expected_safe))
            }
        }
