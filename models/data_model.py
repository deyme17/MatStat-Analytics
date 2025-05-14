import numpy as np
import pandas as pd
from models.graph_model.hist_models import Hist
from models.graph_model.edf_model import EmpiricalDistribution

class DataModel:
    def __init__(self, series: pd.Series, bins: int = 10, label: str = "Original"):
        self.original = series.copy()
        self.series = series.dropna().reset_index(drop=True)
        self.label = label
        self.bins = bins

        if self.series.empty:
            raise ValueError("No valid data points in series")

        self.n = len(self.series)
        self.min = self.series.min()
        self.max = self.series.max()
        self.mean = self.series.mean()
        self.std = self.series.std(ddof=1)
        self.var = self.series.var(ddof=1)
        self.hist = Hist(self.series, bins)
        self.edf = EmpiricalDistribution(self.series)
        self.transform_state = None
        self.anomalies_removed = False

    def describe(self):
        return {
            "n": self.n,
            "mean": self.mean,
            "std": self.std,
            "var": self.var,
            "min": self.min,
            "max": self.max
        }

    def update_bins(self, bins: int):
        self.bins = bins
        self.hist = Hist(self.series, bins)

    def apply_transformation(self, func, label=None):
        transformed = func(self.series)
        return DataModel(transformed, bins=self.bins, label=label or "Transformed")

    def revert_to_original(self):
        return DataModel(self.original, bins=self.bins, label="Original")