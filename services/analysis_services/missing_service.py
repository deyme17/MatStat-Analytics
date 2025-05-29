import numpy as np
import pandas as pd
from scipy import interpolate

class MissingService:
    """
    Service for detecting and handling missing values in pandas Series.
    """

    @staticmethod
    def detect_missing(data: pd.Series) -> dict:
        """
        Detect missing values in the series.

        :param data: input pandas Series
        :return: dictionary with total count, percentage, and indices of missing values
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

        :param data: input pandas Series
        :return: series with NaNs replaced by mean
        """
        return data.fillna(data.mean())

    @staticmethod
    def replace_missing_with_median(data: pd.Series) -> pd.Series:
        """
        Replace missing values with the median of the series.

        :param data: input pandas Series
        :return: series with NaNs replaced by median
        """
        return data.fillna(data.median())

    @staticmethod
    def interpolate_missing(data: pd.Series, method: str = 'linear') -> pd.Series:
        """
        Interpolate missing values using the specified method.

        :param data: input pandas Series
        :param method: interpolation method ('linear', 'quadratic', 'cubic')
        :raises ValueError: if method is not supported
        :return: series with interpolated values
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

        :param data: input pandas Series
        :return: series without NaNs
        """
        return data.dropna()