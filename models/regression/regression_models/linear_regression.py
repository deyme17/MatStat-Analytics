from ..interfaces import IRegression, IOptimizationAlgorithm
from typing import Dict, Any, Optional
import numpy as np

class LinearRegression(IRegression):
    """Linear regression model"""
    def __init__(self, algorithm: IOptimizationAlgorithm):
        self.algorithm: IOptimizationAlgorithm = algorithm

        self.X_: np.ndarray | None = None
        self.y_: np.ndarray | None = None
        self.coef_: np.ndarray | None = None
        self.intercept_: float | None = None

        self.y_pred_: np.ndarray | None = None
        self.residuals_: np.ndarray | None = None
        self.r_squared_: float | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train model on data"""
        self.X_, self.y_ = X, y
        self.algorithm.fit(X, y)
        params = self.algorithm.get_params()
        self.coef_ = params.get("coef", None)
        self.intercept_ = params.get("intercept", None)
        self._evaluate_model(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Returns prediction for X"""
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet")
        return self.algorithm.predict(X)

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
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet")
        return {
            "coefficients": self.coef_,
            "intercept": self.intercept_,
            "r_squared": self.r_squared_,
            "residual_std_error": float(np.std(self.residuals_)),
        }

    def confidence_intervals(self, alpha: float = 0.95) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with t-value, p-value and confidance intervals for coefficients.
        Returns: 
            {
                't_value': float,
                'p_values': np.ndarray (`float` for each coefficient + intercept)
                'CI': np.ndarray ([coef, std_err, ci_lower, ci_upper] for each coefficient + intercept)
            }
        """
        return self.algorithm.compute_confidence_intervals(
            self.X_, self.residuals_, alpha=alpha
        )

    @property
    def name(self) -> str:
        """Returns a name of regression type"""
        return f"Linear Regression ({self.algorithm.name})"
    
    def _evaluate_model(self) -> None:
        """Evaluates model and saves statistic and metrics"""
        self.y_pred_ = self.algorithm.predict(self.X_)
        self.residuals_ = self.y_ - self.y_pred_

        # r-squared
        ss_res = np.sum(self.residuals_ ** 2)
        ss_tot = np.sum((self.y_ - np.mean(self.y_)) ** 2)
        self.r_squared_ = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan