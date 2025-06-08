from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats
import pandas as pd

class LaplaceDistribution(StatisticalDistribution):
    """Laplace distribution."""

    def __init__(self, mu=None, b=None):
        """
        :param mu: location parameter
        :param b: scale parameter
        """
        super().__init__()
        self.color = 'pink'
        self.name = 'Laplace'
        self.params = (mu, b) if mu is not None and b is not None else None

    @property
    def distribution_params(self) -> dict[str, float | None]:
        """
        :return: {"mu": location, "b": scale}
        """
        return {
            "mu": self.params[0] if self.params else None,
            "b": self.params[1] if self.params else None
        }

    def fit(self, data: pd.Series) -> tuple:
        """
        Fit Laplace distribution to the given data.

        :param data: input data series
        :return: (mu, b)
        """
        try:
            shift, scale = stats.laplace.fit(data)
            scale = max(0.01, scale)
            self.params = (shift, scale)
        except:
            shift = np.nanmean(data)
            scale = np.nanstd(data)
            if scale == 0:
                scale = 0.01
            self.params = (shift, scale)
        return self.params

    def get_mean(self) -> float | None:
        """
        Return the theoretical mean of the fitted distribution.

        :return: mean value or None
        """
        if not self.params:
            return None
        return self.params[0]

    def get_pdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the PDF of the Laplace distribution.

        :param x: array of evaluation points
        :param params: (mu, b)
        :return: array of PDF values
        """
        return stats.laplace.pdf(x, loc=params[0], scale=params[1])

    def get_distribution_object(self, params: tuple):
        """
        Return a frozen scipy.stats.laplace object with given parameters.

        :param params: (mu, b)
        :return: scipy.stats.rv_frozen object
        """
        return stats.laplace(loc=params[0], scale=params[1])

    def get_cdf_variance(self, x_vals: np.ndarray, params: tuple, n: int) -> np.ndarray:
        """
        Compute the variance of the CDF estimate at given points.

        :param x_vals: array of evaluation points
        :param params: (mu, b)
        :param n: sample size
        :return: array of variances
        """
        mu, lam = params

        var_mu = (lam ** 2) / n
        var_lambda = (lam ** 2) / n

        # handle overflow
        exp_pos = np.exp(np.clip(lam * (x_vals - mu), a_min=None, a_max=700))
        exp_neg = np.exp(np.clip(-lam * (x_vals - mu), a_min=None, a_max=700))

        dF_dlambda = np.where(
            x_vals <= mu,
            0.5 * (x_vals - mu) * exp_pos,
            0.5 * (x_vals - mu) * exp_neg
        )

        dF_dmu = np.where(
            x_vals <= mu,
            -0.5 * lam * exp_pos,
            -0.5 * lam * exp_neg
)
        variance = (dF_dlambda ** 2) * var_lambda + (dF_dmu ** 2) * var_mu
        return variance

    def get_inverse_cdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the inverse CDF (quantile function) of the Laplace distribution.

        :param x: array of probabilities in [0, 1]
        :param params: (mu, b)
        :return: array of quantiles
        """
        loc = params[0]
        scale = params[1]
        return stats.laplace.ppf(x, loc=loc, scale=scale)
