from scipy import stats, interpolate
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

def detect_ci_anomalies(data, confidence_level=0.95):
    """
    Detect anomalies using confidence intervals and variation series.
    
    Args:
        data: numpy array or pandas Series
        confidence_level: confidence level (default: 0.95)
        
    Returns:
        Dictionary with anomaly indices and threshold values
    """
    sorted_data = np.sort(data)
    gamma = 1 - confidence_level
    
    n = len(data)
    

    lower_index = max(0, int(np.floor(gamma * n)))
    upper_index = min(n - 1, int(np.ceil((1 - gamma) * n)) - 1)

    lower_limit = sorted_data[lower_index]
    upper_limit = sorted_data[upper_index]
    
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

def detect_missing_values(data):
    """
    Detect missing values in the dataset.
    
    Args:
        data (pd.Series): Input data series
    
    Returns:
        dict: Information about missing values
    """
    missing_mask = data.isna()
    return {
        'total_missing': missing_mask.sum(),
        'missing_percentage': missing_mask.mean() * 100,
        'missing_indices': missing_mask[missing_mask].index.tolist()
    }

def interpolate_missing_values(data, method='linear'):
    """
    Interpolate missing values using various methods.
    
    Args:
        data (pd.Series): Input data series
        method (str): Interpolation method ('linear', 'quadratic', 'cubic')
    
    Returns:
        pd.Series: Data series with interpolated values
    """
    methods = {
        'linear': 1,
        'quadratic': 2,
        'cubic': 3
    }
    
    if method not in methods:
        raise ValueError(f"Method {method} not supported. Choose from: {list(methods.keys())}")
    
    x = data.index
    valid_mask = ~data.isna()
    
    f = interpolate.interp1d(
        x[valid_mask], 
        data[valid_mask], 
        kind=method, 
        fill_value='extrapolate'
    )
    
    interpolated_data = data.copy()
    interpolated_data[data.isna()] = f(x[data.isna()])
    
    return interpolated_data

def replace_missing_with_mean(data):
    """
    Replace missing values with mean of the dataset.
    
    Args:
        data (pd.Series): Input data series
    
    Returns:
        pd.Series: Data series with missing values replaced by mean
    """
    return data.fillna(data.mean())

def replace_missing_with_median(data):
    """
    Replace missing values with median of the dataset.
    
    Args:
        data (pd.Series): Input data series
    
    Returns:
        pd.Series: Data series with missing values replaced by median
    """
    return data.fillna(data.median())

def drop_missing_values(data):
    """
    Drop rows containing missing values.
    
    Args:
        data (pd.Series): Input data series
    
    Returns:
        pd.Series: Data series with missing rows dropped
    """
    return data.dropna()