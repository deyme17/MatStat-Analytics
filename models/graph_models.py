import seaborn as sns
import numpy as np
import pandas as pd

class Hist:
    def __init__(self, data, bins=10):
        self.data = np.sort(data)
        self.bins = bins

        # we'll use it for EDF
        self.bin_edges = np.linspace(self.data.min(), self.data.max(), self.bins + 1)
        self.bin_counts, _ = np.histogram(self.data, bins=self.bin_edges)

    def plot_hist(self, ax):
        if self.data is not None:
            ax.clear()
            
            # hist
            sns.histplot(self.data, bins=self.bins, kde=True, ax=ax, 
                        edgecolor='black', alpha=0.7, stat='probability', 
                        label='Histogram')
            
            ax.grid(True, alpha=0.3)
            ax.set_title('Histogram with Density Curve')
            ax.set_xlabel('Values')
            ax.set_ylabel('Relative Frequency')

    def plot_EDF(self, ax):
        if self.data is not None:
            ax.clear()
            
            # cumulative freq
            cumulative_counts = np.cumsum(self.bin_counts)
            total_counts = cumulative_counts[-1]
            cumulative_relative_frequencies = cumulative_counts / total_counts
            
            x_values = []
            y_values = []
            
            # start
            x_values.append(self.bin_edges[0])
            y_values.append(0)
            
            for i in range(len(self.bin_edges) - 1):
                x_values.extend([self.bin_edges[i], self.bin_edges[i + 1]])
                y_values.extend([cumulative_relative_frequencies[i], cumulative_relative_frequencies[i]])
            
            # final
            x_values.append(self.bin_edges[-1])
            y_values.append(1)
            
            # plot
            ax.plot(x_values, y_values, 'c-', linewidth=2)
            
            # points
            for i in range(len(self.bin_edges)):
                ax.plot(self.bin_edges[i], cumulative_relative_frequencies[i - 1] if i > 0 else 0, 'co', markersize=6)
                ax.plot(self.bin_edges[i], cumulative_relative_frequencies[i] if i < len(self.bin_edges) - 1 else 1, 'co', markersize=6, markerfacecolor='white')
            
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Values')
            ax.set_ylabel('Cumulative Relative Frequency')
            ax.set_title('Empirical Distribution Function')
            
            # limits
            ax.set_ylim(-0.05, 1.05)