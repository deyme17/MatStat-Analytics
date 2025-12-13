from ..interfaces import IRegression, IOptimizationAlgorithm
from typing import Dict, Any, Optional, List, Tuple
from scipy import stats
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

        self._model_sagn_cache_: Dict[str, Any] | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Train model on data
        Args:
            X (np.ndarray): Feature matrix.
            y (np.ndarray): Target Vector.
        """
        self.X_, self.y_ = X, y
        self.algorithm.fit(X, y)
        params = self.algorithm.get_params()
        self.coef_ = params.get("coef", None)
        self.intercept_ = params.get("intercept", None)
        self._evaluate_model()
        self._model_sagn_cache_ = None

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Returns prediction for X
        Args:
            X (np.ndarray): New feature matrix of shape (n_samples_new, n_features).
        Returns:
            Prediction for X (np.ndarray)
        """
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
        equation = self._generate_equation()
        return {
            "features": self.features_,
            "coefficients": self.coef_,
            "intercept": self.intercept_,
            "equation": equation,
            "metrics": {
                "R^2": self.r_squared_,
                "Adjusted R^2": self.r_squared_adj_,
                "MSE": float(np.mean(self.residuals_ ** 2)),
                "RSE": float(np.std(self.residuals_)),
            }
        }

    def confidence_intervals(self, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with t-stat, p-value and confidance intervals for coefficients.
        Args:
            alpha (float): Significance level (e.g., 0.05 for 95% interval)
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
    
    def predict_intervals(self, X_new: np.ndarray, alpha: float = 0.05) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        """
        Computes Confidence and Prediction Intervals for X_new.
        Args:
            X_new (np.ndarray): New feature matrix.
            alpha (float): Significance level (e.g., 0.05 for 95% interval).
        Returns:
            Dict[str, Tuple[np.ndarray, np.ndarray]]: {
                'CI_mean': (lower_bound, upper_bound) for the Confidence Interval.
                'CI_ind': (lower_bound, upper_bound) for the Prediction Interval.
            }
        """
        if self.coef_ is None or self.X_ is None or self.residuals_ is None:
            raise RuntimeError("Model must be fitted and training data stored to compute intervals.")

        y_hat_new = self.predict(X_new)
        se_results = self.algorithm.compute_prediction_standard_errors(
            X_new, self.X_, self.residuals_
        )
        SE_mean = se_results['SE_mean']
        SE_ind = se_results['SE_ind']
        
        n_samples, n_features = self.X_.shape
        df = n_samples - n_features - 1
        
        t_val = stats.t.ppf(1 - alpha / 2, df)
        
        margin_mean = t_val * SE_mean
        CI_mean_lower = y_hat_new - margin_mean
        CI_mean_upper = y_hat_new + margin_mean
        
        margin_ind = t_val * SE_ind
        CI_ind_lower = y_hat_new - margin_ind
        CI_ind_upper = y_hat_new + margin_ind
        
        return {
            'CI_mean': (CI_mean_lower, CI_mean_upper),
            'CI_ind': (CI_ind_lower, CI_ind_upper),
        }
    
    def model_significance(self, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with F-stat, p-value and conclusion of significance for model.
        Args:
            alpha (float): Significance level (e.g., 0.05 for 95% interval).
        Returns: 
            {
                'stat': Dict[str, float|str] (contain 'name' and 'val'),
                'p_value': float,
                'significant': bool,
            }
        """
        if not self._model_sagn_cache_:
            self._model_sagn_cache_ = self.algorithm.compute_model_significance(self.X_, self.y_)
        self._model_sagn_cache_["significant"] = self._model_sagn_cache_["p_value"] < alpha
        return self._model_sagn_cache_

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

    def _generate_equation(self) -> str:
        """Generate the string representation of the model equation"""
        equation = "y = "
        if self.features_:
            terms = [f"{coef:.4f}·{feat}" for coef, feat in zip(self.coef_, self.features_)]
            equation += " + ".join(terms)
        if self.intercept_ is not None:
            equation += f" + {self.intercept_:.4f}"
        return equation