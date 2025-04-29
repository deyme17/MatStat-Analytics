from scipy.stats import chisquare, kstest, norm, expon, uniform, weibull_min, laplace
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
            'Laplace': self._fit_laplace,
        }
        
        self.dist_colors = {
            'Normal': 'red',
            'Exponential': 'green',
            'Uniform': 'purple',
            'Weibull': 'orange',
            'Laplace': 'pink',
        }
    
    def get_available_distributions(self):
        """Return list of available distribution names."""
        return list(self.available_distributions.keys())
    
    def get_distribution_color(self, dist_name):
        """Get the default color for a distribution."""
        return self.dist_colors.get(dist_name, 'blue')
    
    def fit_distribution(self, data, dist_name):
        """Fit specified distribution to data and return parameters."""
        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        
        if len(data_clean) == 0:
            raise ValueError("No valid data points after removing NaN values")
            
        if dist_name in self.available_distributions:
            return self.available_distributions[dist_name](data_clean)
        else:
            raise ValueError(f"Distribution '{dist_name}' not supported")
    
    def plot_distribution(self, ax, data, dist_name, color=None, label=None, **kwargs):
        """
        Plot the specified distribution fitted to data.
        
        Parameters:
            ax: matplotlib axis to plot on
            data: data to fit the distribution to
            dist_name: name of the distribution to fit
            color: color for the line (uses defaults if None)
            label: label for the legend (uses distribution name if None)
            **kwargs: Additional plotting parameters like linewidth
        
        Returns:
            bool: True if successful, False otherwise
        """
        if dist_name not in self.available_distributions:
            return False

        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        
        if len(data_clean) == 0:
            return False

        try:
            # get hist vals for proper normalization
            hist_values, bin_edges = np.histogram(data_clean, bins='auto', density=True)
            max_hist_value = np.max(hist_values) if len(hist_values) > 0 else 1.0
            
            if color is None:
                color = self.get_distribution_color(dist_name)
                
            if dist_name == 'Exponential':
                min_val = np.nanmin(data_clean)
                x_min = max(0, min_val * 0.8) if min_val > 0 else 0
                x_max = np.nanmax(data_clean) * 1.2
            elif dist_name == 'Uniform':
                params = self.fit_distribution(data_clean, dist_name)
                x_min = params[0] - 0.1 * (params[1] - params[0])  
                x_max = params[1] + 0.1 * (params[1] - params[0])  
            else:
                x_min = np.nanmin(data_clean) * 0.8
                x_max = np.nanmax(data_clean) * 1.2

            x = np.linspace(x_min, x_max, 1000)
            
            # fit dist
            params = self.fit_distribution(data_clean, dist_name)
            pdf_values = self._get_pdf_values(x, dist_name, params)
            
            # scaling
            pdf_max = np.max(pdf_values) if len(pdf_values) > 0 else 1.0
            if pdf_max > 0:
                pdf_values = pdf_values * (max_hist_value / pdf_max)
            
            # label
            if label is None:
                label = f"{dist_name} Distribution"
            
            # plot
            ax.plot(x, pdf_values, color=color, label=label, **kwargs)
                
            return True
        except Exception as e:
            print(f"Error plotting {dist_name} distribution: {str(e)}")
            return False
    
    def get_distribution_object(self, dist_name, params):
        """
        Get scipy distribution object with fitted parameters.
        
        Parameters:
            dist_name: Name of the distribution
            params: Parameters for the distribution as returned by fit_distribution()
            
        Returns:
            A scipy.stats distribution object
        """
        if dist_name == 'Normal':
            return stats.norm(loc=params[0], scale=params[1])
        elif dist_name == 'Exponential':
            return stats.expon(scale=1/params[0]) if params[0] > 0 else stats.expon()
        elif dist_name == 'Uniform':
            return stats.uniform(loc=params[0], scale=params[1]-params[0])
        elif dist_name == 'Weibull':
            return stats.weibull_min(c=params[0], scale=params[1])
        elif dist_name == 'Laplace':
            return stats.laplace(loc=params[0], scale=params[1])
        else:
            raise ValueError(f"Unsupported distribution: {dist_name}")
    
    def perform_goodness_of_fit_tests(self, data, dist_name, num_bins=10):
        """
        Perform both Pearson's Chi-squared and Kolmogorov-Smirnov goodness-of-fit tests.
        
        Parameters:
            data: Input data
            dist_name: Name of the distribution to test against
            num_bins: Number of bins for histogram (Chi-squared test)
            
        Returns:
            Dictionary with test statistics and p-values
        """
        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        
        if len(data_clean) == 0:
            raise ValueError("No valid data points after removing NaN values")
            
        # fit distr
        params = self.fit_distribution(data_clean, dist_name)
        
        dist_obj = self.get_distribution_object(dist_name, params)
        
        # chi-squared test
        hist_counts, bin_edges = np.histogram(data_clean, bins=num_bins)
        
        cdf_values = [dist_obj.cdf(edge) for edge in bin_edges]
        expected_probs = np.diff(cdf_values)
        expected_counts = expected_probs * len(data_clean)
        
        expected_counts = np.where(expected_counts < 1, 1, expected_counts)
        
        chi2_stat, chi2_p = chisquare(hist_counts, expected_counts)
        
        # Kolmogorov test
        ks_stat, ks_p = kstest(data_clean, dist_obj.cdf)
        
        return {
            'chi2_statistic': chi2_stat,
            'chi2_p_value': chi2_p,
            'ks_statistic': ks_stat,
            'ks_p_value': ks_p
        }
    
    def _get_pdf_values(self, x, dist_name, params):
        """Calculate PDF values for the given distribution and parameters."""
        if dist_name == 'Normal':
            return stats.norm.pdf(x, loc=params[0], scale=params[1])
        
        elif dist_name == 'Exponential':
            return stats.expon.pdf(x, loc=0, scale=1/params[0] if params[0] > 0 else 1)
        
        elif dist_name == 'Uniform':
            return stats.uniform.pdf(x, loc=params[0], scale=params[1]-params[0])
        
        elif dist_name == 'Weibull':
            shape = max(0.1, params[0]) 
            scale = max(0.1, params[1])
            return stats.weibull_min.pdf(x, c=shape, loc=0, scale=scale)
        
        elif dist_name == 'Laplace':
            return stats.laplace.pdf(x, loc=params[0], scale=params[1])

        else:
            return np.zeros_like(x)
    
    def _fit_normal(self, data):
        """Fit normal distribution and return parameters (mean, std)."""
        mean = np.nanmean(data)
        std = np.nanstd(data)
        if std == 0:
            std = 0.01
        return (mean, std)
    
    def _fit_exponential(self, data):
        """Fit exponential distribution and return parameters (lambda)."""
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01
            
        mean = np.nanmean(data)
        if mean == 0:
            mean = 0.01
        return (1/mean,)
    
    def _fit_uniform(self, data):
        """Fit uniform distribution and return parameters (min, max)."""
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        if min_val == max_val:
            max_val = min_val + 0.01
        return (min_val, max_val)
    
    def _fit_weibull(self, data):
        """Fit Weibull distribution and return parameters (shape, scale)."""
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
        
    def _fit_laplace(self, data):
        """Fit Laplace distribution and return parameters (shift, scale)."""
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