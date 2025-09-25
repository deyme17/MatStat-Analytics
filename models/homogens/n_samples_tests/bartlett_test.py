import numpy as np
from scipy.stats import norm
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
                ...
            }
        """
        if len(samples) < 3: return {}

        ...

        return {
        }