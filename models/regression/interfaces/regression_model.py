from typing import Dict, Any, Optional, List, Tuple
from abc import ABC, abstractmethod
import numpy as np

class IRegression(ABC):
    """Base interface for regression models"""
    features_: List[str] | None
    coef_: np.ndarray | None
    intercept_: float | None

    y_pred_: np.ndarray | None
    residuals_: np.ndarray | None

    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Train model on data
        Args:
            X (np.ndarray): Feature matrix.
            y (np.ndarray): Target Vector.
        """
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Returns prediction for X
        Args:
            X (np.ndarray): New feature matrix of shape (n_samples_new, n_features).
        Returns:
            Prediction for X (np.ndarray)
        """
        pass

    @abstractmethod
    def summary(self) -> Dict[str, Any]:
        """
        Returns model's summary (coefficients, intercept, metrics, etc.)
        Example: {
            "features": list[str],
            "coefficients": np.ndarray,
            "equation": str
            "intercept": float,
            "metrics": dict[str, float],
        }
        """
        pass

    @abstractmethod
    def confidence_intervals(self, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with t-stat, p-value and confidance intervals for coefficients.
        Args:
            alpha (float): Significance level (e.g., 0.05 for 95% interval).
        Returns: 
            {   
                't_stats': np.ndarray (`float` for each coefficient + intercept),
                'p_values': np.ndarray (`float` for each coefficient + intercept),
                'CI': np.ndarray ([variable, coef, std_err, ci_lower, ci_upper] for each coefficient + intercept)
            }
        """
        pass
    
    @abstractmethod
    def predict_intervals(self, X_new: np.ndarray, alpha: float = 0.05) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        """
        Computes Confidence and Prediction Intervals for X_new.
        Args:
            X_new (np.ndarray): New feature matrix (x0) of shape (n_samples_new, n_features).
            alpha (float): Significance level (e.g., 0.05 for 95% interval).
        Returns:
            Dict[str, Tuple[np.ndarray, np.ndarray]]: {
                'CI_mean': (lower_bound, upper_bound) for the Confidence Interval.
                'CI_ind': (lower_bound, upper_bound) for the Prediction Interval.
            }
        """
        pass
    
    @abstractmethod
    def model_significance(self, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with stat, p-value and conclusion of significance for model.
        Args:
            alpha (float): Significance level (e.g., 0.05 for 95% interval).
        Returns: 
            {
                'stat': Dict[str, float|str] (contain 'name' and 'val'),
                'p_value': float,
                'significant': bool,
            }
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns a name of regression type"""
        pass

    @abstractmethod
    def _generate_feature_names(self, n_original_features: int) -> None:
        """Generate names for model features"""
        pass
    
    def _generate_equation(self) -> str:
        """Generate the string representation of the model equation"""
        equation = "y = "
        if self.features_ and self.coef_.size > 0:
            terms = [f"{coef:.4f}·{feat}" for coef, feat in zip(self.coef_, self.features_)]
            equation += " + ".join(terms)
        if self.intercept_ is not None:
            equation += f" + {self.intercept_:.4f}"
        return equation