import numpy as np
from scipy.stats import norm
from models.homogens.base_homogen_test import BaseHomogenTest


class MannWhitneyUTest(BaseHomogenTest):
    """Homogeneity Mann-Whitney U test."""

    def name(self) -> str:
        """
        Returns: "Mann-Whitney U test"
        """
        return "Mann-Whitney U test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Mann-Whitney U test.
        Args:
            samples (list[np.ndarray]): two input data arrays
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "u_statistic": float,
                "E[U]": float,
                "D[U]": float,
                "u_value": float,
                "z_crit": float,
                "p_value": float,
                "decision": bool
            }
        """
        if len(samples) != 2: return {}
        if not is_independent:
            raise ValueError("Mann-Whitney U test is used only for independent samples")

        x, y = samples
        N1, N2 = len(x), len(y)
        N = N1 + N2

        U = sum(1 for xi in x for yj in y if xi > yj)

        EU = (N1 * N2) / 2
        DU = N1 * N2 * (N + 1) / 12

        u = (U - EU) / np.sqrt(DU)

        z_crit = norm.ppf(1 - alpha / 2)
        p_value = 2 * (1 - norm.cdf(abs(u)))
        decision = abs(u) < z_crit

        return {
            "u_statistic": float(U),
            "E[U]": float(EU),
            "D[U]": float(DU),
            "u_value": float(u),
            "z_crit": float(z_crit),
            "p_value": float(p_value),
            "decision": decision
        }