import numpy as np
from scipy.stats import kstwobign

def kolmogorov_smirnov_test(data, dist, alpha=0.05):
    n = len(data)
    sorted_data = np.sort(data)
    params = dist.fit(data)
    dist_obj = dist.get_distribution_object(params)

    cdf_vals = dist_obj.cdf(sorted_data)
    ecdf_vals = np.arange(1, n + 1) / n

    dn_plus = np.max(ecdf_vals - cdf_vals)
    dn_minus = np.max(cdf_vals - (np.arange(0, n) / n))
    dn = max(dn_plus, dn_minus)

    z = np.sqrt(n) * dn
    critical = kstwobign.ppf(1 - alpha)
    p_value = 1 - _kolmogorov_cdf(z)

    return {
        "dn": dn,
        "z": z,
        "critical": critical,
        "p_value": p_value,
        "passed": z <= critical
    }

def _kolmogorov_cdf(z):
    if z < 1.18:
        return 0.0
    sum_term = 0.0
    for k in range(1, 101):
        term = (-1) ** (k - 1) * np.exp(-2 * (k ** 2) * (z ** 2))
        sum_term += term
    return max(0.0, min(1.0, 1 - 2 * sum_term))
