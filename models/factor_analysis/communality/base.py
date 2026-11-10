from abc import ABC, abstractmethod
import numpy as np

class BaseCommunalityEstimator(ABC):
    """Initial communality (h^2) estimation method for the principal factor method."""
    def estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        """
        Estimates communality for the principal factor method from correlation matrix.
        Args:
            R: Correlation matrix (n, n).
            n_factors: Number of common factors (used by PCA-based estimator).
        Returns:
            h^2 estimates of shape (n,), clipped to [0, 1].
        """
        if R.shape[0] < 2:
            raise ValueError("At least 2 features are required.")
        h_squared = self._estimate(R, n_factors)
        return np.clip(h_squared, 0.0, 1.0)

    @abstractmethod
    def _estimate(self, R: np.ndarray, n_factors: int | None = None) -> np.ndarray:
        """Helper method for estimating communality from correlation matrix."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return communality estimation method name."""
        pass

    @staticmethod
    def _abs_zerodiag(R: np.ndarray) -> np.ndarray:
        """Return `R` with absolute values and zero-diagonal."""
        R = np.abs(R).copy()
        np.fill_diagonal(R, 0.0)
        return R