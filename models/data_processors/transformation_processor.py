import pandas as pd
import numpy as np

class TransformationProcessor:
    """
    Class for applying mathematical transformations to pandas Series.
    """
    @staticmethod
    def standardize(data: pd.Series|pd.DataFrame) -> tuple[pd.Series|pd.DataFrame, dict]:
        """
        Standardize the data (Z-score normalization).
        Args:
            data: input pandas Series or DataFrame
        Return:
            tuple of (standardized data, params dict for inverse)
            params: {'col': (mean, std)} for DataFrame, {'mean': mean, 'std': std} for Series
        """
        if isinstance(data, pd.DataFrame):
            params = {col: (data[col].mean(), data[col].std()) for col in data.columns}
            result = data.copy()
            for col, (mean, std) in params.items():
                result[col] = (result[col] - mean) / std
            return result, params
        else:
            mean, std = data.mean(), data.std()
            return (data - mean) / std, {'mean': mean, 'std': std}
        
    @staticmethod
    def unstandardize(data: pd.Series|pd.DataFrame, params: dict) -> pd.Series|pd.DataFrame:
        """
        Reverse Z-score standardization using stored params.
        Args:
            data: standardized Series or DataFrame
            params: params returned from standardize()
        Return:
            data in original scale
        """
        if isinstance(data, pd.DataFrame):
            result = data.copy()
            for col, (mean, std) in params.items():
                result[col] = result[col] * std + mean
            return result
        else:
            return data * params['std'] + params['mean']

    @staticmethod
    def log_transform(data: pd.Series, kind: str = "ln") -> pd.Series:
        """
        Apply logarithmic transformation with shift to ensure positivity.
        Args:
            data: input pandas Series
            kind: type of log transformation ("ln" for natural log, "lg" for base-10, "log2" for base-2)
        Return:
            log-transformed series
        """
        shift = 0
        if data.min() <= 0: shift = abs(data.min()) + 1
        logs = {"ln": np.log, "lg": np.log10, "log2": np.log2}
        if kind not in logs:
            raise ValueError(f"Unsupported log transformation kind: {kind}")
        return logs[kind](data + shift)
        
    @staticmethod
    def inverse_log_transform(data: pd.Series, kind: str = "ln") -> pd.Series:
        """
        Apply inverse of logarithmic transformation.
        Args:
            data: log-transformed pandas Series
            kind: type of log transformation that was applied ("ln", "lg", "log2")
        Return:
            original scale series
        """
        exps = {"ln": np.exp, "lg": lambda x: 10**x, "log2": lambda x: 2**x}
        if kind not in exps:
            raise ValueError(f"Unsupported log transformation kind: {kind}")
        return exps[kind](data)

    @staticmethod
    def shift(data: pd.Series, shift_value: float) -> pd.Series:
        """
        Shift all values in the series by a constant.
        Args:
            data: input pandas Series
            shift_value: value to add to each element
        Return:
            shifted series
        """
        return data + shift_value