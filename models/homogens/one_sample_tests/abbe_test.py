import numpy as np
from scipy.stats import norm
from models.homogens.base_homogen_test import BaseHomogenTest


class AbbeTest(BaseHomogenTest):
    """Homogeneity Abbe test."""

    def name(self) -> str:
        """
        Returns: "Abbe independance test"
        """
        return "Abbe independance test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Abbe test.
        Args:
            samples (list[np.ndarray]): input data array
            alpha (float): significance level
            is_independent (bool): is not used here
        Returns:
            dict: {
                "d_statistic": float(d) ,
                "q_statistic": float(q) ,
                "E[q]": float(Eq),
                "D[q]": float(Dq),
                "U_statistic": float(U),
                "p_value": float(p_value),
                "decision": bool
            }
        """
        if len(samples) != 1: return {}

        x = samples[0]
        N = len(x)

        d2 = (1 / (N - 1)) * sum((x[i + 1] - x[i])**2 for i in range(N - 1))

        S2 = np.var(x, ddof=1)
        q = d2 / (2 * S2)

        Eq = 1
        Dq = (N - 2) / (N**2 - 1)

        U = (q - 1) * np.sqrt((N**2 - 1) / (N - 2))

        p_value = 2 * (1 - norm.cdf(abs(U)))
        decision = p_value > alpha

        return {
            "d2_statistic": float(d2),
            "q_statistic": float(q),
            "E[q]": float(Eq),
            "D[q]": float(Dq),
            "U_statistic": float(U),
            "p_value": float(p_value),
            "decision": decision
        }