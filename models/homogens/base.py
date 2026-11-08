from abc import ABC, abstractmethod
import numpy as np

class BaseHomogenTest(ABC):
    """Abstract base class for homogeneity tests."""
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, *samples: list[np.ndarray], alpha: float = 0.05, **kwargs) -> dict:
        pass