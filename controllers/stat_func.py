import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
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

        'Assymetry coefficient': skewness,
        'Excess': excess,
        'Contrec excess': contrec_excess,
        'Pearson variation (%)': pearson_variation,

        'Median': median,
        'Median absolute deviation': mad
    })