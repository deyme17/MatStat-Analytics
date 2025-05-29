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