import numpy as np
from scipy.stats import chi2
from models.homogens.base_homogen_test import BaseHomogenTest


class CochranQTest(BaseHomogenTest):
    """Homogeneity Cochran's Q test."""

    def name(self) -> str:
        """
        Returns: "Cochran Q test"
        """
        return "Cochran Q test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Cochran's Q test.
        Args:
            samples (list[np.ndarray]): input data arrays (> 2)
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "Q_statistic": float(q),
                "df": int(df),
                "chi2_crit": float(chi2_crit),
                "p_value": float(p_value),
                "decision": bool
            }
        """
        k = len(samples)
        if k < 3: return {}

        for i, sample in enumerate(samples):
            if not np.all(np.isin(sample, [0, 1])):
                raise ValueError(f"Sample {i} contains non-binary values. Cochran Q test requires binary data (0 or 1).")
        
        n = len(samples[0])
        for i, sample in enumerate(samples[1:], 1):
            if len(sample) != n:
                raise ValueError(f"All samples must have the same length. Sample 0 has length {n}, sample {i} has length {len(sample)}.")
        

        data_matrix = np.column_stack(samples)

        T_j = np.sum(data_matrix, axis=0)
        sum_T_j = np.sum(T_j)
        T_mean = sum_T_j / k
        
        u_i = np.sum(data_matrix, axis=1)
        sum_u_i_squared = np.sum(u_i ** 2)
        
        
        numerator = k * (k - 1) * np.sum((T_j - T_mean) ** 2)
        denominator = k * np.sum(u_i) - sum_u_i_squared
        
        if denominator == 0: return {}
        
        Q_statistic = numerator / denominator
        
        df = k - 1
        chi2_crit = chi2.ppf(1 - alpha, df)
        p_value = 1 - chi2.cdf(Q_statistic, df)
        
        decision = Q_statistic <= chi2_crit
        
        return {
            "Q_statistic": float(Q_statistic),
            "df": int(df),
            "chi2_crit": float(chi2_crit),
            "p_value": float(p_value),
            "decision": bool(decision)
        }