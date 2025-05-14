import numpy as np
import pandas as pd
from models.graph_model.hist_models import Hist
from models.graph_model.edf_model import EmpiricalDistribution

class DataModel:
    def __init__(
        self,
        series: pd.Series,
        bins: int = 10,
        label: str = "Original",
        history=None
    ):
        self.label = label
        self.original = series.copy()
        self.series = series.reset_index(drop=True)
        self.bins = bins

        if self.series.empty:
            raise ValueError("No valid data points in series")

        self._cache = {}
        self._recompute_cache()

        self.anomalies_removed = False
        self.history = history or []

    def _recompute_cache(self):
        self._cache['hist'] = Hist(self.series, self.bins)
        self._cache['edf'] = EmpiricalDistribution(self.series)
        self._cache['stats'] = {
            "n": len(self.series),
            "mean": self.series.mean(),
            "std": self.series.std(ddof=1),
            "var": self.series.var(ddof=1),
            "min": self.series.min(),
            "max": self.series.max()
        }

    def clear_cache(self):
        self._cache.clear()
        self._recompute_cache()

    @property
    def hist(self):
        return self._cache.get('hist')

    @property
    def edf(self):
        return self._cache.get('edf')

    def describe(self):
        return self._cache.get('stats')

    def update_bins(self, bins: int):
        self.bins = bins
        self._cache['hist'] = Hist(self.series, bins)

    def apply_transformation(self, func, label=None):
        transformed = func(self.series)
        return self.add_version(transformed, label or "Transformed")

    def add_version(self, new_series, label):
        return DataModel(
            new_series,
            bins=self.bins,
            label=label,
            history=self.history + [self]
        )

    def revert_to_original(self):
        return self.history[0] if self.history else self

    @property
    def current_transformation(self):
        if not self.history:
            return "Original"
        steps = [m.label for m in self.history[1:] + [self]]
        if len(steps) <= 3:
            return " → ".join(steps)
        return f"{steps[0]} → ... → {steps[-1]} ({len(steps)} steps)"