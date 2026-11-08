import numpy as np
from .base import BaseCommunalityEstimator

class PCABasedMethod(BaseCommunalityEstimator):
    """
    Estimates communalities using the sum of squared component 
    loadings from a reduced Principal Component Analysis.
    """
    def _estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        if n_factors is None:
            raise ValueError("PCA-based estimator requires n_factors.")

        eigen_vals, eigen_vects = self._eigh_sorted(R)
        lambdas = np.clip(eigen_vals[:n_factors], 0.0, None)
        loadings = eigen_vects[:, :n_factors] * np.sqrt(lambdas)
        return (loadings**2).sum(axis=1)

    @staticmethod
    def _eigh_sorted(R: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        eigen_vals, eigen_vects = np.linalg.eigh(R)
        idx = np.argsort(eigen_vals)[::-1]
        return eigen_vals[idx], eigen_vects[:, idx]
    
    def name(self):
        return "PCA-based Method"