import numpy as np
from scipy.stats import norm
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
                ...
            }
        """
        if len(samples) < 3: return {}

        ...

        return {
        }