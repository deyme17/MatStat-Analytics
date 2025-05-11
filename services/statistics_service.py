import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, t, chi2
from PyQt6.QtWidgets import QTableWidgetItem

class StatisticsService:
    @staticmethod
    def get_characteristics(hist) -> pd.Series:
        data_num = len(hist.data)
        splitting_step = round(data_num / hist.bins, 2)

        mean = round(np.mean(hist.data), 2)
        minimum = round(np.min(hist.data), 2)
        maximum = round(np.max(hist.data), 2)
        sigma = round(np.std(hist.data, ddof=1), 2)
        variance = round(np.var(hist.data, ddof=1), 2)

        skewness = round(skew(hist.data), 2)
        excess = round(kurtosis(hist.data), 2)
        contrec_excess = round(1 / (excess + 3), 2) if (excess + 3) != 0 else 0
        pearson_variation = round((sigma / mean) * 100, 2) if mean != 0 else 0

        median = round(np.median(hist.data), 2)
        mad = round(np.median(np.abs(hist.data - median)), 2)

        return pd.Series({
            'Classes': hist.bins,
            'Number of data': data_num,
            'Splitting step': splitting_step,
            'Mean': mean,
            'Variance': variance,
            'RMS deviation': sigma,
            'Minimum': minimum,
            'Maximum': maximum,
            'Assymetry coeff.': skewness,
            'Excess': excess,
            'Contrec excess': contrec_excess,
            'Pearson var (%)': pearson_variation,
            'MED': median,
            'MAD': mad
        })

    @staticmethod
    def compute_intervals(data: pd.Series, confidence_level=0.95, precision=2) -> pd.Series:
        n = len(data)
        mean = np.mean(data)
        std_dev = np.std(data, ddof=1)
        variance = np.var(data, ddof=1)
        median = np.median(data)
        skewness = skew(data)
        excess = kurtosis(data)

        df = n - 1

        t_crit = t.ppf((1 + confidence_level) / 2, df=df)
        chi2_lower = chi2.ppf((1 - confidence_level) / 2, df=df)
        chi2_upper = chi2.ppf((1 + confidence_level) / 2, df=df)

        se_mean = std_dev / np.sqrt(n)
        se_skewness = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
        se_kurtosis = 2 * se_skewness * np.sqrt((n * n - 1) / ((n - 3) * (n + 5)))

        mean_ci = (round(mean - t_crit * se_mean, precision), round(mean + t_crit * se_mean, precision))
        variance_ci = (
            round((n - 1) * variance / chi2_upper, precision),
            round((n - 1) * variance / chi2_lower, precision)
        )
        std_dev_ci = (
            round(np.sqrt((n - 1) * variance / chi2_upper), precision),
            round(np.sqrt((n - 1) * variance / chi2_lower), precision)
        )
        skewness_ci = (
            round(skewness - t_crit * se_skewness, precision),
            round(skewness + t_crit * se_skewness, precision)
        )
        kurtosis_ci = (
            round(excess - t_crit * se_kurtosis, precision),
            round(excess + t_crit * se_kurtosis, precision)
        )
        median_ci = (
            round(median - t_crit * (std_dev / np.sqrt(n)), precision),
            round(median + t_crit * (std_dev / np.sqrt(n)), precision)
        )

        return pd.Series({
            'Mean CI': mean_ci,
            'Std Deviation CI': std_dev_ci,
            'Variance CI': variance_ci,
            'MED CI': median_ci,
            'Assymetry coeff. CI': skewness_ci,
            'Excess CI': kurtosis_ci
        })

    @staticmethod
    def update_table(table, hist_model, data, precision, confidence_level):
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
