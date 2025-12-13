from models.correlation_coeffs._significance_test_result import SignificanceTestResult
from abc import ABC, abstractmethod
import numpy as np

class ICorrelationCoefficient(ABC):
    EPSILON = 1e-11
    def __init__(self):
        self.r = None
        self.n = None
    
    @abstractmethod
    def name(self) -> str:
        """Return correlation method name."""
        pass

    @abstractmethod
    def fit(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute correlation coefficient."""
        pass

    @abstractmethod
    def significance_test(self, alpha: float = 0.05) -> SignificanceTestResult:
        """Test significance of correlation coefficient."""
        pass

    @abstractmethod
    def _interval(self, alpha: float = 0.05) -> tuple[float, float]:
        """Compute confidence interval for the correlation."""
        pass