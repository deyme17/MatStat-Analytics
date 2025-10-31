from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats
import pandas as pd

class NormalDistribution(StatisticalDistribution):
    """Normal (Gaussian) distribution."""
    def __init__(self, mu=None, sigma=None):
        """
        Args:
            mu: mean of the distribution
            sigma: standard deviation of the distribution
        """
        super().__init__()
        self.color = 'red'
        self.name = 'Normal'
        self.params = (mu, sigma) if mu is not None and sigma is not None else None

    @property
    def distribution_params(self) -> dict[str, float | None]:
        """
        Returns: 
            {"mu": mean, "sigma": standard deviation}
        """
        return {
            "mu": self.params[0] if self.params else None,
            "sigma": self.params[1] if self.params else None
        }

    def fit(self, data: pd.Series) -> tuple:
        """
        Fit normal distribution to the given data.
        Args:
            data: input data series
        Returns: 
            (mean, standard deviation)
        """
        mean = np.nanmean(data)
        std = np.nanstd(data)
        if std == 0:
            std = 0.01
        self.params = (mean, std)
        return self.params

    def get_mean(self) -> float | None:
        """
        Return the theoretical mean of the fitted distribution.
        Returns: 
            mean value or None if not fitted
        """
        if not self.params:
            return None
        return self.params[0]

    def get_pdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the PDF of the normal distribution.
        Args:
            x: array of evaluation points
            params: (mu, sigma)
        Returns: 
            array of PDF values
        """
        return stats.norm.pdf(x, loc=params[0], scale=params[1])

    def get_distribution_object(self, params: tuple) -> stats.rv_frozen:
        """
        Return a frozen scipy.stats.norm object with given parameters.
        Args:
            params: (mu, sigma)
        Returns: 
            scipy.stats.rv_frozen object
        """
        return stats.norm(loc=params[0], scale=params[1])

    def get_cdf_variance(self, x_vals: np.ndarray, params: tuple, n: int) -> np.ndarray:
        """
        Compute the variance of the CDF estimate at given points.
        Args:
            x_vals: array of evaluation points
            params: (mu, sigma)
            n: sample size
        Returns: 
            array of variances
        """
        m, sigma = params

        coeff = 1 / (sigma * np.sqrt(2 * np.pi))
        z = (x_vals - m) / sigma
        exp_term = np.exp(-0.5 * z**2)

        dF_dm = -coeff * exp_term
        dF_dsigma = -z * coeff / sigma * exp_term

        var_m = sigma**2 / n
        var_sigma = sigma**2 / (2 * n)

        variance = (dF_dm ** 2) * var_m + (dF_dsigma ** 2) * var_sigma
        return variance

    def get_inverse_cdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the inverse CDF (quantile function) of the normal distribution.
        Args:
            x: array of probabilities in [0, 1]
            params: (mu, sigma)
        Returns: 
            array of quantiles
        """
        x = np.clip(x, 1e-10, 1 - 1e-10)
        loc = params[0]
        scale = params[1]
        return stats.norm.ppf(x, loc=loc, scale=scale)

    def validate_params(self) -> bool:
        """Validate normal distribution parameters."""
        if not self.params or len(self.params) != 2:
            return False
        mu, sigma = self.params
        return (sigma > 0 and 
                np.isfinite(mu) and np.isfinite(sigma) and
                sigma < 1e6 and abs(mu) < 1e6)