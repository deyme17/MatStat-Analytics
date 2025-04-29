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
    
    def get_distribution_object(self, params):
        return stats.norm(loc=params[0], scale=params[1])