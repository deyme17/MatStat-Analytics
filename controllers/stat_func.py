import pandas as pd
import numpy as np

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