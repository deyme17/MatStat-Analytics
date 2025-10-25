import numpy as np
from scipy.stats import chi2
from models.homogens.base_homogen_test import BaseHomogenTest


class BartlettTest(BaseHomogenTest):
    """Homogeneity Bartlett's test."""

    def name(self) -> str:
        """
        Returns: "Bartlett test"
        """
        return "Bartlett test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Bartlett's test.
        Args:
            samples (list[np.ndarray]): input data arrays (> 2)
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "S2": float(S2),
                "chi2_statistic": float(chi2_stat),
                "chi2_crit": float(chi2_crit),
                "p_value": float(p_value),
                "decision": bool
            }
        """
        k = len(samples)
        if k < 3: return {}

        Ni = np.array([len(s) for s in samples])
        Si2 = np.array([np.var(s, ddof=1) for s in samples])

        df_total = np.sum(Ni - 1)
        S2 = np.sum((Ni - 1) * Si2) / df_total

        B = -np.sum((Ni - 1) * np.log(Si2 / S2))
        C = 1 + (1 / (3 * (k - 1))) * (np.sum(1 / (Ni - 1)) - 1 / df_total)
        chi2_stat = B / C

        df = k - 1
        chi2_crit = chi2.ppf(1 - alpha, df)
        p_value = 1 - chi2.cdf(chi2_stat, df)

        decision = chi2_stat <= chi2_crit

        return {
            "S2": float(S2),
            "chi2_statistic": float(chi2_stat),
            "chi2_crit": float(chi2_crit),
            "df": int(df),
            "p_value": float(p_value),
            "decision": decision
        }