from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class ExponentialDistribution(StatisticalDistribution):
    """Exponential distribution."""
    
    def __init__(self):
        super().__init__()
        self.color = 'green'
        self.name = 'Exponential'
    
    def fit(self, data):
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01
            
        mean = np.nanmean(data)
        if mean == 0:
            mean = 0.01
        return (1/mean,)
    
    def get_pdf(self, x, params):
        return stats.expon.pdf(x, loc=0, scale=1/params[0] if params[0] > 0 else 1)
    
    def get_distribution_object(self, params):
        return stats.expon(scale=1/params[0]) if params[0] > 0 else stats.expon()
    
    def _get_plot_range(self, data):
        min_val = np.nanmin(data)
        x_min = max(0, min_val * 0.8) if min_val > 0 else 0
        x_max = np.nanmax(data) * 1.2
        return x_min, x_max