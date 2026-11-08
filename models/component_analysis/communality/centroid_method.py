import numpy as np
from .base import BaseCommunalityEstimator

class CentroidMethod(BaseCommunalityEstimator):
    """
    Estimates communalities using the squared sum of a variable's 
    absolute correlations divided by the matrix grand sum.
    """
    def _estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        A = self._abs_zerodiag(R)
        np.fill_diagonal(A, A.max(axis=1))
        return A.sum(axis=1)**2 / A.sum()

    def name(self):
        return "Centroid Method"