from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
from utils.helpers import validate_feature_names
from models.regression.interfaces import IRegression


class RegressionController:
    """
    Main controller class for regression tasks.
    Provides a unified interface for various regression models.
    """
    def __init__(self, regression_models: List[IRegression]):
        self._models: Dict[str, IRegression] = {}
        self._current_model: IRegression | None = None
        self._register_models(regression_models)

    def _register_models(self, regression_models: List[IRegression]):
        for regression in regression_models:
            self._models[regression.name] = regression

    @property
    def regression_models(self) -> List[str]:
        return list(self._models.keys())

    @property
    def current_features(self) -> list[str]:
        """Return feature names of the currently fitted model."""
        if not self._current_model:
            return []
        return list(getattr(self._current_model, 'features_', []))

    @property
    def current_target(self) -> str | None:
        """Return target column name of the currently fitted model."""
        if not self._current_model:
            return None
        return getattr(self._current_model, 'target_', None)
    
    @property
    def current_residuals(self) -> np.ndarray:
        """Return residuals of the currently fitted model."""
        if not self._current_model or self._current_model.residuals_ is None:
            return np.array([])
        return self._current_model.residuals_

    @property
    def current_fitted_values(self) -> np.ndarray:
        """Return fitted values of the currently fitted model."""
        if not self._current_model or self._current_model.y_pred_ is None:
            return np.array([])
        return self._current_model.y_pred_

    def fit(self, model_name: str, X_df: pd.DataFrame, y_series: pd.Series) -> None:
        """Train selected model on DataFrame."""
        if model_name not in self._models:
            raise ValueError(f"Unknown model: {model_name}")

        self._current_model = self._models[model_name]

        X = X_df.to_numpy(dtype=float)
        y = y_series.to_numpy(dtype=float)
        
        # add feature names if its valid
        feature_names = list(X_df.columns)
        if validate_feature_names(feature_names):
            self._current_model.features_ = list(feature_names)
        self._current_model.target_ = y_series.name

        self._current_model.fit(X, y)

    def predict(self, X_df: pd.DataFrame) -> pd.Series:
        """Returns prediction for X"""
        if not self._current_model:
            raise RuntimeError("Model not trained yet")
        preds = self._current_model.predict(X_df.to_numpy(dtype=float))
        return pd.Series(preds, name="prediction")

    def summary(self) -> Dict[str, Any]:
        """Returns model's summary (coefficients, intercept, equation, metrics, etc.)"""
        if not self._current_model:
            return {}
        summary = self._current_model.summary()
        return summary

    def confidence_intervals(self, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Returns dictionary with t-stat, p-value and confidance intervals for coefficients.
        Returns: 
            {
                'CI': pd.DatFrame,
                't_stats': pd.Series,
                'p_values': pd.Series,
                'significant': pd.Series,
            }
        """
        if not self._current_model:
            raise RuntimeError("Model not trained yet")

        ci_result = self._current_model.confidence_intervals(alpha)
        if ci_result is None:
            return
        
        df_ci = pd.DataFrame(ci_result['CI'], columns=["variable", "coef", "std_err", "ci_lower", "ci_upper"])
        t_stats = pd.Series(ci_result['t_stats'])
        p_values = pd.Series(ci_result['p_values'])

        return {
            'CI': df_ci,
            't_stats': t_stats,
            'p_values': p_values,
            'significant': p_values < alpha,
        }
    
    def predict_intervals(self, X_df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Tuple[float, float]]:
        """
        Returns confidence and prediction intervals for X.
        Returns:
            Dict[str, Tuple[float, float]]: {
                'CI_mean': (lower_bound, upper_bound) for the Confidence Interval.
                'CI_ind': (lower_bound, upper_bound) for the Prediction Interval.}
        """
        if not self._current_model:
            raise RuntimeError("Model not trained yet")
        X_new = X_df.to_numpy(dtype=float)
        pred_intrv = self._current_model.predict_intervals(X_new, alpha)
        return {
            key: (float(bounds[0]), float(bounds[1]))
            for key, bounds in pred_intrv.items()
        }
    
    def confidence_band(self, X_df: pd.DataFrame, alpha: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns CI_mean lower/upper bounds for each row in X_df.
        Used for drawing confidence band on regression plot.
        """
        if not self._current_model:
            raise RuntimeError("Model not trained yet")
        lowers, uppers = [], []
        X_arr = X_df.to_numpy(dtype=float)
        for row in X_arr:
            result = self._current_model.predict_intervals(row.reshape(1, -1), alpha)
            ci = result.get('CI_mean', (np.nan, np.nan))
            lower = np.asarray(ci[0]).ravel()[0]
            upper = np.asarray(ci[1]).ravel()[0]
            lowers.append(lower)
            uppers.append(upper)
        return np.array(lowers), np.array(uppers)

    def predict_tolerance(self, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Computes variance estimation and its tolerance bounds.
        Args:
            alpha (float): Significance level (e.g., 0.05 for 95% interval).
        Returns:
            Dict[str, Any]: {
                "var": (float) variance estimation.
                'CI': (lower_bound, upper_bound) for the tolerance bounds.
            }
        """
        if not self._current_model:
            raise RuntimeError("Model not trained yet")

        tolerance = self._current_model.predict_tolerance(alpha)
        if tolerance is None:
            return
        
        return tolerance
    
    def model_significance(self, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Returns dictionary with stat, p-value and conclusion of significance for model.
        Returns: 
            {
                'stat': Dict[str, float|str] (contain 'name' and 'val'),
                'p_value': float,
                'significant': bool,
            }
        """
        if not self._current_model:
            raise RuntimeError("Model not trained yet")

        model_sagn = self._current_model.model_significance(alpha)
        if model_sagn is None:
            return
        
        return model_sagn
    
    def standardized_coefficients(self) -> Optional[Dict[str, Any]]:
        """
        Returns standardized (beta) coefficients for the current model.
        Returns None if model doesn't support standardization.
        """
        if not self._current_model:
            raise RuntimeError("Model not trained yet")
        return self._current_model.standardized_coefficients()