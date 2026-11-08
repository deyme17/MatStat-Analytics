import numpy as np
from .base import BaseCommunalityEstimator

class TriadsMethod(BaseCommunalityEstimator):
    """Estimates communalities using Spearman's triads formula for three variables."""
    EPSILON = 1e-11
    def _estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        n = R.shape[0]
        if n < 3:
            raise ValueError("Triads Method requiers at least 3 features")

        A = self._abs_zerodiag(R)
        h_square = np.empty((n,))

        for k in range(n):
            i, j = np.argsort(A[k])[-2:]
            denom = np.abs(R[i, j])
            h_square[k] = ((A[k, i] * A[k, j]) / denom
                          if denom > self.EPSILON else 1.)
        
        return h_square

    def name(self):
        return "Triads Method"