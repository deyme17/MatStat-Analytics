import numpy as np
from models.homogens.base_homogen_test import BaseHomogenTest


class SmirnovKolmogorovTest(BaseHomogenTest):
    """Homogeneity Smirnov-Kolmogorov test."""

    def name(self) -> str:
        """
        Returns: "smirnov-kolmogorov test"
        """
        return "smirnov-kolmogorov test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Smirnov-Kolmogorov test.
        Args:
            samples (list[np.ndarray]): two input data arrays
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "z_statistic": float(z),
                "L_z": float(l_z),
                "decision": decision
            }
        """
        if len(samples) != 2: return {}
        if not is_independent:
            raise ValueError("Smirnov-Kolmogorov test is used only for independent samples")

        x, y = samples
        N1, N2 = len(x), len(y)
        N = min(N1, N2)

        x_sorted = np.sort(x)
        y_sorted = np.sort(y)
        all_values = np.sort(np.concatenate([x_sorted, y_sorted]))

        cdf_x = np.searchsorted(x_sorted, all_values, side='right') / len(x_sorted)
        cdf_y = np.searchsorted(y_sorted, all_values, side='right') / len(y_sorted)

        max_diff = np.max(np.abs(cdf_x - cdf_y))
        z = max_diff * np.sqrt(N)

        l_z = (1 - np.exp(-2 * z**2)) * (
            1 - ((2 * z)/(3 * np.sqrt(N))) +
            ((2 * z**2) / (3 * N)) * (1 - ((2 * z**2) / 3)) +
            ((4 * z) / (9 * np.sqrt(N**3))) * ((1 / 5) - ((19 * z**2) / 15) + ((2 * z**4) / 3))
        ) if z <= 3.0 else 1.0

        decision = (1 - l_z) > alpha

        return {
            "z_statistic": float(z),
            "L_z": float(l_z),
            "decision": decision
        }