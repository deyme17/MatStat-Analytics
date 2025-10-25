import numpy as np
from scipy.stats import norm
from math import comb
from models.homogens.base_homogen_test import BaseHomogenTest


class SignsCriterionTest(BaseHomogenTest):
    """Homogeneity SignsCriterion test."""

    def name(self) -> str:
        """
        Returns: "Signs Criterion test"
        """
        return "Signs Criterion test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """
        Perform the Signs criterion rank-sum test.
        Args:
            samples (list[np.ndarray]): two input data arrays
            alpha (float): significance level
            is_independent (bool): True if samples are independent else False
        Returns:
            dict: {
                "S_statistic": float,
                "shift_val_theta": float or None,
                "decision": bool
            }
        """
        if len(samples) != 2: return {}
        if is_independent:
            raise ValueError("Signs criterion test is used only for dependent samples")

        x, y = samples
        N1, N2 = len(x), len(y)
        if N1 != N2:
            raise ValueError("Signs criterion test is used only for samples with identical sizes")

        z = x - y
        z = z[z != 0]
        N = len(z)

        U = (z > 0).astype(int)
        S = np.sum(U)

        alpha0, S_star = None, None
        z_crit, p_value = None, None

        if N <= 15:
            alpha0 = 2 * sum(comb(N, l) for l in range(S, N + 1)) / (2 ** N)
            decision = alpha0 >= alpha
        else:
            E_S = N / 2
            sigma_S = np.sqrt(N) / 2
            S_star = (S - E_S) / sigma_S
            z_crit = norm.ppf(1 - alpha / 2)
            p_value = 2 * (1 - norm.cdf(abs(S_star)))
            decision = abs(S_star) < z_crit

        shift_val_theta = None
        if not decision:
            shift_val_theta = np.median(z)

        return {
            "S_statistic": float(S),
            "alpha0": float(alpha0) if alpha0 is not None else None,
            "S_star": float(S_star) if S_star is not None else None,
            "z_crit": float(z_crit) if z_crit is not None else None,
            "p_value": float(p_value) if p_value is not None else None,
            "shift_val_theta": float(shift_val_theta) if shift_val_theta is not None else None,
            "decision": decision
        }