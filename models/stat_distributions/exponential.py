from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class ExponentialDistribution(StatisticalDistribution):
    """Exponential distribution."""

    def __init__(self, lam=None):
        super().__init__()
        self.params = (lam,)
        self.color = 'yellow'
        self.name = 'Exponential'

    @property
    def distribution_params(self):
        return {"lambda": self.params[0] if self.params else None}

    def fit(self, data):
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01

        mean = np.nanmean(data)
        if mean == 0:
            mean = 0.01
        self.params = (1 / mean,)
        return self.params

    def get_mean(self):
        if not self.params or self.params[0] == 0:
            return None
        lam = self.params[0]
        return 1 / lam

    def get_pdf(self, x, params):
        return stats.expon.pdf(x, loc=0, scale=1 / params[0] if params[0] > 0 else 1)

    def get_distribution_object(self, params):
        return stats.expon(scale=1 / params[0]) if params[0] > 0 else stats.expon()

    def _get_plot_range(self, data):
        min_val = np.nanmin(data)
        x_min = max(0, min_val * 0.8) if min_val > 0 else 0
        x_max = np.nanmax(data) * 1.2
        return x_min, x_max

    def get_cdf_variance(self, x_vals, params, n):
        lam = params[0]
        variance = (x_vals ** 2) * np.exp(-2 * lam * x_vals) * (lam ** 2) / n
        return variance

    def get_inverse_cdf(self, x, params):
        lam = params[0]
        return -np.log(1 - x) / lam