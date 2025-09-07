from scipy.stats import kstwobign
import numpy as np
from models.gofs.base_gof_test import BaseGOFTest
from models.stat_distributions.stat_distribution import StatisticalDistribution

class KolmogorovSmirnovGOFTest(BaseGOFTest):
    """Kolmogorov-Smirnov goodness-of-fit test (refined)."""

    def name(self) -> str:
        """
        Returns: "ks"
        """
        return "ks"

    def run(self, data: np.ndarray, dist: StatisticalDistribution, alpha: float = 0.05) -> dict:
        """
        Perform the Kolmogorov-Smirnov goodness-of-fit test.
        Args:
            data: input data array
            dist: fitted StatisticalDistribution object
            alpha: significance level
        Returns:
            dictionary with test results (statistic, p-value, decision, extra info)
        """
        n = len(data)
        sorted_data = np.sort(data)
        params = dist.fit(data)
        dist_obj = dist.get_distribution_object(params)

        cdf_vals = dist_obj.cdf(sorted_data)
        ecdf_vals = np.arange(1, n + 1) / n

        dn_plus = np.max(ecdf_vals - cdf_vals)
        dn_minus = np.max(cdf_vals - (np.arange(0, n) / n))
        dn = max(dn_plus, dn_minus)

        z = np.sqrt(n) * dn
        critical = kstwobign.ppf(1 - alpha)
        p_value = 1 - self._kolmogorov_cdf(z, n)

        return {
            "statistic": dn,
            "p_value": p_value,
            "passed": z <= critical,
            "extra": {
                "z_stat": z,
                "n": n,
                "critical_value": critical
            }
        }

    def _kolmogorov_cdf(self, z: float, N: int, terms: int = 100) -> float:
        """
        Approximate the CDF of the Kolmogorov distribution using a series expansion.
        Args:
            z: normalized KS statistic
            N: sample size
            terms: number of expansion terms
        Returns:
            approximated CDF value in [0, 1]
        """
        if z <= 0 or N <= 0:
            return 0.0

        sqrt_N = np.sqrt(N)
        total_sum = 0.0

        for k in range(1, terms + 1):
            k2 = k ** 2
            k4 = k ** 4
            f1 = k2 - 0.5 * (1 - (-1) ** k)
            f2 = 5 * k2 + 22 - 7.5 * (1 - (-1) ** k)

            exp_term = np.exp(-2 * k2 * z ** 2)

            main_part = 1 \
                - (2 * k2 * z) / (3 * sqrt_N) \
                - (1 / (18 * N)) * ((f1 - 4 * (f1 + 3)) * k2 * z ** 2 + 8 * k4)

            correction = (k * z) / (27 * np.sqrt(N ** 3)) * (
                (f2 / 5) - (4 * (f2 + 45) * k2 * z ** 2) / 15 + 8 * k4
            )

            term = (-1) ** k * exp_term * (main_part + correction)
            total_sum += term

        result = 1 + 2 * total_sum
        return max(0.0, min(1.0, result))