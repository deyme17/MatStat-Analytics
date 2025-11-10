from typing import List, Dict, Any
import pandas as pd
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

    def fit(self, model_name: str, X_df: pd.DataFrame, y_series: pd.Series) -> None:
        """Train selected model on DataFrame."""
        if model_name not in self._models:
            raise ValueError(f"Unknown model: {model_name}")

        self._current_model = self._models[model_name]

        X = X_df.to_numpy(dtype=float)
        y = y_series.to_numpy(dtype=float)

        self._current_model.features_ = list(X_df.columns)
        self._current_model.fit(X, y)

    def predict(self, X_df: pd.DataFrame) -> pd.Series:
        """Returns prediction for X"""
        if not self._current_model:
            raise RuntimeError("Model not trained yet")
        preds = self._current_model.predict(X_df.to_numpy(dtype=float))
        return pd.Series(preds, name="prediction")

    def summary(self) -> Dict[str, Any]:
        """Returns model's summary (coefficients, intercept, metrics, etc.)"""
        if not self._current_model:
            return {}
        summary = self._current_model.summary()
        return summary

    def confidence_intervals(self, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Returns dictionary with t-stat, p-value and confidance intervals for coefficients.
        Returns: 
            {
                't_stats': pd.Series,
                'p_values': pd.Series,
                'CI': pd.DatFrame
            }
        """
        if not self._current_model:
            raise RuntimeError("Model not trained yet")

        ci_result = self._current_model.confidence_intervals(alpha)
        if ci_result is None:
            return
        
        t_stats = pd.Series(ci_result['t_stats'])
        p_values = pd.Series(ci_result['p_values'])
        df_ci = pd.DataFrame(ci_result['CI'], columns=["variable", "coef", "std_err", "ci_lower", "ci_upper"])

        return {
            't_stats': t_stats,
            'p_values': p_values, 
            'CI': df_ci
        }

    @property
    def regression_models(self) -> List[str]:
        return list(self._models.keys())