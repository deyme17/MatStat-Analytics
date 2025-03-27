import seaborn as sns
from scipy.stats import norm
import numpy as np

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
            self.bin_edges = np.linspace(self.data.min(), self.data.max(), self.bins + 1)
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
                
                # normal distribution
                if show_normal:
                    mean = np.nanmean(self.data)
                    std_dev = np.nanstd(self.data)
                    x = np.linspace(np.nanmin(self.data), np.nanmax(self.data), 1000)
                    y = norm.pdf(x, mean, std_dev)
                    ax.plot(x, y, 'r-', label='Normal Distribution')
                
                # exp distribution
                if show_exponential:
                    # Ensure all data is positive for exponential
                    data_exp = self.data.copy()
                    min_val = np.nanmin(data_exp)
                    if min_val <= 0:
                        data_exp = data_exp - min_val + 0.01
                        
                    lambda_ = 1 / np.nanmean(data_exp)
                    x = np.linspace(0, np.nanmax(data_exp), 1000)
                    y_exp = lambda_ * np.exp(-lambda_ * x)
                    ax.plot(x, y_exp, 'g-', label='Exponential Distribution')
                
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

    def plot_EDF(self, ax):
        """
        Plots the empirical distribution function (EDF) based on cumulative relative frequencies.
        
        Parameters:
            ax (matplotlib.axes.Axes): The axes on which to plot the EDF.
        """
        if self.data is not None and len(self.data) > 0:
            ax.clear()
            
            try:
                # cumulative frequencies
                cum_counts = np.cumsum(self.bin_counts)
                total_counts = cum_counts[-1] if len(cum_counts) > 0 else 1  # Prevent division by zero
                cum_rel_freq = cum_counts / total_counts if total_counts > 0 else np.zeros_like(cum_counts)
                
                # plot EDF
                for i in range(len(self.bin_edges) - 1):
                    x_values = [self.bin_edges[i], self.bin_edges[i + 1]]
                    y_values = [cum_rel_freq[i], cum_rel_freq[i]]
                    ax.plot(x_values, y_values, 'c->', linewidth=2)
                
                # final point
                if len(self.bin_edges) > 0:
                    ax.plot(self.bin_edges[-1], 1, 'c>', markersize=2)
                
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('Values')
                ax.set_ylabel('Cumulative Relative Frequency')
                ax.set_title('Empirical Distribution Function')
                
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