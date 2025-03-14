from scipy import stats
import numpy as np

def standardize_data(data):
    """
    Standardizes the data.
    
    Parameters:
        data (pd.Series): Input data series.

    Returns:
        pd.Series: Standardized data.
    """
    mean = data.mean()
    std = data.std()
    return (data - mean) / std


def log_transform_data(data):
    """
    Applies a logarithmic transformation to the data. 
    
    Parameters:
        data (pd.Series): Input data series.

    Returns:
        pd.Series: Log-transformed data.
    """
    min_value = data.min()
    if min_value <= 0:
        shift = abs(min_value) + 1
        return np.log(data + shift)
    else:
        return np.log(data)


def shift_data(data, shift_value):
    """
    Shifts the data by adding a given value to each element.
    
    Parameters:
        data (pd.Series): Input data series.
        shift_value (float): The value to be added to each data point.

    Returns:
        pd.Series: Shifted data.
    """
    return data + shift_value


def detect_normal_anomalies(data, threshold=3):
    """
    Detect anomalies using normal distribution (mean ± threshold*sigma).
    
    Args:
        data: numpy array or pandas Series
        threshold: multiplier for standard deviation (default: 2.0)
        
    Returns:
        Dictionary with anomaly indices and threshold values
    """
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    lower_limit = mean - threshold * std
    upper_limit = mean + threshold * std
    
    anomalies = np.where((data < lower_limit) | (data > upper_limit))[0]
    
    return {
        'anomalies': anomalies,
        'lower_limit': lower_limit,
        'upper_limit': upper_limit
    }

def detect_anomalies(data):
    """
    Detect anomalies using asymmetry coefficient.
    
    Args:
        data: numpy array or pandas Series
        N: sample size (if None, uses len(data))
        
    Returns:
        Dictionary with anomaly indices and threshold values
    """
    N = len(data)
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    skewness = stats.skew(data)
    excess = stats.kurtosis(data)
    
    t1 = 2 + 0.2 * np.log10(0.04 * N)
    t2 = np.sqrt(np.sqrt(19 * np.sqrt(excess + 2) + 1))
    
    if skewness < -0.2:
        lower_limit = mean - t2 * std
        upper_limit = mean + t1 * std
    elif skewness > 0.2:
        lower_limit = mean - t1 * std
        upper_limit = mean + t2 * std
    else:
        lower_limit = mean - t1 * std
        upper_limit = mean + t1 * std
    
    anomalies = np.where((data < lower_limit) | (data > upper_limit))[0]
    
    return {
        'anomalies': anomalies,
        'lower_limit': lower_limit,
        'upper_limit': upper_limit
    }