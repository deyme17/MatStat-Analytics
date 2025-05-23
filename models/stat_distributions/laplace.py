from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class LaplaceDistribution(StatisticalDistribution):
    """Laplace distribution."""
    
    def __init__(self):
        super().__init__()
        self.color = 'pink'
        self.name = 'Laplace'
    
    def fit(self, data):
        try:
            shift, scale = stats.laplace.fit(data)
            scale = max(0.01, scale)
            return (shift, scale)
        except:
            shift = np.nanmean(data)
            scale = np.nanstd(data)
            if scale == 0:
                scale = 0.01
            return (shift, scale)
    
    def get_pdf(self, x, params):
        return stats.laplace.pdf(x, loc=params[0], scale=params[1])
    
    def get_cdf_variance(self, x, data, params):
        mu, lamb = params
        n = len(data)

        d_mu = 1 / (n * lamb ** 2)
        d_lamb = 1 / n
        cov = 0

        delta = x - mu
        left_mask = x <= mu
        right_mask = x > mu

        dF_dmu = np.zeros_like(x)
        dF_dlambda = np.zeros_like(x)

        dF_dmu[left_mask] = -0.5 * lamb * np.exp(lamb * delta[left_mask])
        dF_dmu[right_mask] = 0.5 * lamb * np.exp(-lamb * delta[right_mask])

        dF_dlambda[left_mask] = 0.5 * delta[left_mask] * np.exp(lamb * delta[left_mask])
        dF_dlambda[right_mask] = 0.5 * delta[right_mask] * np.exp(-lamb * delta[right_mask])

        return (
            (dF_dmu ** 2) * d_mu +
            (dF_dlambda ** 2) * d_lamb +
            2 * dF_dmu * dF_dlambda * cov
        )
    
    def get_distribution_object(self, params):
        return stats.laplace(loc=params[0], scale=params[1])