from ..interfaces import IRegression, IOptimizationAlgorithm
from typing import Dict, Any, Optional, List
import numpy as np

class LinearRegression(IRegression):
    """Linear regression model"""
    def __init__(self, algorithm: IOptimizationAlgorithm):
        self.algorithm: IOptimizationAlgorithm = algorithm

        self.X_: np.ndarray | None = None
        self.y_: np.ndarray | None = None

        self.features_: List[str] | None = None
        self.coef_: np.ndarray | None = None
        self.intercept_: float | None = None

        self.y_pred_: np.ndarray | None = None
        self.residuals_: np.ndarray | None = None
        self.r_squared_: float | None = None
        self.r_squared_adj_:  float | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train model on data"""
        self.X_, self.y_ = X, y
        self.algorithm.fit(X, y)
        params = self.algorithm.get_params()
        self.coef_ = params.get("coef", None)
        self.intercept_ = params.get("intercept", None)
        self._evaluate_model()

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Returns prediction for X"""
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet")
        return self.algorithm.predict(X)

    def summary(self) -> Dict[str, Any]:
        """
        Returns model's summary (coefficients, intercept, metrics, etc.)
        Example: {
            "features": list[str],
            "coefficients": np.ndarray,
            "intercept": float,
            "metrics": {
                "R^2": float,
                "Adjusted R^2": float,
                "MSE": float,
                "RSE": float
                }
        }
        """
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet")
        return {
            "features": self.features_,
            "coefficients": self.coef_,
            "intercept": self.intercept_,
            "metrics": {
                "R^2": self.r_squared_,
                "Adjusted R^2": self.r_squared_adj_,
                "MSE": float(np.mean(self.residuals_ ** 2)),
                "RSE": float(np.std(self.residuals_)),
            }
        }

    def confidence_intervals(self, alpha: float = 0.95) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with t-stat, p-value and confidance intervals for coefficients.
        Returns: 
            {   
                't_stats': np.ndarray (`float` for each coefficient + intercept),
                'p_values': np.ndarray (`float` for each coefficient + intercept),
                'CI': np.ndarray ([variable, coef, std_err, ci_lower, ci_upper] for each coefficient + intercept)
            }
        """
        ci_result = self.algorithm.compute_confidence_intervals(
            self.X_, self.residuals_, alpha=alpha
        )
        variables = np.array(self.features_ + ["intercept"]).reshape(-1, 1)
        ci_result["CI"] = np.column_stack([variables, ci_result["CI"]])
        return ci_result

    @property
    def name(self) -> str:
        """Returns a name of regression type"""
        return f"Linear Regression ({self.algorithm.name})"
    
    def _evaluate_model(self) -> None:
        """Evaluates model and saves statistic and metrics"""
        self.y_pred_ = self.algorithm.predict(self.X_)
        self.residuals_ = self.y_ - self.y_pred_

        # r-squared
        RSS = np.sum(self.residuals_ ** 2)
        TSS = np.sum((self.y_ - np.mean(self.y_)) ** 2)
        self.r_squared_ = 1 - RSS / TSS if TSS > 0 else np.nan

        # adjusted r-squared
        n, p = self.X_.shape
        if n > p + 1 and not np.isnan(self.r_squared_):
            self.r_squared_adj_ = 1 - (1 - self.r_squared_) * (n - 1) / (n - p - 1)
        else:
            self.r_squared_adj_ = np.nan