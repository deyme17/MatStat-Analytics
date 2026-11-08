import numpy as np
from .base import BaseCommunalityEstimator

class AveroidMethod(BaseCommunalityEstimator):
    """
    Estimates communalities using the squared absolute correlation sum 
    scaled by `n / (n - 1)` and divided by the grand sum (`n` - number of features).
    """
    def _estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        n = R.shape[0]
        A = self._abs_zerodiag(R)
        return (n / (n - 1)) * (A.sum(axis=1)**2 / A.sum())

    def name(self):
        return "Averoid Method"