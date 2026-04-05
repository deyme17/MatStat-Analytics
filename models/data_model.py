import pandas as pd
import numpy as np


class Hist:
    """
    Histogram model that computes bin counts and edges for numeric data.
    """
    def __init__(self, data, bins: int = 10):
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


class DataModel:
    """
    Model that holds the current data df along with histogram, and statistics cache.
    Supports transformations with revert to original.
    """
    def __init__(self, df: pd.DataFrame, bins: int = 10, label: str = "Original",
                 history=None, current_col_idx: int = 0):
        """
        Initialize DataModel with original data and histogram/statistics cache.
        Args:
            df: input pandas df
            bins: number of histogram bins
            label: description label for current version
            history: ignored, kept for backwards compatibility
            current_col_idx: index of currently selected column
        Raises:
             ValueError: if input df is empty
        """
        if df.empty or len(df) == 0:
            raise ValueError("No valid data points in df")

        self._original_df: pd.DataFrame = df.reset_index(drop=True).copy()
        self._df: pd.DataFrame = self._original_df.copy()

        self.label: str = label
        self.current_col_idx: int = current_col_idx
        self.bins: int = bins
        self.anomalies_removed: bool = False

        self._cache: dict = {}
        self._recompute_cache()

    @property
    def original(self) -> pd.DataFrame:
        """Original unmodified dataframe (read-only view)."""
        return self._original_df

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._df

    @property
    def series(self) -> pd.Series:
        return self._df.iloc[:, self.current_col_idx]

    def select_column(self, idx: int) -> None:
        """Select a different column by index as current series."""
        if idx < 0 or idx >= self._df.shape[1]:
            raise IndexError("Column index out of range")
        self.current_col_idx = idx
        self.clear_cache()

    def add_version_from_series(self, new_series: pd.Series, label: str) -> 'DataModel':
        """Apply series to current column in-place and return self."""
        self._df.iloc[:, self.current_col_idx] = new_series.values
        self.label = label
        self._recompute_cache()
        return self

    def add_version(self, new_df: pd.DataFrame, label: str) -> 'DataModel':
        """Apply dataframe in-place and return self."""
        self._df = new_df.reset_index(drop=True)
        self.label = label
        self._recompute_cache()
        return self

    def apply_transformation(self, func, label: str = None, to_series: bool = True) -> 'DataModel':
        """
        Apply transformation function to current df or specific column in-place.
        Args:
            func: function to apply to df or series
            label: optional label for new version
            to_series: if True, apply to current column; if False, apply to entire DataFrame
        Return:
            self
        """
        if to_series:
            transformed = func(self._df.iloc[:, self.current_col_idx])
            self._df.iloc[:, self.current_col_idx] = transformed
        else:
            self._df = func(self._df).reset_index(drop=True)
        self.label = label or "Transformed"
        self._recompute_cache()
        return self

    def revert_to_original(self, whole_dataset: bool = False) -> 'DataModel':
        """
        Revert to original data in-place and return self.
        Args:
            whole_dataset: if True revert entire df; if False revert current column only
        Return:
            self
        """
        if whole_dataset:
            self._df = self._original_df.copy()
        else:
            self._df.iloc[:, self.current_col_idx] = (
                self._original_df.iloc[:, self.current_col_idx].copy()
            )
        self.label = "Original"
        self.anomalies_removed = False
        self._recompute_cache()
        return self

    def is_current_column_modified(self) -> bool:
        """Check if current column has been modified from original."""
        return not self.series.equals(self._original_df.iloc[:, self.current_col_idx])

    def is_dataset_modified(self) -> bool:
        """Check if entire dataset has been modified from original."""
        return not self._df.equals(self._original_df)

    @property
    def current_transformation(self) -> str:
        """Return human-readable current transformation label."""
        return self.label

    def _recompute_cache(self) -> None:
        """Recompute and store histogram and descriptive stats in cache."""
        s = self.series
        self._cache['hist'] = Hist(s, self.bins)
        self._cache['stats'] = {
            "n": len(s),
            "mean": s.mean(),
            "std": s.std(ddof=1),
            "var": s.var(ddof=1),
            "min": s.min(),
            "max": s.max()
        }

    def clear_cache(self) -> None:
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

    def update_bins(self, bins: int) -> None:
        """
        Update histogram bin count and recompute histogram cache.
        Args:
            bins: new number of bins
        """
        self.bins = bins
        self._cache['hist'] = Hist(self.series, bins)