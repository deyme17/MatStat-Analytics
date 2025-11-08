from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class IRegression(ABC):
    """Base interface for regression models"""
    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train model on data"""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Returns prediction for X"""
        pass

    @abstractmethod
    def summury(self) -> dict[str, str|float|int]:
        """Returns model's summary (coefficients, intercept, metrics, etc.)"""
        pass

    @abstractmethod
    def confidance_intervals(self, alpha: float = 0.95) -> pd.DataFrame:
        """Returns confidance intervals for coeficients if possible"""
        pass