from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
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
    def summary(self) -> Dict[str, Any]:
        """
        Returns model's summary (coefficients, intercept, metrics, etc.)
        Example: {
            "coefficients": np.ndarray,
            "intercept": float,
            "r_squared": float,
            "residual_std_error": float,
        }
        """
        pass

    @abstractmethod
    def confidence_intervals(self, alpha: float = 0.95) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with t-stat, p-value and confidance intervals for coefficients.
        Returns: 
            {
                't_stats': np.ndarray (`float` for each coefficient + intercept),
                'p_values': np.ndarray (`float` for each coefficient + intercept),
                'CI': np.ndarray ([coef, std_err, ci_lower, ci_upper] for each coefficient + intercept)
            }
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns a name of regression type"""
        pass