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
    Supports versioning and transformations.
    """
    def __init__(self, df: pd.DataFrame, bins: int = 10, label: str = "Original", history=None, current_col_idx: int = 0):
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
        self.label = label                          # version label
        self.original = df.copy()                   # full original df
        self._df = df.reset_index(drop=True)        # cleaned current df

        self.current_col_idx = current_col_idx
        self._series = self._df.iloc[:, self.current_col_idx]          # current series for plotting|stats|tests etc.
        self.bins = bins        
        self.anomalies_removed = False                     

        if self._df.empty or len(self._df) == 0:
            raise ValueError("No valid data points in df")

        self._cache = {}
        self._recompute_cache()

        self.history = history or []                       # list of previous versions

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._df
    @property
    def series(self) -> pd.Series:
        return self._series
    
    def select_column(self, idx: int) -> None:
        """Select a different column by index as current series"""
        if idx < 0 or idx >= self._df.shape[1]:
            raise IndexError("Column index out of range")
        self.current_col_idx = idx
        self._series = self._df.iloc[:, idx]
        self.clear_cache()
    
    def _recompute_cache(self) -> None:
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
        self._cache['hist'] = Hist(self._series, bins)

    def apply_transformation(self, func, label: str = None, to_series: bool = True) -> 'DataModel':
        """
        Apply transformation function to current df or specific column and return a new version.
        Args:
            func: function to apply to df or series
            label: optional label for new version
            col_idx: if True, apply transformation to current column by index;
                    if False, apply to entire DataFrame
        Return:
            new DataModel with updated df and history
        """
        if to_series:
            series_to_transform = self._df.iloc[:, self.current_col_idx]
            transformed_series = func(series_to_transform)
            new_df = self._df.copy()
            new_df.iloc[:, self.current_col_idx] = transformed_series
        else:
            new_df = func(self._df)
        
        return self.add_version(new_df, label or "Transformed")

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
            history=self.history + [self],
            current_col_idx=self.current_col_idx
        )
    
    def add_version_from_series(self, new_series: pd.Series, label: str) -> 'DataModel':
        """Create new version with updated first column from series"""
        new_df = self._df.copy()
        new_df.iloc[:, self.current_col_idx] = new_series
        return self.add_version(new_df, label)

    def revert_to_original(self, whole_dataset: bool = False) -> 'DataModel':
        """
        Revert to the original version in the transformation history.
        Args:
            revert_series: if True, revert only current column to original;
                    if False, revert entire DataFrame to original
        Return:
            DataModel with reverted data
        """
        if not self.history: return self
        original_model = self.history[0]
        
        if whole_dataset:
            return DataModel(
                original_model._df.copy(),
                bins=original_model.bins,
                label=original_model.label,
                history=original_model.history,
                current_col_idx=self.current_col_idx
            )
        else:
            new_df = self._df.copy()
            new_df.iloc[:, self.current_col_idx] = original_model.original.iloc[:, self.current_col_idx]
            label = f"Reverted column to original"
            return self.add_version(new_df, label)

    def is_current_column_modified(self) -> bool:
        """
        Check if current column has been modified from original.
        Return:
            True if current column differs from original
        """
        if not self.history: return False
        original_model = self.history[0]
        original_col = original_model.original.iloc[:, self.current_col_idx]
        return not self._series.equals(original_col)
    
    def is_dataset_modified(self) -> bool:
        """
        Check if entire dataset has been modified from original.
        Return:
            True if any column differs from original
        """
        if not self.history: return False
        original_model = self.history[0]
        return not self._df.equals(original_model.original)
    
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