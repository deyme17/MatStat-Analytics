import numpy as np
import pandas as pd

class EmpiricalDistribution:
    """
    Empirical Distribution Function (EDF) for a sample.
    """

    def __init__(self, data: np.ndarray | pd.Series):
        if hasattr(data, 'dropna'):
            self.data = np.sort(data.dropna().values)
        else:
            self.data = np.sort(data[~np.isnan(data)])

        self.n = len(self.data)
        if self.n == 0:
            raise ValueError("No valid data points for EDF")

        self.min = self.data[0]                
        self.max = self.data[-1]                  
