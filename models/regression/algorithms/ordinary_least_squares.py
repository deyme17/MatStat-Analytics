import numpy as np
from scipy import stats
from ..interfaces import IOptimizationAlgorithm

class OLS(IOptimizationAlgorithm):
    """
    Ordinary Least Squares (OLS) regression class.
    """
    def __init__(self):
        self.coef_: np.ndarray | None = None
        self.intercept_: float | None = None
        self.fitted: bool = False

        self._std_err_: np.ndarray | None = None
        self._df_: int | None = None
        self._all_params_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Fit the OLS model to the provided data.
        Args:
            X (np.ndarray): Feature matrix of shape (n_samples,) or (n_samples, n_features).
            y (np.ndarray): Target vector of shape (n_samples,).
        """
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of samples")

        # add intercept column
        X_ext = np.column_stack([X, np.ones(X.shape[0])])

        # compute OLS coefficients
        try:
            beta = np.linalg.inv(X_ext.T @ X_ext) @ X_ext.T @ y
        except np.linalg.LinAlgError:
            raise ValueError("Design matrix is singular; cannot compute inverse.")

        self.coef_ = beta[:-1]
        self.intercept_ = beta[-1]
        self.fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict target values using the fitted OLS model.
        Args:
            X (np.ndarray): Feature matrix of shape (n_samples,) or (n_samples, n_features).
        Returns:
            np.ndarray: Predicted values of shape (n_samples,).
        """
        if not self.fitted:
            raise RuntimeError("Model not fitted yet")
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        return X @ self.coef_ + self.intercept_

    def get_params(self) -> dict:
        """
        Retrieve the model parameters.
        Returns:
            dict: {
                "coef": np.ndarray,
                "intercept": float
            }
        """
        if not self.fitted: raise RuntimeError("Model not fitted yet")
        return {"coef": self.coef_, "intercept": self.intercept_}

    def compute_confidence_intervals(self, X: np.ndarray, residuals: np.ndarray, alpha: float = 0.95) -> np.ndarray:
        """
        Computes and returns confidance intervals for coefficients for OLS in format:
            [coef, std_err, ci_lower, ci_upper] for each coefficient + intercept
        """
        if self._std_err_ is None:
            self._compute_std_errors(X, residuals)
        
        t_val = stats.t.ppf((1 + alpha) / 2, self._df_)
        
        ci_lower = self._all_params_ - t_val * self._std_err_
        ci_upper = self._all_params_ + t_val * self._std_err_
        
        return np.column_stack([self._all_params_, self._std_err_, ci_lower, ci_upper])

    def _compute_std_errors(self, X: np.ndarray, residuals: np.ndarray) -> None:
        """
        Calculate and cache std errors
        """
        if X.ndim == 1: X = X.reshape(-1, 1)
        
        n_samples, n_features = X.shape
        X_ext = np.column_stack([X, np.ones(n_samples)])
        
        self._df_ = n_samples - n_features - 1
        
        mse = np.sum(residuals ** 2) / self._df_
        
        try:
            XtX_inv = np.linalg.inv(X_ext.T @ X_ext)
        except np.linalg.LinAlgError:
            raise ValueError("Cannot compute confidence intervals: singular matrix")
        
        var_coef = np.diag(XtX_inv) * mse
        self._std_err_ = np.sqrt(var_coef)
        
        self._all_params_ = np.concatenate([self.coef_, [self.intercept_]])

    @property
    def name(self) -> str:
        """Returns a name of optimization algorithm"""
        return "OLS"