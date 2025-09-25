import numpy as np
from scipy.stats import chi2, rankdata
from models.homogens.base_homogen_test import BaseHomogenTest


class HTest(BaseHomogenTest):
    """Homogeneity Kruskal-Wallis H test."""

    def name(self) -> str:
        """
        Returns: "H test"
        """
        return "H test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Kruskal-Wallis H test.
        Args:
            samples (list[np.ndarray]): input data arrays (> 2)
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "H_statistic": float(H),
                "df": int(df),
                "chi2_crit": float(chi2_crit), 
                "p_value": float(p_value),
                "decision": bool
            }
        """
        k = len(samples)
        if k < 3: return {}

        all_data = np.concatenate(samples)
        ranks = rankdata(all_data)

        N = len(all_data)
        H = 0.0

        start = 0
        for sample in samples:
            Ni = len(sample)
            ranks_i = ranks[start : start + Ni]
            W_bar_i = np.sum(ranks_i) / Ni
            E_W_bar = (N + 1) / 2
            var_W_bar = (N + 1) * (N - Ni) / (12 * Ni)
            H += ((W_bar_i - E_W_bar)**2) / var_W_bar * (1 - Ni / N)
            start += Ni

        df = k - 1
        chi2_crit = chi2.ppf(1 - alpha, df)
        p_value = 1 - chi2.cdf(H, df)
        decision = H <= chi2_crit

        return {
            "H_statistic": float(H),
            "df": df,
            "chi2_crit": float(chi2_crit),
            "p_value": float(p_value),
            "decision": decision
        }