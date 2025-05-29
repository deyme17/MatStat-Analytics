import numpy as np
from scipy import interpolate

class EmpiricalDistribution:
    def __init__(self, data):
        if hasattr(data, 'dropna'):
            self.data = np.sort(data.dropna().values)
        else:
            self.data = np.sort(data[~np.isnan(data)])

        self.n = len(self.data)
        self.min = self.data[0]
        self.max = self.data[-1]

        if self.n == 0:
            raise ValueError("No valid data points for EDF")