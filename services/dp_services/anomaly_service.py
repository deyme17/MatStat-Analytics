import numpy as np
import pandas as pd
from scipy import stats

class AnomalyService:
    """
    Service for detecting anomalies in numeric data using different statistical methods.
    """
    @staticmethod
    def detect_sigma_anomalies(data: pd.DataFrame, sigma: float = 3) -> dict:
        """
        Detect anomalies based on the normal distribution (±sigma * std).
        Args:
            data: input 1-dimensional pandas Dataframe
            sigma: number of standard deviations for the bounds
        Return:
            dictionary with anomaly indices and bounds
        """
        col = data.columns[0]
        series = data[col]

        mean = series.mean()
        std = series.std(ddof=1)
        lower = mean - sigma * std
        upper = mean + sigma * std
        anomalies = series.index[(series < lower) | (series > upper)].to_numpy()
        return {
            'anomalies': anomalies,
            'lower_limit': lower,
            'upper_limit': upper
        }

    @staticmethod
    def detect_conf_anomalies(data: pd.DataFrame, confidence_level: float = 0.95) -> dict:
        """
        Detect anomalies using confidence interval based on order statistics.
        Args:
            data: input 1-dimensional pandas Dataframe
            confidence_level: confidence level for the interval
        Return:
            dictionary with anomaly indices and bounds
        """
        col = data.columns[0]
        series = data[col]

        sorted_series = np.sort(series)
        n = len(series)
        gamma = 1 - confidence_level
        lower_index = max(0, int(np.round(gamma * n)) - 1)
        upper_index = min(n - 1, int(np.round((1 - gamma) * n)) - 1)
        lower = sorted_series[lower_index]
        upper = sorted_series[upper_index]
        anomalies = series.index[(series < lower) | (series > upper)].to_numpy()
        return {
            'anomalies': anomalies,
            'lower_limit': lower,
            'upper_limit': upper
        }

    @staticmethod
    def detect_asymmetry_anomalies(data: pd.DataFrame) -> dict:
        """
        Detect anomalies using asymmetry and kurtosis-adjusted limits.
        Args:
            data: input 1-dimensional pandas Dataframe
        Return:
            dictionary with anomaly indices and bounds
        """
        col = data.columns[0]
        series = data[col]
        
        N = len(series)
        mean = series.mean()
        std = series.std(ddof=1)
        skewness = stats.skew(series)
        excess = stats.kurtosis(series)

        t1 = 2 + 0.2 * np.log10(0.04 * N)
        t2 = np.sqrt(np.sqrt(19 * np.sqrt(excess + 2) + 1))

        if skewness < -0.2:
            lower = mean - t2 * std
            upper = mean + t1 * std
        elif skewness > 0.2:
            lower = mean - t1 * std
            upper = mean + t2 * std
        else:
            lower = mean - t1 * std
            upper = mean + t1 * std

        anomalies = series.index[(series < lower) | (series > upper)].to_numpy()
        return {
            'anomalies': anomalies,
            'lower_limit': lower,
            'upper_limit': upper
        }