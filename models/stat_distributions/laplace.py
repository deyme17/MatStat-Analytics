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
    
    def get_distribution_object(self, params):
        return stats.laplace(loc=params[0], scale=params[1])
    
    def get_cdf_variance(self, x_vals, data):
        params = self.fit(data)
        mu, lam = params

        n = data.dropna().shape[0]
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
