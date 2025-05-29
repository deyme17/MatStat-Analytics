from abc import ABC, abstractmethod
from scipy.stats import chisquare, kstest
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class StatisticalDistribution(ABC):
    """Abstract base class for statistical distributions."""
    
    def __init__(self):
        self.color = 'red'  # default color
        self.name = self.__class__.__name__
    
    @abstractmethod
    def fit(self, data):
        """Fit distribution to data and return parameters."""
        pass
    
    @abstractmethod
    def get_pdf(self, x, params):
        """Calculate PDF values for given parameters."""
        pass
    
    def get_distribution_object(self, params):
        """Get scipy distribution object with fitted parameters."""
        return None
    
    def get_plot_data(self, data, params):
        x_min, x_max = self._get_plot_range(data)
        x = np.linspace(x_min, x_max, 1000)
        pdf = self.get_pdf(x, params)
        return x, pdf
        
    def _get_plot_range(self, data):
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        return min_val * 0.8, max_val * 1.2

    def __str__(self):
        """Return formatted distribution name."""
        return f"{self.name} Distribution"