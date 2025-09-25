import numpy as np
from scipy.stats import norm
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

        ... 

        return {
        }