import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, ttest_1samp, t, chi2, norm
from PyQt6.QtWidgets import QTableWidgetItem

class StatisticsService:
    """
    Service for computing descriptive statistics, confidence intervals, and statistical tests.
    """

    @staticmethod
    def _common_stats(data: pd.Series) -> dict:
        """
        Compute common descriptive statistics.

        :param data: input pandas Series
        :return: dictionary with n, mean, std, var, median, skewness, excess
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

        :param hist: histogram model
        :return: pandas Series with labeled values
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

        :param data: input pandas Series
        :param confidence_level: confidence level for intervals
        :param precision: number of decimals in output
        :return: pandas Series with confidence intervals as tuples
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
                round(median - t_crit * (std_dev / np.sqrt(n)), precision),
                round(median + t_crit * (std_dev / np.sqrt(n)), precision)
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

    @staticmethod
    def get_cdf_with_confidence(data: pd.Series, dist, confidence_level: float = 0.95):
        """
        Return empirical CDF with confidence intervals based on the given distribution.

        :param data: input data series
        :param dist: fitted StatisticalDistribution
        :param confidence_level: confidence level for intervals
        :return: tuple of (x values, CDF values, lower CI, upper CI) or None
        """
        stats = StatisticsService._common_stats(data)
        n = stats['n']

        params = dist.fit(data)
        dist_obj = dist.get_distribution_object(params)
        if dist_obj is None:
            return None

        x_vals = np.linspace(data.min(), data.max(), 300)
        cdf_vals = dist_obj.cdf(x_vals)

        z = norm.ppf((1 + confidence_level) / 2)
        variance = dist.get_cdf_variance(x_vals, params, n)
        epsilon = z * np.sqrt(variance)

        ci_lower = np.clip(cdf_vals - epsilon, 0, 1)
        ci_upper = np.clip(cdf_vals + epsilon, 0, 1)

        return x_vals, cdf_vals, ci_lower, ci_upper

    @staticmethod
    def perform_t_test(sample: pd.Series, true_mean: float) -> dict:
        """
        Perform one-sample t-test comparing sample mean to true mean.

        :param sample: input data
        :param true_mean: value to test against
        :return: dictionary with t-statistic and p-value
        """
        t_stat, p_value = ttest_1samp(sample, popmean=true_mean)
        return {'t_statistic': t_stat, 'p_value': p_value}

    @staticmethod
    def update_table(table, hist_model, data: pd.Series, precision: int, confidence_level: float):
        """
        Update QTableWidget with descriptive statistics and confidence intervals.

        :param table: QTableWidget to update
        :param hist_model: histogram model
        :param data: input data series
        :param precision: decimal precision for values
        :param confidence_level: confidence level for intervals
        """
        char = StatisticsService.get_characteristics(hist_model)
        ci = StatisticsService.compute_intervals(data, confidence_level, precision)

        mapping = {
            'Mean': 'Mean CI',
            'RMS deviation': 'Std Deviation CI',
            'Variance': 'Variance CI',
            'MED': 'MED CI',
            'Assymetry coeff.': 'Assymetry coeff. CI',
            'Excess': 'Excess CI'
        }

        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
        table.setRowCount(len(char))

        for i, (name, value) in enumerate(char.items()):
            value = round(float(value), precision)
            ci_name = mapping.get(name)
            lower, upper = ('N/A', 'N/A')
            if ci_name in ci:
                lower, upper = ci[ci_name]
            table.setVerticalHeaderItem(i, QTableWidgetItem(name))
            table.setItem(i, 0, QTableWidgetItem(str(lower)))
            table.setItem(i, 1, QTableWidgetItem(str(value)))
            table.setItem(i, 2, QTableWidgetItem(str(upper)))