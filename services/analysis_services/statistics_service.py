import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, t, chi2

class StatisticsService:
    """
    Service for computing descriptive statistics and its confidence intervals.
    """
    @staticmethod
    def _common_stats(data: pd.Series) -> dict:
        """
        Compute common descriptive statistics.
        Args:
            data: input pandas Series
        Return:
            dictionary with n, mean, std, var, median, skewness, excess
        """
        return {
            'n': len(data),
            'mean': np.mean(data),
            'std_dev': np.std(data, ddof=1),
            'variance': np.var(data, ddof=1),
            'median': np.median(data),
            'skewness': skew(data),
            'excess': kurtosis(data)
        }

    @staticmethod
    def get_characteristics(hist) -> pd.Series:
        """
        Compute rounded descriptive stats and shape characteristics from histogram.
        Args:
            hist: histogram model
        Return:
            pandas Series with labeled values
        """
        stats = StatisticsService._common_stats(hist.data)

        splitting_step = round(stats['n'] / hist.bins, 2)
        contrec_excess = round(1 / (stats['excess'] + 3), 2) if (stats['excess'] + 3) != 0 else 0
        pearson_variation = round((stats['std_dev'] / stats['mean']) * 100, 2) if stats['mean'] != 0 else 0
        mad = round(np.median(np.abs(hist.data - stats['median'])), 2)

        return pd.Series({
            'Classes': hist.bins,
            'Number of data': stats['n'],
            'Splitting step': splitting_step,
            'Mean': round(stats['mean'], 2),
            'Variance': round(stats['variance'], 2),
            'RMS deviation': round(stats['std_dev'], 2),
            'Minimum': round(np.min(hist.data), 2),
            'Maximum': round(np.max(hist.data), 2),
            'Assymetry coeff.': round(stats['skewness'], 2),
            'Excess': round(stats['excess'], 2),
            'Contrec excess': contrec_excess,
            'Pearson var (%)': pearson_variation,
            'MED': round(stats['median'], 2),
            'MAD': mad
        })

    @staticmethod
    def compute_intervals(data: pd.Series, confidence_level: float = 0.95, precision: int = 2) -> pd.Series:
        """
        Compute confidence intervals for various characteristics.
        Args:
            data: input pandas Series
            confidence_level: confidence level for intervals
            precision: number of decimals in output
        Return:
            pandas Series with confidence intervals as tuples
        """
        stats = StatisticsService._common_stats(data)
        n, mean, std_dev, variance = stats['n'], stats['mean'], stats['std_dev'], stats['variance']
        median, skewness, excess = stats['median'], stats['skewness'], stats['excess']

        df = n - 1
        t_crit = t.ppf((1 + confidence_level) / 2, df=df)
        chi2_lower = chi2.ppf((1 - confidence_level) / 2, df=df)
        chi2_upper = chi2.ppf((1 + confidence_level) / 2, df=df)

        se_mean = std_dev / np.sqrt(n)
        se_skewness = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
        se_kurtosis = 2 * se_skewness * np.sqrt((n * n - 1) / ((n - 3) * (n + 5)))

        return pd.Series({
            'Mean CI': (round(mean - t_crit * se_mean, precision), round(mean + t_crit * se_mean, precision)),
            'Std Deviation CI': (
                round(np.sqrt((n - 1) * variance / chi2_upper), precision),
                round(np.sqrt((n - 1) * variance / chi2_lower), precision)
            ),
            'Variance CI': (
                round((n - 1) * variance / chi2_upper, precision),
                round((n - 1) * variance / chi2_lower, precision)
            ),
            'MED CI': (
                round(median - t_crit * (se_mean), precision),
                round(median + t_crit * (se_mean), precision)
            ),
            'Assymetry coeff. CI': (
                round(skewness - t_crit * se_skewness, precision),
                round(skewness + t_crit * se_skewness, precision)
            ),
            'Excess CI': (
                round(excess - t_crit * se_kurtosis, precision),
                round(excess + t_crit * se_kurtosis, precision)
            )
        })