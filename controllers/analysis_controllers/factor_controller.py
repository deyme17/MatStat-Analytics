from typing import Any
import pandas as pd
import numpy as np
from utils.decorators import validate_fitted
from models.factor_analysis import PFM, PFMFittingResult

OK_RESULT = [PFMFittingResult.CONVERGED, 
             PFMFittingResult.OBJECTIVE_INCREASED]


class FactorController:
    """
    Main controller class for factor analysis.
    """
    def __init__(self, pfm: PFM):
        self.pfm: PFM = pfm
        self._feature_names: list[str] = []

    def fit_transform(self, X_df: pd.DataFrame, h2_estimator_name: str, n_factors: int | None = None) -> pd.DataFrame:
        """
        Fit the PFM model and estimate factor scores.
        Args:
            X_df: DataFrame of shape (n_samples, n_features).
            h2_estimator_name: Communality estimation method.
            n_factors: Number of factors to retain.
        Returns:
            DataFrame of factor scores (n_samples, n_factors).
        """
        self._feature_names = []
        X = X_df.to_numpy(dtype=np.float64)
        X_transformed = self.pfm.fit_transform(X, h2_estimator_name, n_factors=n_factors)
        self._feature_names = list(X_df.columns)
        pfm_labels = [f"F_{i}" for i in range(1, X_transformed.shape[1] + 1)]
        return pd.DataFrame(X_transformed, columns=pfm_labels, index=X_df.index)

    @validate_fitted
    def get_iteration(self, idx: int) -> dict[str, Any]:
        """
        Labeled results of one accepted iteration.
        Args:
            idx: index in history (0-based).
        Returns:
            dict with keys: iter (int), f (float), R_h, A (DataFrames), h2 (Series).
        """
        h = self.pfm.history[idx]
        feats, factors = self._feature_names, self._factor_labels()
        return {
            "iter": h["iter"],
            "f": h["f"],
            "R_h": pd.DataFrame(h["Rh"], index=feats, columns=feats),
            "A": pd.DataFrame(h["A"], index=feats, columns=factors),
            "h2": pd.Series(h["h2"], index=feats),
        }
    
    @validate_fitted
    def get_results(self) -> dict[str, Any]:
        """
        Returns dict with results of the last fit with keys:
            - estimator: name of the initial h2 estimator.
            - R: correlation matrix (DataFrame, n x n).
            - R_h: final reduced correlation matrix (DataFrame, n x n).
            - A: factor loading matrix (DataFrame, n x n_factors).
            - h2: final communalities (Series, n).
            - h2_init: initial communalities (Series, n).
            - n_factors: factors kept.
            - n_iter:  accepted iterations.
            - f: final objective.
            - f_first: objective after the first pass.
            - result: FittingResult (convergence status).
            - ok: si fitting sucessful (bool).
        """
        feats, factors = self._feature_names, self._factor_labels()
        return {
            "estimator": self.pfm.h2_estimator_name_,
            "R": pd.DataFrame(self.pfm.correlation_matrix_, index=feats, columns=feats),
            "R_h": pd.DataFrame(self.pfm.reduction_matrix_, index=feats, columns=feats),
            "A": pd.DataFrame(self.pfm.loadings_, index=feats, columns=factors),
            "h2": pd.Series(self.pfm.communality_, index=feats),
            "h2_init": pd.Series(self.pfm.initial_communality_, index=feats),
            "n_factors": self.pfm.n_factors_,
            "n_iter": self.pfm.n_iter_,
            "f": self.pfm.objective_,
            "f_first": self.pfm.history[0]["f"],
            "result": self.pfm.fitting_result,
            "ok": self.pfm.fitting_result in OK_RESULT,
        }

    @validate_fitted
    def get_statistics(self) -> dict[str, Any]:
        """
        Returns dict of statistics of the last fit with keys:
            - uniqueness: unique variance d^2 = 1 - h^2 per feature (Series, n).
            - factor_var_contributions: V_v = Σ_k a^2_kv per factor (Series, n_factors).
            - factor_var_share: V_v / n_features, share of total variance (Series, n_factors).
            - cumulative_var_share: cumulative sum of factor_var_share (Series, n_factors).
            - total_variance: V = Σ V_v, variance explained by all common factors (float).
            - total_variance_share: V / n_features (float).
        """
        features, factors = self._feature_names, self._factor_labels()
        n_features = len(features)
        factor_vars = pd.Series(self.pfm.factor_var_contributions_, index=factors)
        share = factor_vars / n_features
        return {
            "uniqueness": pd.Series(self.pfm.uniqueness_, index=features),
            "factor_var_contributions": factor_vars,
            "factor_var_share": share,
            "cumulative_var_share": share.cumsum(),
            "total_variance": self.pfm.total_variance_,
            "total_variance_share": self.pfm.total_variance_ / n_features,
        }

    def get_h2_estimators_names(self) -> list[str]:
        """Return list of names of available h2 estimators."""
        return self.pfm.get_h2_estimators_names()

    def _factor_labels(self) -> list[str]:
        """Retirn new factor-labels ({F_i, i=1,n_factors})."""
        return [f"F_{i}" for i in range(1, self.pfm.n_factors_ + 1)]

    def clear(self) -> None:
        """Clears controller state."""
        self.pfm.clear_state()
        self._feature_names = []