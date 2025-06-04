from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats
from scipy.special import gamma
import pandas as pd

class WeibullDistribution(StatisticalDistribution):
    """Weibull distribution."""

    def __init__(self, shape=None, scale=None):
        """
        :param shape: shape parameter (β)
        :param scale: scale parameter (α)
        """
        super().__init__()
        self.color = 'orange'
        self.name = 'Weibull'
        self.params = (shape, scale) if shape is not None and scale is not None else None

    @property
    def distribution_params(self) -> dict[str, float | None]:
        """
        :return: {"shape": β, "scale": α}
        """
        return {
            "shape": self.params[0] if self.params else None,
            "scale": self.params[1] if self.params else None
        }

    def fit(self, data: pd.Series) -> tuple:
        """
        Fit Weibull distribution to the given data.

        :param data: input data series
        :return: (shape, scale)
        """
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01

        try:
            shape, _, scale = stats.weibull_min.fit(data, floc=0)
            shape = max(0.1, shape)
            scale = max(0.1, scale)
            self.params = (shape, scale)
        except:
            mean = np.nanmean(data)
            std = np.nanstd(data)
            if std == 0:
                std = 0.01
            shape = 1.5
            scale = mean / 0.9
            self.params = (shape, scale)
        return self.params

    def get_mean(self) -> float | None:
        """
        Return the theoretical mean of the fitted distribution.

        :return: mean value or None
        """
        if not self.params:
            return None
        shape, scale = self.params
        return scale * gamma(1 + 1 / shape)

    def get_pdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the PDF of the Weibull distribution.

        :param x: array of evaluation points
        :param params: (shape, scale)
        :return: array of PDF values
        """
        shape = max(0.1, params[0])
        scale = max(0.1, params[1])
        return stats.weibull_min.pdf(x, c=shape, loc=0, scale=scale)

    def get_distribution_object(self, params: tuple):
        """
        Return a frozen scipy.stats.weibull_min object with given parameters.

        :param params: (shape, scale)
        :return: scipy.stats.rv_frozen object
        """
        return stats.weibull_min(c=params[0], scale=params[1])

    def get_cdf_variance(self, x_vals: np.ndarray, params: tuple, n: int) -> np.ndarray:
        """
        Compute the variance of the CDF estimate at given points.

        :param x_vals: array of evaluation points
        :param params: (α, β)
        :param n: sample size
        :return: array of variances
        """
        alpha, beta = params
        x_safe = np.clip(x_vals, 1e-10, 1e10)

        # the limitation for safety
        safe_power = np.clip(x_safe ** beta, 0, 1e300)
        expo = np.clip(safe_power / alpha, 0, 700)

        dF_dalpha = -safe_power / (alpha ** 2) * np.exp(-expo)
        dF_dbeta = safe_power * np.log(x_safe) / alpha * np.exp(-expo)

        var_alpha = alpha ** 2 / n
        var_beta = beta ** 2 / n

        variance = (dF_dalpha ** 2) * var_alpha + (dF_dbeta ** 2) * var_beta
        return np.nan_to_num(variance, nan=0.0, posinf=0.0, neginf=0.0)

    def get_inverse_cdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the inverse CDF (quantile function) of the Weibull distribution.

        :param x: array of probabilities in [0, 1]
        :param params: (shape, scale)
        :return: array of quantiles
        """
        shape = max(0.1, params[0])
        scale = max(0.1, params[1])
        return scale * (-np.log(1 - x))**(1 / shape)