import numpy as np
import pandas as pd
from scipy import stats

class AnomalyService:
    @staticmethod
    def detect_normal_anomalies(data: pd.Series, threshold=3) -> dict:
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        lower = mean - threshold * std
        upper = mean + threshold * std
        anomalies = np.where((data < lower) | (data > upper))[0]
        return {'anomalies': anomalies, 'lower_limit': lower, 'upper_limit': upper}

    @staticmethod
    def detect_conf_anomalies(data: pd.Series, confidence_level=0.95) -> dict:
        sorted_data = np.sort(data)
        n = len(data)
        gamma = 1 - confidence_level
        lower_index = max(0, int(np.round(gamma * n)) - 1)
        upper_index = min(n - 1, int(np.round((1 - gamma) * n)) - 1)
        lower = sorted_data[lower_index]
        upper = sorted_data[upper_index]
        anomalies = np.where((data < lower) | (data > upper))[0]
        return {'anomalies': anomalies, 'lower_limit': lower, 'upper_limit': upper}

    @staticmethod
    def detect_asymmetry_anomalies(data: pd.Series) -> dict:
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
        return {'anomalies': anomalies, 'lower_limit': lower, 'upper_limit': upper}