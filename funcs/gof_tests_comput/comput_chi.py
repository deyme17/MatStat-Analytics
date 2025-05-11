import numpy as np
from scipy.stats import chi2

def pearson_chi2_test(data, dist, bins, alpha=0.05):
    hist, bin_edges = np.histogram(data, bins=bins)
    total = len(data)

    params = dist.fit(data)
    dist_obj = dist.get_distribution_object(params)

    cdf_vals = [dist_obj.cdf(edge) for edge in bin_edges]
    probs = np.diff(cdf_vals)
    expected = probs * total

    mask = expected > 1e-8
    hist_safe = hist[mask]
    expected_safe = expected[mask]

    chi2_stat = np.sum((hist_safe - expected_safe) ** 2 / expected_safe)
    df = np.sum(mask) - 1 - len(params)
    chi2_crit = chi2.ppf(1 - alpha, df)
    p_value = chi2.cdf(chi2_stat, df)

    return {
        "statistic": chi2_stat,
        "df": df,
        "critical": chi2_crit,
        "p_value": p_value,
        "passed": chi2_stat <= chi2_crit
    }
