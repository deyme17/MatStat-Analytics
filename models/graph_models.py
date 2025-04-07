import seaborn as sns
from scipy import stats
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy import interpolate

class Hist:
    """
    A class for handling histogram data and visualization, including empirical distribution functions (EDF).
    """

    def __init__(self, data, bins=10):
        """
        Initializes the histogram object.
        
        Parameters:
            data (array-like): Input dataset.
            bins (int): Number of bins to divide the data into (default is 10).
        
        Attributes:
            data (np.array): Sorted dataset without NaN values.
            bins (int): Number of bins.
            bin_edges (np.array): The edges of the bins.
            bin_counts (np.array): Count of data points in each bin.
        """
        # filter out NaN vals from the data
        if hasattr(data, 'dropna'):
            data_no_nan = data.dropna().values
        else:
            data_no_nan = data[~np.isnan(data)]
            
        if len(data_no_nan) == 0:
            raise ValueError("No valid data points after removing NaN values")

        # sort the clean data
        self.data = np.sort(data_no_nan)
        self.bins = bins

        # calculate bin edges
        try:
            self.bin_edges = np.linspace(np.nanmin(self.data), np.nanmax(self.data), self.bins + 1)
            self.bin_counts, _ = np.histogram(self.data, bins=self.bin_edges)
        except Exception as e:
            print(f"Error in histogram calculation: {str(e)}")

            self.bin_edges = np.linspace(np.nanmin(self.data), np.nanmax(self.data), self.bins + 1)
            self.bin_counts = np.zeros(self.bins)

    def plot_hist(self, ax, show_normal=False, show_exponential=False):
        """
        Plots a histogram with optional density curves for normal and exponential distributions.
        
        Parameters:
            ax (matplotlib.axes.Axes): The axes on which to plot the histogram.
            show_normal (bool): Whether to overlay a normal distribution curve (default: False).
            show_exponential (bool): Whether to overlay an exponential distribution curve (default: False).
        """
        if self.data is not None and len(self.data) > 0:
            ax.clear()
            
            try:
                # hist
                sns.histplot(self.data, bins=self.bins, kde=True, ax=ax, 
                             edgecolor='black', alpha=0.7, stat='probability', 
                             label='Histogram')
                
                ax.grid(True, alpha=0.3)
                ax.set_title('Histogram with Density Curve')
                ax.set_xlabel('Values')
                ax.set_ylabel('Relative Frequency')
                ax.legend()
                
                # layout
                ax.figure.tight_layout()
                ax.figure.canvas.draw()
            except Exception as e:
                print(f"Error plotting histogram: {str(e)}")
                ax.clear()
                ax.text(0.5, 0.5, f"Error plotting histogram: {str(e)}", 
                        ha='center', va='center', transform=ax.transAxes)
                ax.figure.canvas.draw()

    def plot_EDF(self, ax, show_smooth_edf=True, confidence_level=0.95):
        """
        Plots the empirical distribution function (EDF) with confidence interval.
        Uses step function with cyan arrows and optionally adds a smooth EDF curve
        with confidence interval calculated using dispersion estimate.
        
        Parameters:
            ax (matplotlib.axes.Axes): The axes on which to plot the EDF.
            show_smooth_edf (bool): Whether to show the smooth EDF curve with CI.
            confidence_level (float): Confidence level for intervals (default: 0.95).
        """
        if self.data is not None and len(self.data) > 0:
            ax.clear()
            
            try:
                n = len(self.data)
                alpha = 1 - confidence_level
                
                # calculate cum freqs
                cum_counts = np.cumsum(self.bin_counts)
                total_counts = cum_counts[-1]
                cum_rel_freq = cum_counts / total_counts
                
                # plot the EDF
                for i in range(len(self.bin_edges) - 1):
                    x_values = [self.bin_edges[i], self.bin_edges[i + 1]]
                    y_values = [cum_rel_freq[i], cum_rel_freq[i]]
                    ax.plot(x_values, y_values, 'c->', linewidth=2)
                
                # final point
                ax.plot(self.bin_edges[-1], 1, 'c>', markersize=2)
                
                # smooth EDF with confidence intervals
                if show_smooth_edf:
                    x_sorted = np.sort(self.data)
                    y_edf = np.arange(1, n + 1) / n

                    # create smooth x points
                    x_smooth = np.linspace(np.min(self.data), np.max(self.data), 300)
                    
                    # interpolate EDF values
                    f_linear = interpolate.interp1d(x_sorted, y_edf, kind='linear', 
                                                bounds_error=False, fill_value=(0, 1))
                    y_interp = f_linear(x_smooth)
                    
                    # Gaussian smoothing
                    sigma = 8
                    y_smooth = gaussian_filter1d(y_interp, sigma=sigma)
                    
                    # limits
                    y_smooth[0] = 0.0
                    y_smooth[-1] = 1.0
                    y_smooth = np.clip(y_smooth, 0, 1)
                    
                    # plot the smooth EDF curve
                    ax.plot(x_smooth, y_smooth, '-', color='red', linewidth=2, label='EDF Curve')
                    
                    # confidence bands
                    from scipy import stats
                    u_quantile = stats.norm.ppf(1 - alpha/2)
                    dispersion_estimate = y_smooth * (1 - y_smooth) / n
                    ci_width = u_quantile * np.sqrt(dispersion_estimate)
                    
                    y_upper = np.minimum(1, y_smooth + ci_width)
                    y_lower = np.maximum(0, y_smooth - ci_width)
                    
                    ax.fill_between(x_smooth, y_lower, y_upper, color='skyblue', alpha=0.3, 
                                label=f'{confidence_level*100:.0f}% CI')
                    
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('Values')
                ax.set_ylabel('Probability')
                ax.set_title('Empirical Distribution Function')
                if show_smooth_edf:
                    ax.legend()
                
                # limits
                ax.set_ylim(-0.05, 1.05)
                
                # layout
                ax.figure.tight_layout()
                ax.figure.canvas.draw()
                
            except Exception as e:
                print(f"Error plotting EDF: {str(e)}")

                ax.clear()
                ax.text(0.5, 0.5, f"Error plotting EDF: {str(e)}", 
                        ha='center', va='center', transform=ax.transAxes)
                ax.figure.canvas.draw()