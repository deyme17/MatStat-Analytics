import numpy as np
from scipy.stats import f
from models.homogens.base_homogen_test import BaseHomogenTest


class ANOVATest(BaseHomogenTest):
    """Homogeneity ANOVA test."""

    def name(self) -> str:
        """
        Returns: "ANOVA test"
        """
        return "ANOVA test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the ANOVA test.
        Args:
            samples (list[np.ndarray]): input data arrays (> 2)
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "S2_between": float(S2_between),
                "S2_within": float(S2_within), 
                "S2_total": float(S2_total),
                "F_statistic": float(F),
                "df1": int(df1),
                "df2": int(df2),
                "f_crit": float(f_crit),
                "p_value": float(p_value),
                "decision": bool
            }
        """
        k = len(samples)
        if k < 3: return {}

        N = sum([len(s) for s in samples])

        Ni = np.array([len(s) for s in samples])
        Ei = np.array([np.mean(s) for s in samples])
        Si2 = np.array([np.var(s, ddof=1) for s in samples])

        E = (1 / N) * sum([Ni[i] * Ei[i] for i in range(k)])

        S2_between = (1 / (k - 1)) * sum([Ni[i] * (Ei[i] - E)**2 for i in range(k)])
        S2_within = (1 / (N - k)) * sum([(Ni[i] - 1) * Si2[i] for i in range(k)])
        S2_total = S2_between + S2_within

        F = S2_between / S2_within

        df1 = k - 1
        df2 = N - k

        f_crit = f.ppf(1 - alpha, df1, df2)
        p_value = 1 - f.cdf(F, df1, df2)

        decision = F <= f_crit        

        return {
            "S2_between": float(S2_between),
            "S2_within": float(S2_within), 
            "S2_total": float(S2_total),
            "F_statistic": float(F),
            "df1": int(df1),
            "df2": int(df2),
            "f_crit": float(f_crit),
            "p_value": float(p_value),
            "decision": decision
            }