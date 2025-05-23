from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class NormalDistribution(StatisticalDistribution):
    """Normal (Gaussian) distribution."""
    
    def __init__(self):
        super().__init__()
        self.color = 'red'
        self.name = 'Normal'
    
    def fit(self, data):
        mean = np.nanmean(data)
        std = np.nanstd(data)
        if std == 0:
            std = 0.01
        return (mean, std)
    
    def get_pdf(self, x, params):
        return stats.norm.pdf(x, loc=params[0], scale=params[1])
    
    def get_cdf_variance(self, x, data, params):
        mean, std = params
        n = len(data)
        
        d_mean = (std ** 2) / n
        d_std = (std ** 2) / (2 * n)
        cov = 0

        coeff = 1 / (std * np.sqrt(2 * np.pi))
        exp_component = np.exp(-((x - mean) ** 2) / (2 * std ** 2))

        dF_dmean = -coeff * exp_component
        dF_dstd = -((x - mean) / (std ** 2 * np.sqrt(2 * np.pi))) * exp_component

        return (dF_dmean ** 2) * d_mean + (dF_dstd ** 2) * d_std + 2 * dF_dmean * dF_dstd * cov
    
    def get_distribution_object(self, params):
        return stats.norm(loc=params[0], scale=params[1])