from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class NormalDistribution(StatisticalDistribution):
    """Normal (Gaussian) distribution."""

    def __init__(self, mu=None, sigma=None):
        super().__init__()
        self.color = 'red'
        self.name = 'Normal'
        self.params = (mu, sigma) if mu is not None and sigma is not None else None

    @property
    def distribution_params(self):
        return {
            "mu": self.params[0] if self.params else None,
            "sigma": self.params[1] if self.params else None
        }

    def fit(self, data):
        mean = np.nanmean(data)
        std = np.nanstd(data)
        if std == 0:
            std = 0.01
        self.params = (mean, std)
        return self.params

    def get_mean(self):
        if not self.params:
            return None
        return self.params[0]

    def get_pdf(self, x, params):
        return stats.norm.pdf(x, loc=params[0], scale=params[1])

    def get_distribution_object(self, params):
        return stats.norm(loc=params[0], scale=params[1])

    def get_cdf_variance(self, x_vals, params, n):
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

    def get_inverse_cdf(self, x, params):
        x = np.clip(x, 1e-10, 1 - 1e-10)
        loc = params[0]
        scale = params[1]
        return stats.norm.ppf(x, loc=loc, scale=scale)
