import numpy as np
from .base import BaseCommunalityEstimator

class MaxCorrelationMethod(BaseCommunalityEstimator):
    """Estimates communalities using the maximum absolute correlation of each variable."""
    def _estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        return self._abs_zerodiag(R).max(axis=1)

    def name(self):
        return "Max. Correltion Method"