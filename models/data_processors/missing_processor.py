import numpy as np
import pandas as pd
from scipy import interpolate

class MissingProcessor:
    """
    Class for detecting and handling missing values in pandas Series.
    """
    @staticmethod
    def detect_missing(data: pd.Series) -> dict:
        """
        Detect missing values in the series.
        Args:
            data: input pandas Series
        Return:
            dictionary with total count, percentage, and indices of missing values
        """
        missing_mask = data.isna()
        return {
            'total_missing': missing_mask.sum(),
            'missing_percentage': missing_mask.mean() * 100,
            'missing_indices': missing_mask[missing_mask].index.tolist()
        }

    @staticmethod
    def replace_missing_with_mean(data: pd.Series) -> pd.Series:
        """
        Replace missing values with the mean of the series.
        Args:
            data: input pandas Series
        Return:
            series with NaNs replaced by mean
        """
        return data.fillna(data.mean())

    @staticmethod
    def replace_missing_with_median(data: pd.Series) -> pd.Series:
        """
        Replace missing values with the median of the series.

            data: input pandas Series
        Return:
            series with NaNs replaced by median
        """
        return data.fillna(data.median())

    @staticmethod
    def interpolate_missing(data: pd.Series, method: str = 'linear') -> pd.Series:
        """
        Interpolate missing values using the specified method.
        Args:
            data: input pandas Series
            method: interpolation method ('linear', 'quadratic', 'cubic')
        Return:
            series with interpolated values
        """
        if method not in ['linear', 'quadratic', 'cubic']:
            raise ValueError(f"Unsupported method: {method}")

        x = data.index
        valid = ~data.isna()

        f = interpolate.interp1d(
            x[valid], data[valid], kind=method, fill_value='extrapolate'
        )

        new_data = data.copy()
        new_data[data.isna()] = f(x[data.isna()])
        return new_data

    @staticmethod
    def drop_missing(data: pd.Series) -> pd.Series:
        """
        Drop all missing values from the series.
        Args:
            data: input pandas Series
        Return:
             series without NaNs
        """
        return data.dropna()