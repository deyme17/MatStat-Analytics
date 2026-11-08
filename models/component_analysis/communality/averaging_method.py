import numpy as np
from .base import BaseCommunalityEstimator

class AveragingMethod(BaseCommunalityEstimator):
    """Estimates communalities using the average absolute correlation of each variable."""
    def _estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        n = R.shape[0]
        A = self._abs_zerodiag(R)
        return (1 / (n - 1)) * A.sum(axis=0)

    def name(self):
        return "Averaging Method"