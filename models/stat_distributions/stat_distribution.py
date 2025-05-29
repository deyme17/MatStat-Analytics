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
        
    def perform_goodness_of_fit_tests(self, data, num_bins=10):
        """
        Perform goodness-of-fit tests.
        
        Parameters:
            data: Input data
            num_bins: Number of bins for histogram (Chi-squared test)
            
        Returns:
            Dictionary with test statistics and p-values
        """
        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        
        if len(data_clean) == 0:
            raise ValueError("No valid data points after removing NaN values")
            
        # fit distr
        params = self.fit(data_clean)
        dist_obj = self.get_distribution_object(params)
        
        if dist_obj is None:
            raise NotImplementedError("Goodness-of-fit tests not implemented for this distribution")
        
        # chi-squared test
        hist_counts, bin_edges = np.histogram(data_clean, bins=num_bins)
        cdf_values = [dist_obj.cdf(edge) for edge in bin_edges]
        expected_probs = np.diff(cdf_values)
        expected_counts = expected_probs * len(data_clean)
        expected_counts = np.where(expected_counts < 1, 1, expected_counts)
        chi2_stat, chi2_p = chisquare(hist_counts, expected_counts)
        
        # Kolmogorov-Smirnov test
        ks_stat, ks_p = kstest(data_clean, dist_obj.cdf)
        
        return {
            'chi2_statistic': chi2_stat,
            'chi2_p_value': chi2_p,
            'ks_statistic': ks_stat,
            'ks_p_value': ks_p
        }

    def __str__(self):
        """Return formatted distribution name."""
        return f"{self.name} Distribution"