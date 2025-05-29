from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class UniformDistribution(StatisticalDistribution):
    """Uniform distribution."""

    def __init__(self, a=None, b=None):
        super().__init__()
        self.color = 'purple'
        self.name = 'Uniform'
        self.params = (a, b) if a is not None and b is not None else None

    @property
    def distribution_params(self):
        return {
            "a": self.params[0] if self.params else None,
            "b": self.params[1] if self.params else None
        }

    def fit(self, data):
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        if min_val == max_val:
            max_val = min_val + 0.01
        self.params = (min_val, max_val)
        return self.params

    def get_mean(self):
        if not self.params:
            return None
        a, b = self.params
        return (a + b) / 2

    def get_pdf(self, x, params):
        return stats.uniform.pdf(x, loc=params[0], scale=params[1] - params[0])

    def get_distribution_object(self, params):
        return stats.uniform(loc=params[0], scale=params[1] - params[0])

    def _get_plot_range(self, data):
        params = self.fit(data)
        x_min = params[0] - 0.1 * (params[1] - params[0])
        x_max = params[1] + 0.1 * (params[1] - params[0])
        return x_min, x_max

    def get_cdf_variance(self, x_vals, params, n):
        a, b = params

        var_a = (b - a)**2 / (12 * n)
        var_b = (b - a)**2 / (12 * n)
        cov_ab = 0

        denom = (b - a) ** 4
        term1 = ((x_vals - b) ** 2) * var_a / denom
        term2 = ((x_vals - a) ** 2) * var_b / denom
        term3 = -2 * (x_vals - a) * (x_vals - b) * cov_ab / denom

        variance = term1 + term2 + term3
        return variance

    def get_inverse_cdf(self, x, params):
        a = params[0]
        b = params[1] - params[0]
        return a + b * x