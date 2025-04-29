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