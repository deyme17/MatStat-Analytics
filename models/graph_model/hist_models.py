import seaborn as sns
import numpy as np
from models.graph_model.edf_model import EmpiricalDistribution

class Hist:
    def __init__(self, data, bins=10):
        if hasattr(data, 'dropna'):
            self.data = data.dropna().values
        else:
            self.data = data[~np.isnan(data)]

        self.bins = bins
        self.n = len(self.data)
        self.min = np.nanmin(self.data)
        self.max = np.nanmax(self.data)

        if self.n == 0:
            raise ValueError("No valid data points after removing NaN values")

        try:
            self.bin_edges = np.linspace(self.min, self.max, self.bins + 1)
            self.bin_counts, _ = np.histogram(self.data, bins=self.bin_edges)
        except Exception as e:
            print(f"Error in histogram calculation: {str(e)}")
            self.bin_edges = np.linspace(self.min, self.max, self.bins + 1)
            self.bin_counts = np.zeros(self.bins)

    def plot_hist(self, ax, show_kde):
        if self.data is not None and self.n > 0:
            ax.clear()
            try:
                sns.histplot(self.data, bins=self.bins, kde=show_kde, ax=ax, 
                             edgecolor='black', alpha=0.7, stat='probability', 
                             label='Histogram')

                ax.grid(True, alpha=0.3)
                ax.set_title('Histogram')
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
        if self.data is not None and self.n > 0:
            edf_plotter = EmpiricalDistribution(self.data)
            edf_plotter.plot(ax, bin_edges=self.bin_edges, show_edf_curve=show_edf_curve)