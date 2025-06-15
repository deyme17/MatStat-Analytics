import pandas as pd
import numpy as np

class TransformationService:
    """
    Service for applying mathematical transformations to pandas Series.
    """

    @staticmethod
    def standardize(data: pd.Series) -> pd.Series:
        """
        Standardize the data (Z-score normalization).

        :param data: input pandas Series
        :return: standardized series with mean 0 and std 1
        """
        mean = data.mean()
        std = data.std()
        return (data - mean) / std

    @staticmethod
    def log_transform(data: pd.Series) -> pd.Series:
        """
        Apply logarithmic transformation with shift to ensure positivity.

        :param data: input pandas Series
        :return: log-transformed series
        """
        min_value = data.min()
        shift = abs(min_value) + 1 if min_value <= 0 else 0
        return np.log(data + shift)

    @staticmethod
    def shift(data: pd.Series, shift_value: float) -> pd.Series:
        """
        Shift all values in the series by a constant.

        :param data: input pandas Series
        :param shift_value: value to add to each element
        :return: shifted series
        """
        return data + shift_value