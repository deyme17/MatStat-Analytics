from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import numpy as np

class IOptimizationAlgorithm(ABC):
    """Base interface for optimization algorithms used in regression models."""
    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Fit the algorithm to training data.
        Args:
            X: Feature matrix of shape (n_samples, n_features)
            y: Target vector of shape (n_samples,)
        """
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict target values for given features.
        Args:
            X: Feature matrix of shape (n_samples, n_features)
        Returns:
            Predicted values of shape (n_samples,)
        """
        pass
    
    @abstractmethod
    def get_params(self) -> Dict:
        """
        Get fitted model parameters.
        Returns:
            Dictionary containing model parameters (e.g., coefficients, intercept)
        """
        pass
    
    @abstractmethod
    def compute_confidence_intervals(self, X: np.ndarray, residuals: np.ndarray, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
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

    @abstractmethod
    def compute_model_sagnificance(self, X: np.ndarray, y: np.ndarray, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with stat, p-value and conclusion of sagnificance for model.
        Returns: 
            {
                'stat': Dict[str, float|str] (contain 'name' and 'val'),
                'p_value': float,
            }
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns a name of optimization algorithm"""
        pass