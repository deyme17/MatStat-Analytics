import numpy as np
import pandas as pd
from scipy import stats

class AnomalyService:
    """
    Service for detecting anomalies in numeric data using different statistical methods.
    """

    @staticmethod
    def detect_normal_anomalies(data: pd.Series, threshold: float = 3) -> dict:
        """
        Detect anomalies based on the normal distribution (±threshold * std).
        Args:
            data: input data series
            threshold: number of standard deviations for the bounds
        Return:
            dictionary with anomaly indices and bounds
        """
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        lower = mean - threshold * std
        upper = mean + threshold * std
        anomalies = np.where((data < lower) | (data > upper))[0]
        return {
            'anomalies': anomalies,
            'lower_limit': lower,
            'upper_limit': upper
        }

    @staticmethod
    def detect_conf_anomalies(data: pd.Series, confidence_level: float = 0.95) -> dict:
        """
        Detect anomalies using confidence interval based on order statistics.
        Args:
            data: input data series
            confidence_level: confidence level for the interval
        Return:
            dictionary with anomaly indices and bounds
        """
        sorted_data = np.sort(data)
        n = len(data)
        gamma = 1 - confidence_level
        lower_index = max(0, int(np.round(gamma * n)) - 1)
        upper_index = min(n - 1, int(np.round((1 - gamma) * n)) - 1)
        lower = sorted_data[lower_index]
        upper = sorted_data[upper_index]
        anomalies = np.where((data < lower) | (data > upper))[0]
        return {
            'anomalies': anomalies,
            'lower_limit': lower,
            'upper_limit': upper
        }

    @staticmethod
    def detect_asymmetry_anomalies(data: pd.Series) -> dict:
        """
        Detect anomalies using asymmetry and kurtosis-adjusted limits.
        Args:
            data: input data series
        Return:
            dictionary with anomaly indices and bounds
        """
        N = len(data)
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        skewness = stats.skew(data)
        excess = stats.kurtosis(data)

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

        anomalies = np.where((data < lower) | (data > upper))[0]
        return {
            'anomalies': anomalies,
            'lower_limit': lower,
            'upper_limit': upper
        }
