from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats

class UniformDistribution(StatisticalDistribution):
    """Uniform distribution."""
    
    def __init__(self):
        super().__init__()
        self.color = 'purple'
        self.name = 'Uniform'
    
    def fit(self, data):
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        if min_val == max_val:
            max_val = min_val + 0.01
        return (min_val, max_val)
    
    def get_pdf(self, x, params):
        return stats.uniform.pdf(x, loc=params[0], scale=params[1]-params[0])
    
    def get_distribution_object(self, params):
        return stats.uniform(loc=params[0], scale=params[1]-params[0])
    
    def _get_plot_range(self, data):
        params = self.fit(data)
        x_min = params[0] - 0.1 * (params[1] - params[0])  
        x_max = params[1] + 0.1 * (params[1] - params[0])
        return x_min, x_max