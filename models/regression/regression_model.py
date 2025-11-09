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
    def summary(self) -> dict[str, str|float|int]:
        """Returns model's summary (coefficients, intercept, metrics, etc.)"""
        pass

    @abstractmethod
    def confidence_intervals(self, alpha: float = 0.95) -> np.ndarray:
        """
        Returns confidance intervals for coefficients (if possible) in format:
            [coef, std_err, ci_lower, ci_upper] for each coefficient + intercept
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns a name of regression type"""
        pass