import pandas as pd
import numpy as np
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
    average = round(np.mean(hist.data), 2)
    sigma = round(np.std(hist.data, ddof=1), 2)
    variance = round(np.var(hist.data, ddof=1), 2)

    return pd.Series({
        'Classes': hist.bins,
        'Splitting step': splitting_step,
        'Number of data': data_num,
        'Average': average,
        'Variance': variance,
        'RMS deviation': sigma
    })