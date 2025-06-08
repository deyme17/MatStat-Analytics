import pandas as pd
import numpy as np
from scipy.stats import norm 


class ConfidenceService:
    """
    Service for computing confidence intervals for cumulative distribution function.
    """

    @staticmethod
    def cdf_variance_ci(data: pd.Series, dist, confidence_level: float = 0.95):
        """
        Compute CDF with variance-based confidence intervals.

        :param data: input data series
        :param dist: StatisticalDistribution instance
        :param confidence_level: confidence level (default: 0.95)
        :return: tuple (x, CDF, lower CI, upper CI) or None if failed
        """
        n = len(data)

        params = dist.fit(data)
        dist_obj = dist.get_distribution_object(params)
        if dist_obj is None:
            return None

        x_vals = np.linspace(data.min(), data.max(), 300)
        cdf_vals = dist_obj.cdf(x_vals)

        z = norm.ppf((1 + confidence_level) / 2)
        variance = dist.get_cdf_variance(x_vals, params, n)
        epsilon = z * np.sqrt(variance)

        ci_lower = np.clip(cdf_vals - epsilon, 0, 1)
        ci_upper = np.clip(cdf_vals + epsilon, 0, 1)

        return x_vals, cdf_vals, ci_lower, ci_upper