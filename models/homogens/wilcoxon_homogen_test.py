import numpy as np
from scipy.stats import norm, rankdata
from models.homogens.base_homogen_test import BaseHomogenTest


class WilcoxonHomogenTest(BaseHomogenTest):
    """Homogeneity wilcoxon test."""

    def name(self) -> str:
        """
        Returns: "wilcoxon test"
        """
        return "wilcoxon test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Wilcoxon rank-sum test.
        Args:
            samples (list[np.ndarray]): two input data arrays
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                'w_statistic': float,
                'z_value': float,
                'p_value': float,
                'decision': bool
            }
        """
        if len(samples) != 2: return {}
        if not is_independent:
            raise ValueError("Wilcoxon test uses only for independent samples")

        x, y = samples
        N1, N2 = len(x), len(y)
        N = N1 + N2

        all_values = np.concatenate([x, y])
        ranks = rankdata(all_values, method="average")

        W = np.sum(ranks[:N1])

        EW = N1 * (N + 1) / 2
        DW = N1 * N2 * (N + 1) / 12

        w = (W - EW) / np.sqrt(DW)

        z_crit = norm.ppf(1 - alpha / 2)
        p_value = 2 * (1 - norm.cdf(abs(w)))
        decision = abs(w) < z_crit

        return {
            "w_statistic": float(W),
            "E[W]": float(EW),
            "D[W]": float(DW),
            "w_value": float(w),
            "z_crit": float(z_crit),
            "p_value": float(p_value),
            "decision": decision
        }