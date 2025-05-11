import pandas as pd
import numpy as np

class TransformationService:
    @staticmethod
    def standardize(data: pd.Series) -> pd.Series:
        mean = data.mean()
        std = data.std()
        return (data - mean) / std

    @staticmethod
    def log_transform(data: pd.Series) -> pd.Series:
        min_value = data.min()
        shift = abs(min_value) + 1 if min_value <= 0 else 0
        return np.log(data + shift)

    @staticmethod
    def shift(data: pd.Series, shift_value: float) -> pd.Series:
        return data + shift_value