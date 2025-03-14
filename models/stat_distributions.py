import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class StatisticalDistributions:
    """Class for handling various statistical distributions and their visualization."""
    
    def __init__(self):
        self.available_distributions = {
            'Normal': self._fit_normal,
            'Exponential': self._fit_exponential,
            'Uniform': self._fit_uniform,
            'Weibull': self._fit_weibull,
        }
    
    def get_available_distributions(self):
        """Return list of available distribution names."""
        return list(self.available_distributions.keys())
    
    def fit_distribution(self, data, dist_name):
        """Fit specified distribution to data and return parameters."""
        if dist_name in self.available_distributions:
            return self.available_distributions[dist_name](data)
        else:
            raise ValueError(f"Distribution '{dist_name}' not supported")
    
    def plot_distribution(self, ax, data, dist_name, color='r', label=None):
        """Plot the specified distribution fitted to data."""
        if dist_name not in self.available_distributions:
            return False

        x = np.linspace(np.min(data) * 0.8, np.max(data) * 1.2, 1000)
        
        params = self.fit_distribution(data, dist_name)
        pdf_values = self._get_pdf_values(x, dist_name, params)
        
        # plot
        if label is None:
            label = f"{dist_name} Distribution"
        ax.plot(x, pdf_values, color=color, label=label)
        return True
    
    def _get_pdf_values(self, x, dist_name, params):
        """Calculate PDF values for the given distribution and parameters."""
        if dist_name == 'Normal':
            return stats.norm.pdf(x, loc=params[0], scale=params[1])
        
        elif dist_name == 'Exponential':
            return stats.expon.pdf(x, loc=0, scale=params[0])
        
        elif dist_name == 'Uniform':
            return stats.uniform.pdf(x, loc=params[0], scale=params[1]-params[0])
        
        elif dist_name == 'Weibull':
            return stats.weibull_min.pdf(x, c=params[0], loc=0, scale=params[1])
        else:
            return np.zeros_like(x)
    
    def _fit_normal(self, data):
        """Fit normal distribution and return parameters (mean, std)."""
        return stats.norm.fit(data)
    
    def _fit_exponential(self, data):
        """Fit exponential distribution and return parameters (scale)."""
        # shift data if necessary to make it positive
        min_val = np.min(data)
        if min_val <= 0:
            data = data - min_val + 0.01
        return (1/np.mean(data),)
    
    def _fit_uniform(self, data):
        """Fit uniform distribution and return parameters (min, max)."""
        return (np.min(data), np.max(data))
    
    def _fit_weibull(self, data):
        """Fit Weibull distribution and return parameters (shape, scale)."""
        # shift data if necessary to make it positive
        min_val = np.min(data)
        if min_val <= 0:
            data = data - min_val + 0.01
        return stats.weibull_min.fit(data)[:-1]  # ignoring location parameter