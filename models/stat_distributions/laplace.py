from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class LaplaceDistribution(StatisticalDistribution):
    """Laplace distribution."""

    def __init__(self, mu=None, b=None):
        super().__init__()
        self.color = 'pink'
        self.name = 'Laplace'
        self.params = (mu, b) if mu is not None and b is not None else None

    @property
    def distribution_params(self):
        return {
            "mu": self.params[0] if self.params else None,
            "b": self.params[1] if self.params else None
        }

    def fit(self, data):
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

    def get_mean(self):
        if not self.params:
            return None
        return self.params[0]

    def get_pdf(self, x, params):
        return stats.laplace.pdf(x, loc=params[0], scale=params[1])

    def get_distribution_object(self, params):
        return stats.laplace(loc=params[0], scale=params[1])

    def get_cdf_variance(self, x_vals, params, n):
        mu, lam = params

        var_mu = (lam**2) / n
        var_lambda = (lam**2) / n

        dF_dlambda = np.where(
            x_vals <= mu,
            0.5 * (x_vals - mu) * np.exp(lam * (x_vals - mu)),
            0.5 * (x_vals - mu) * np.exp(-lam * (x_vals - mu))
        )

        dF_dmu = np.where(
            x_vals <= mu,
            -0.5 * lam * np.exp(lam * (x_vals - mu)),
            -0.5 * lam * np.exp(-lam * (x_vals - mu))
        )

        variance = (dF_dlambda ** 2) * var_lambda + (dF_dmu ** 2) * var_mu
        return variance

    def get_inverse_cdf(self, x, params):
        loc = params[0]
        scale = params[1]
        return stats.laplace.ppf(x, loc=loc, scale=scale)