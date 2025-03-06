import seaborn as sns
from scipy.stats import norm, expon
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Hist:
    def __init__(self, data, bins=10):
        self.data = np.sort(data)
        self.bins = bins

        # we'll use it for EDF
        self.bin_edges = np.linspace(self.data.min(), self.data.max(), self.bins + 1)
        self.bin_counts, _ = np.histogram(self.data, bins=self.bin_edges)

import seaborn as sns
from scipy.stats import norm, expon
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Hist:
    def __init__(self, data, bins=10):
        self.data = np.sort(data)
        self.bins = bins

        # we'll use it for EDF
        self.bin_edges = np.linspace(self.data.min(), self.data.max(), self.bins + 1)
        self.bin_counts, _ = np.histogram(self.data, bins=self.bin_edges)

    def plot_hist(self, ax, show_normal=False, show_exponential=False):
        if self.data is not None:
            ax.clear()
            
            # hist
            sns.histplot(self.data, bins=self.bins, kde=True, ax=ax, 
                        edgecolor='black', alpha=0.7, stat='probability', 
                        label='Histogram')
            
            # Plot normal distribution if selected
            if show_normal:
                mean = np.mean(self.data)
                std_dev = np.std(self.data)
                x = np.linspace(self.data.min(), self.data.max(), 1000)
                y = norm.pdf(x, mean, std_dev)
                ax.plot(x, y, 'r-', label='Normal Distribution')
            
            # Plot exponential distribution if selected
            if show_exponential:
                lambda_ = 1 / np.mean(self.data)
                x = np.linspace(0, self.data.max(), 1000)
                y_exp = lambda_ * np.exp(-lambda_ * x)
                ax.plot(x, y_exp, 'y-', label='Exponential Distribution')
            
            ax.grid(True, alpha=0.3)
            ax.set_title('Histogram with Density Curve')
            ax.set_xlabel('Values')
            ax.set_ylabel('Relative Frequency')
            ax.legend()
            
            # layout
            ax.figure.tight_layout()
            ax.figure.canvas.draw()

    def plot_EDF(self, ax):
        if self.data is not None:
            ax.clear()
            
            # cumulative freq
            cum_counts = np.cumsum(self.bin_counts)
            total_counts = cum_counts[-1]
            cum_rel_freq = cum_counts / total_counts
            
            # plot
            for i in range(len(self.bin_edges) - 1):
                x_values = [self.bin_edges[i], self.bin_edges[i + 1]]
                y_values = [cum_rel_freq[i], cum_rel_freq[i]]
                ax.plot(x_values, y_values, 'c->', linewidth=2)
            
            # final point
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

def plot_EDF(self, ax):
    if self.data is not None:
        ax.clear()
        
        # cumulative freq
        cum_counts = np.cumsum(self.bin_counts)
        total_counts = cum_counts[-1]
        cum_rel_freq = cum_counts / total_counts
        
        # plot
        for i in range(len(self.bin_edges) - 1):
            x_values = [self.bin_edges[i], self.bin_edges[i + 1]]
            y_values = [cum_rel_freq[i], cum_rel_freq[i]]
            ax.plot(x_values, y_values, 'c->', linewidth=2)
        
        # final point
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