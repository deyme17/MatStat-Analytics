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
    def get_params(self) -> dict:
        """
        Get fitted model parameters.
        Returns:
            Dictionary containing model parameters (e.g., coefficients, intercept)
        """
        pass
    
    @abstractmethod
    def compute_confidence_intervals(self, X: np.ndarray, y: np.ndarray, 
                                    residuals: np.ndarray, alpha: float = 0.95) -> np.ndarray | None:
        """
        Computes confidance intervals for coefficients (if possible) in format:
            [coef, std_err, ci_lower, ci_upper] for each coefficient + intercept
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns a name of optimization algorithm"""
        pass