import numpy as np
from scipy.stats import norm
from models.homogens.base_homogen_test import BaseHomogenTest


class AbbeTest(BaseHomogenTest):
    """Homogeneity Abbe test."""

    def name(self) -> str:
        """
        Returns: "abbe test"
        """
        return "abbe test"

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

        ...

        return {
            "d2_statistic": float(d2) ,
            "q_statistic": float(q) ,
            "E[q]": float(Eq),
            "D[q]": float(Dq),
            "U_statistic": float(U),
            "p_value": float(p_value),
            "decision": decision
        }