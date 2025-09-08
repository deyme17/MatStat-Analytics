import pandas as pd
from models.graph_model.hist_model import Hist

class DataModel:
    """
    Model that holds the current data df along with histogram, and statistics cache.
    Supports versioning and transformations.
    """
    def __init__(self, df: pd.DataFrame, bins: int = 10, label: str = "Original", history=None):
        """
        Initialize DataModel with original data and histogram/statistics cache.
        Args:
            df: input pandas df
            bins: number of histogram bins
            label: description label for current version
            history: list of previous DataModel versions
        Raises:
             ValueError: if input df is empty
        """
        self.label = label                                 # version label
        self.original = df.copy()                      # full original df
        self._df = df.reset_index(drop=True)        # cleaned current df
        self._series = self._df.iloc[:, 0]

        self.bins = bins                                   
        self.anomalies_removed = False                     

        if self._df.empty or len(self._df) == 0:
            raise ValueError("No valid data points in df")

        self._cache = {}
        self._recompute_cache()

        self.history = history or []                       # list of previous versions

    @property
    def dataframe(self):
        return self._df
    @property
    def series(self):
        return self._series
    
    def select_column(self, idx: int):
        """Select a different column by index as current series"""
        if idx < 0 or idx >= self.df.shape[1]:
            raise IndexError("Column index out of range")
        self._series = self.df.iloc[:, idx]
        self.clear_cache()
    
    def _recompute_cache(self):
        """Recompute and store histogram, and descriptive stats in cache."""
        self._cache['hist'] = Hist(self._series, self.bins)
        self._cache['stats'] = {
            "n": len(self._series),
            "mean": self._series.mean(),
            "std": self._series.std(ddof=1),
            "var": self._series.var(ddof=1),
            "min": self._series.min(),
            "max": self._series.max()
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
        self._cache['hist'] = Hist(self._df, bins)

    def apply_transformation(self, func, label: str = None) -> 'DataModel':
        """
        Apply transformation function to current df and return a new version.
        Args:
            func: function to apply to df
            label: optional label for new version
        Return:
            new DataModel with updated df and history
        """
        transformed = func(self._df)
        return self.add_version(transformed, label or "Transformed")

    def add_version(self, new_df: pd.DataFrame, label: str) -> 'DataModel':
        """
        Create a new version of the model with updated df and current history.
        Args:
            new_df: transformed df
            label: description for the new version
        Return:
            new DataModel instance
        """
        return DataModel(
            new_df,
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