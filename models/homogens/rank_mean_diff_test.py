import numpy as np
from scipy.stats import norm, rankdata
from models.homogens.base_homogen_test import BaseHomogenTest


class RankMeanDiffTest(BaseHomogenTest):
    """Homogeneity Rank Mean Difference test."""

    def name(self) -> str:
        """
        Returns: "rank mean difference test"
        """
        return "rank mean difference test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Rank Mean Difference test.
        Args:
            samples (list[np.ndarray]): two input data arrays
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "v_statistic": float(v),
                "z_crit": float(z_crit),
                "p_value": float(p_value),
                "decision": decision
            }
        """
        if len(samples) != 2: return {}
        if not is_independent:
            raise ValueError("Rank Mean Difference test is used only for independent samples")

        x, y = samples
        N1, N2 = len(x), len(y)
        N = N1 + N2

        all_values = np.concatenate([x, y])
        ranks = rankdata(all_values, method="average")

        rx = np.mean(ranks[:N1])
        ry = np.mean(ranks[N1:])

        v = (rx - ry) / (N * np.sqrt((N + 1) / 12 * N1 * N2))

        z_crit = norm.ppf(1 - alpha / 2)
        p_value = 2 * (1 - norm.cdf(abs(v)))
        decision = abs(v) < z_crit

        return {
            "v_statistic": float(v),
            "z_crit": float(z_crit),
            "p_value": float(p_value),
            "decision": decision
        }