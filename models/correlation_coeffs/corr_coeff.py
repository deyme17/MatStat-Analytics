from abc import ABC, abstractmethod
import numpy as np

class ICorrelationCoefficient(ABC):
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
    def interval(self, confidence: float = 0.95) -> tuple[float, float]:
        """Compute confidence interval for the correlation."""
        pass