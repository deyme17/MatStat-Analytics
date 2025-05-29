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
    
    def get_distribution_object(self, params):
        return stats.weibull_min(c=params[0], scale=params[1])
    
    def get_cdf_variance(self, x_vals, params, n):
        alpha, beta = params

        dF_dalpha = - (x_vals ** beta) / (alpha ** 2) * np.exp(- (x_vals ** beta) / alpha)

        safe_x = np.where(x_vals == 0, 1e-10, x_vals)
        dF_dbeta = (x_vals ** beta) * np.log(safe_x) / alpha * np.exp(- (x_vals ** beta) / alpha)

        var_alpha = alpha ** 2 / n
        var_beta = beta ** 2 / n

        variance = (dF_dalpha ** 2) * var_alpha + (dF_dbeta ** 2) * var_beta
        return variance
