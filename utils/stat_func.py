import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, t, norm, chi2
import math

def variation_series(data):
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
    data_num = len(hist.data)  
    splitting_step = round(data_num / hist.bins, 2)

    mean = round(np.mean(hist.data), 2)
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

        'Assymetry coeff.': skewness,
        'Excess': excess,
        'Contrec excess': contrec_excess,
        'Pearson var (%)': pearson_variation,

        'MED': median,
        'MAD': mad
    })


def confidence_intervals(data, confidence_level=0.95, precision=2):
    n = len(data)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    variance = np.var(data, ddof=1)
    median = np.median(data)
    skewness = skew(data)
    excess = kurtosis(data)
    
    # freesom deg
    df = n - 1
    
    # crit vals
    t_crit = t.ppf((1 + confidence_level) / 2, df=df)
    chi2_lower = chi2.ppf((1 - confidence_level) / 2, df=df)
    chi2_upper = chi2.ppf((1 + confidence_level) / 2, df=df)
    
    # std err (se)
    se_mean = std_dev / np.sqrt(n)
    se_skewness = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
    se_kurtosis = 2 * se_skewness * np.sqrt((n * n - 1) / ((n - 3) * (n + 5)))
    
    # conf intervals
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

def standardize_data(data):
    mean = data.mean()
    std = data.std()
    return (data - mean) / std

def log_transform_data(data):
    min_value = data.min()
    if min_value <= 0:
        shift = abs(min_value) + 1
        return np.log(data + shift)
    else:
        return np.log(data)

def shift_data(data, shift_value):
    return data + shift_value