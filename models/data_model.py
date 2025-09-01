import numpy as np
import pandas as pd
from models.graph_model.hist_model import Hist

class DataModel:
    """
    Model that holds the current data series along with histogram, and statistics cache.
    Supports versioning and transformations.
    """

    def __init__(self, series: pd.Series, bins: int = 10, label: str = "Original", history=None):
        """
        Initialize DataModel with original data and histogram/statistics cache.
        Args:
            series: input pandas Series
            bins: number of histogram bins
            label: description label for current version
            history: list of previous DataModel versions
        Raises:
             ValueError: if input series is empty
        """
        self.label = label                                 # version label
        self.original = series.copy()                      # full original series
        self.series = series.reset_index(drop=True)        # cleaned current series
        self.bins = bins                                   
        self.anomalies_removed = False                     

        if self.series.empty or len(self.series) == 0:
            raise ValueError("No valid data points in series")

        self._cache = {}
        self._recompute_cache()

        self.history = history or []                       # list of previous versions

    def _recompute_cache(self):
        """Recompute and store histogram, and descriptive stats in cache."""
        self._cache['hist'] = Hist(self.series, self.bins)
        self._cache['stats'] = {
            "n": len(self.series),
            "mean": self.series.mean(),
            "std": self.series.std(ddof=1),
            "var": self.series.var(ddof=1),
            "min": self.series.min(),
            "max": self.series.max()
        }

    def clear_cache(self):
        """Clear and recompute all cached values."""
        self._cache.clear()
        self._recompute_cache()

    @property
    def hist(self) -> Hist:
        """Return histogram object."""
        return self._cache.get('hist')

    def describe(self) -> dict:
        """Return dictionary with descriptive statistics."""
        return self._cache.get('stats')

    def update_bins(self, bins: int):
        """
        Update histogram bin count and recompute histogram cache.
        Args:            
            bins: new number of bins
        """
        self.bins = bins
        self._cache['hist'] = Hist(self.series, bins)

    def apply_transformation(self, func, label: str = None) -> 'DataModel':
        """
        Apply transformation function to current series and return a new version.
        Args:
            func: function to apply to series
            label: optional label for new version
        Return:
            new DataModel with updated series and history
        """
        transformed = func(self.series)
        return self.add_version(transformed, label or "Transformed")

    def add_version(self, new_series: pd.Series, label: str) -> 'DataModel':
        """
        Create a new version of the model with updated series and current history.
        Args:
            new_series: transformed series
            label: description for the new version
        Return:
            new DataModel instance
        """
        return DataModel(
            new_series,
            bins=self.bins,
            label=label,
            history=self.history + [self]
        )

    def revert_to_original(self) -> 'DataModel':
        """
        Revert to the original version in the transformation history.
        Return:
            first DataModel in the history or self if history is empty
        """
        return self.history[0] if self.history else self

    @property
    def current_transformation(self) -> str:
        """
        Return a human-readable description of the transformation path.
        Return:
            transformation chain as string
        """
        if not self.history:
            return "Original"
        steps = [m.label for m in self.history[1:] + [self]]
        if len(steps) <= 3:
            return " → ".join(steps)
        return f"{steps[0]} → ... → {steps[-1]} ({len(steps)} steps)"