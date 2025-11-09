from typing import List, Dict, Any
import pandas as pd
from models.regression.interfaces import IRegression


class RegressionController:
    """
    Main controller class for regression tasks.
    Provides a unified interface for various regression types.
    """
    def __init__(self, regression_types: List[IRegression]):
        self._regressions: Dict[str, IRegression] = {}
        self._current_model: IRegression | None = None
        self._feature_names: List[str] | None = None
        self._register_regressions(regression_types)

    def _register_regressions(self, regression_types: List[IRegression]):
        for regression in regression_types:
            self._regressions[regression.name] = regression

    def fit(self, model_name: str, X_df: pd.DataFrame, y_series: pd.Series) -> None:
        """Train selected model on DataFrame."""
        if model_name not in self._regressions:
            raise ValueError(f"Unknown model: {model_name}")

        self._feature_names = list(X_df.columns)
        self._current_model = self._regressions[model_name]

        X = X_df.to_numpy(dtype=float)
        y = y_series.to_numpy(dtype=float)

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
        summary["features"] = self._feature_names
        return summary

    def confidence_intervals(self, alpha: float = 0.05) -> pd.DataFrame:
        """Returns confidance intervals for coeficients if possible"""
        if not self._current_model:
            raise RuntimeError("Model not trained yet")
        if not self._feature_names:
            raise RuntimeError("No feature names stored")

        ci_matrix = self._current_model.confidence_intervals(alpha)
        df_ci = pd.DataFrame(ci_matrix, columns=["coef", "std_err", "ci_lower", "ci_upper"])
        df_ci.insert(0, "variable", self._feature_names + ["intercept"])
        return df_ci

    @property
    def regression_types(self) -> List[str]:
        return list(self._regressions.keys())