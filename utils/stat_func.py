import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, t, norm, chi2
from PyQt6.QtWidgets import QTableWidgetItem

def variation_series(data):
    """
    Constructs a variation series from the given data.
    
    Parameters:
        data (pd.Series): Input data series.

    Returns:
        pd.DataFrame: A DataFrame containing values, their frequencies, and relative frequencies.
    """
    value_counts = data.value_counts()
    value_counts = value_counts.sort_index()
    
    variation_series = value_counts.index.values
    frequencies = value_counts.values
    relative_frequencies = frequencies / len(data)

    return pd.DataFrame({
        'Values': variation_series,
        'Frequency': frequencies,
        'Relative Frequency': relative_frequencies
    })


def create_characteristic_table(hist):
    """
    Creates a characteristic table with statistical measures from histogram data.
    
    Parameters:
        hist (object): Histogram object containing data and bin count.

    Returns:
        pd.Series: A series with various statistical characteristics.
    """
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
        'Minimum': minimum,
        'Maximum': maximum,
        'Variance': variance,
        'RMS deviation': sigma,

        'Assymetry coeff.': skewness,
        'Excess': excess,
        'Contrec excess': contrec_excess,
        'Pearson var (%)': pearson_variation,

        'MED': median,
        'MAD': mad
    })


def confidence_intervals(data, confidence_level=0.95, precision=2):
    """
    Computes confidence intervals for various statistical measures.
    
    Parameters:
        data (pd.Series): Input data series.
        confidence_level (float, optional): Confidence level for intervals. Default is 0.95.
        precision (int, optional): Rounding precision. Default is 2.

    Returns:
        pd.Series: A series containing confidence intervals for mean, variance, standard deviation,
                   median, skewness, and kurtosis.
    """
    n = len(data)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    variance = np.var(data, ddof=1)
    median = np.median(data)
    skewness = skew(data)
    excess = kurtosis(data)
    
    # degrees of freedom
    df = n - 1
    
    # critical values
    t_crit = t.ppf((1 + confidence_level) / 2, df=df)
    chi2_lower = chi2.ppf((1 - confidence_level) / 2, df=df)
    chi2_upper = chi2.ppf((1 + confidence_level) / 2, df=df)
    
    # std errors
    se_mean = std_dev / np.sqrt(n)
    se_skewness = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
    se_kurtosis = 2 * se_skewness * np.sqrt((n * n - 1) / ((n - 3) * (n + 5)))
    
    # confidence intervals
    mean_ci = (
        round(mean - t_crit * se_mean, precision),
        round(mean + t_crit * se_mean, precision)
    )
    
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

def update_merged_table(hist_model, data, table, window):
    """
    Update the statistical data and confidence intervals.
    
    Args:
        hist_model: The histogram model
        data: The data series
        table: The table widget to update
        window: The main application window
    """
    precision = window.precision_spinbox.value()
    confidence_level = window.confidence_spinbox.value()
    
    characteristics = create_characteristic_table(hist_model)
    ci = confidence_intervals(data, confidence_level=confidence_level, precision=precision)
    
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
    
    ci_mapping = {
        'Mean': 'Mean CI',
        'RMS deviation': 'Std Deviation CI',
        'Variance': 'Variance CI',
        'MED': 'MED CI',
        'Assymetry coeff.': 'Assymetry coeff. CI',
        'Excess': 'Excess CI'
    }
    
    rows = []
    for char_name, char_value in characteristics.items():
        ci_name = ci_mapping.get(char_name)
        
        if ci_name and ci_name in ci:
            ci_values = ci[ci_name]
            char_value = round(float(char_value), precision)
            rows.append((char_name, char_value, ci_values[0], ci_values[1]))
        else:
            rows.append((char_name, char_value, 'N/A', 'N/A'))
    
    # update table
    table.setRowCount(len(rows))
    for idx, (name, lower, value, upper) in enumerate(rows):
        # set header
        table.setVerticalHeaderItem(idx, QTableWidgetItem(str(name)))
        # set values
        table.setItem(idx, 1, QTableWidgetItem(str(lower)))
        table.setItem(idx, 0, QTableWidgetItem(str(value)))
        table.setItem(idx, 2, QTableWidgetItem(str(upper)))


def set_default_bins(data):
    """
    Calculate the default number of bins based on data size.
    
    Args:
        data: The data series
        
    Returns:
        int: The recommended number of bins
    """
    bins = 10

    if not data.empty:
        classes = len(data)

        if classes <= 100:
            bins = int(classes ** (1 / 2)) if classes % 2 == 1 else int(classes ** (1 / 2)) - 1
        else:
            bins = int(classes ** (1 / 3)) if classes % 2 == 1 else int(classes ** (1 / 3)) - 1

    return max(bins, 1)