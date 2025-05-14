import seaborn as sns
import numpy as np
from models.graph_model.edf_model import EmpiricalDistribution

class Hist:
    """
    A class for handling histogram data and visualization, including empirical distribution functions (EDF).
    """

    def __init__(self, data, bins=10):
        if hasattr(data, 'dropna'):
            data_no_nan = data.dropna().values
        else:
            data_no_nan = data[~np.isnan(data)]

        if len(data_no_nan) == 0:
            raise ValueError("No valid data points after removing NaN values")

        self.data = np.sort(data_no_nan)
        self.bins = bins

        try:
            self.bin_edges = np.linspace(np.nanmin(self.data), np.nanmax(self.data), self.bins + 1)
            self.bin_counts, _ = np.histogram(self.data, bins=self.bin_edges)
        except Exception as e:
            print(f"Error in histogram calculation: {str(e)}")
            self.bin_edges = np.linspace(np.nanmin(self.data), np.nanmax(self.data), self.bins + 1)
            self.bin_counts = np.zeros(self.bins)

    def plot_hist(self, ax):
        if self.data is not None and len(self.data) > 0:
            ax.clear()
            try:
                sns.histplot(self.data, bins=self.bins, kde=True, ax=ax, 
                             edgecolor='black', alpha=0.7, stat='probability', 
                             label='Histogram')

                ax.grid(True, alpha=0.3)
                ax.set_title('Histogram with Density Curve')
                ax.set_xlabel('Values')
                ax.set_ylabel('Relative Frequency')
                ax.legend()
                ax.figure.tight_layout()
                ax.figure.canvas.draw()
            except Exception as e:
                print(f"Error plotting histogram: {str(e)}")
                ax.clear()
                ax.text(0.5, 0.5, f"Error plotting histogram: {str(e)}", 
                        ha='center', va='center', transform=ax.transAxes)
                ax.figure.canvas.draw()

    def plot_EDF(self, ax, show_edf_curve=False):
        if self.data is not None and len(self.data) > 0:
            edf_plotter = EmpiricalDistribution(self.data)
            edf_plotter.plot(ax, bin_edges=self.bin_edges, show_edf_curve=show_edf_curve)