import numpy as np
from models.gofs.base_gof_test import BaseGOFTest
from models.stat_distributions.stat_distribution import StatisticalDistribution
from scipy.stats import chi2, multivariate_normal

class Normal2DChi2GOFTest(BaseGOFTest):
    """Chi-squared goodness-of-fit test for testing data on 2D Normal distribution."""

    def name(self) -> str:
        return "norm2d_chi2"

    def run(self, data: np.ndarray, dist: StatisticalDistribution, bins: int = 6, alpha: float = 0.05) -> dict:
        """
        Perform a 2D chi-squared goodness-of-fit test for normality.
        Args:
            data: np.ndarray of shape (n, 2)
            dist: is not used here
            bins: number of bins per dimension
            alpha: significance level
        Returns:
            dict with test statistic, p-value, decision and extra info
        """
        if data.ndim != 2 or data.shape[1] != 2:
            raise ValueError("Data must be a 2D array of shape (n, 2)")

        n = len(data)

        # params
        mean = np.mean(data, axis=0)
        cov = np.cov(data, rowvar=False)
        dist = multivariate_normal(mean=mean, cov=cov)

        O, x_edges, y_edges = np.histogram2d(data[:, 0], data[:, 1], bins=bins)

        # freqs
        E = np.zeros_like(O)
        for i in range(bins):
            for j in range(bins):
                x1, x2 = x_edges[i], x_edges[i + 1]
                y1, y2 = y_edges[j], y_edges[j + 1]

                # area probability from cdf
                p = (
                    dist.cdf([x2, y2])
                    - dist.cdf([x1, y2])
                    - dist.cdf([x2, y1])
                    + dist.cdf([x1, y1])
                )
                E[i, j] = n * p

        mask = E > 1e-8
        O_safe = O[mask]
        E_safe = E[mask]

        # chi^2
        chi2_stat = np.sum((O_safe - E_safe) ** 2 / E_safe)
        df = np.sum(mask) - 1 - 3  # 2 means + 1 cov
        chi2_crit = chi2.ppf(1 - alpha, df)
        p_value = 1 - chi2.cdf(chi2_stat, df)

        return {
            "statistic": chi2_stat,
            "p_value": p_value,
            "passed": chi2_stat <= chi2_crit,
            "extra": {
                "df": df,
                "critical_value": chi2_crit,
                "expected_min": float(np.min(E_safe)),
                "expected_max": float(np.max(E_safe)),
            },
        }