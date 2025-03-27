import seaborn as sns
from scipy.stats import norm, t, gaussian_kde
import numpy as np
from scipy.interpolate import interp1d

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
        # Filter out NaN values from the data
        if hasattr(data, 'dropna'):
            data_no_nan = data.dropna().values
        else:
            data_no_nan = data[~np.isnan(data)]
            
        # Check if we have data after filtering
        if len(data_no_nan) == 0:
            raise ValueError("No valid data points after removing NaN values")

        # Sort the clean data
        self.data = np.sort(data_no_nan)
        self.bins = bins

        # Calculate bin edges and counts safely
        try:
            self.bin_edges = np.linspace(np.nanmin(self.data), np.nanmax(self.data), self.bins + 1)
            self.bin_counts, _ = np.histogram(self.data, bins=self.bin_edges)
        except Exception as e:
            # Fallback for edge cases
            print(f"Error in histogram calculation: {str(e)}")
            # Create uniform bins as fallback
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
                
                # Normal distribution implementation for StatisticalDistributions
                # class to use
                
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
                # Clear the axis in case of error
                ax.clear()
                ax.text(0.5, 0.5, f"Error plotting histogram: {str(e)}", 
                        ha='center', va='center', transform=ax.transAxes)
                ax.figure.canvas.draw()

    def plot_EDF(self, ax, show_smooth_edf=True):
        """
        Plots the empirical distribution function (EDF) with confidence interval.
        Uses your original step function with cyan arrows and optionally adds a smooth EDF curve
        with confidence interval.
        
        Parameters:
            ax (matplotlib.axes.Axes): The axes on which to plot the EDF.
            show_smooth_edf (bool): Whether to show the smooth EDF curve with CI.
        """
        if self.data is not None and len(self.data) > 0:
            ax.clear()
            
            try:
                n = len(self.data)
                alpha = 0.05  # for 95% CI
                
                # Calculate cumulative frequencies for the step function
                cum_counts = np.cumsum(self.bin_counts)
                total_counts = cum_counts[-1]
                cum_rel_freq = cum_counts / total_counts
                
                # Plot the EDF as a step function using your original cyan arrows
                for i in range(len(self.bin_edges) - 1):
                    x_values = [self.bin_edges[i], self.bin_edges[i + 1]]
                    y_values = [cum_rel_freq[i], cum_rel_freq[i]]
                    ax.plot(x_values, y_values, 'c->', linewidth=2)
                
                # final point
                ax.plot(self.bin_edges[-1], 1, 'c>', markersize=2)
                
                # Add smooth EDF with confidence interval if requested
                if show_smooth_edf:
                    # Calculate EDF points for smooth curve
                    x_sorted = np.sort(self.data)
                    y_edf = np.arange(1, n + 1) / n
                    
                    # Plot the EDF as a smooth curve (red color)
                    ax.plot(x_sorted, y_edf, '-', color='red', linewidth=2, label='Smooth EDF')
                    
                    # Calculate confidence bands for EDF using DKW inequality
                    epsilon = np.sqrt(np.log(2/alpha) / (2 * n))
                    y_upper = np.minimum(1, y_edf + epsilon)
                    y_lower = np.maximum(0, y_edf - epsilon)
                    
                    # Plot confidence bands for EDF (light blue)
                    ax.fill_between(x_sorted, y_lower, y_upper, color='skyblue', alpha=0.3, label='95% CI')
                
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
                # Clear the axis in case of error
                ax.clear()
                ax.text(0.5, 0.5, f"Error plotting EDF: {str(e)}", 
                        ha='center', va='center', transform=ax.transAxes)
                ax.figure.canvas.draw()