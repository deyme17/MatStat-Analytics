import numpy as np
import pandas as pd
from scipy import interpolate

class MissingService:
    @staticmethod
    def detect_missing(data: pd.Series) -> dict:
        missing_mask = data.isna()
        return {
            'total_missing': missing_mask.sum(),
            'missing_percentage': missing_mask.mean() * 100,
            'missing_indices': missing_mask[missing_mask].index.tolist()
        }

    @staticmethod
    def replace_missing_with_mean(data: pd.Series) -> pd.Series:
        return data.fillna(data.mean())

    @staticmethod
    def replace_missing_with_median(data: pd.Series) -> pd.Series:
        return data.fillna(data.median())

    @staticmethod
    def interpolate_missing(data: pd.Series, method='linear') -> pd.Series:
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
        return data.dropna()