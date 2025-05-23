from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class WeibullDistribution(StatisticalDistribution):
    """Weibull distribution."""
    
    def __init__(self):
        super().__init__()
        self.color = 'orange'
        self.name = 'Weibull'

    def fit(self, data):
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01
        
        try:
            shape, _, scale = stats.weibull_min.fit(data, floc=0)
            shape = max(0.1, shape) 
            scale = max(0.1, scale) 
            return (shape, scale)
        except:
            mean = np.nanmean(data)
            std = np.nanstd(data)
            if std == 0:
                std = 0.01

            shape = 1.5  
            scale = mean / 0.9  
            return (shape, scale)
    
    def get_pdf(self, x, params):
        shape = max(0.1, params[0]) 
        scale = max(0.1, params[1])
        return stats.weibull_min.pdf(x, c=shape, loc=0, scale=scale)
    
    def get_cdf_variance(self, x, data, params):
        beta, alpha = params
        n = len(data)

        d_alpha = (alpha ** 2) / n
        d_beta = (beta ** 2) / n
        cov = 0

        x_beta = np.power(x, beta)
        exp_term = np.exp(-x_beta / alpha)
        ln_x = np.log(np.clip(x, a_min=1e-10, a_max=None))

        dF_dalpha = -x_beta / (alpha ** 2) * exp_term
        dF_dbeta = (x_beta * ln_x) / alpha * exp_term

        return (
            (dF_dalpha ** 2) * d_alpha +
            (dF_dbeta ** 2) * d_beta +
            2 * dF_dalpha * dF_dbeta * cov
        )

    
    def get_distribution_object(self, params):
        return stats.weibull_min(c=params[0], scale=params[1])