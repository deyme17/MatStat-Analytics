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

    def compute_confidence_intervals(self, X: np.ndarray, y: np.ndarray, 
                                    residuals: np.ndarray, alpha: float = 0.95) -> np.ndarray:
        """
        Computes and returns confidance intervals for coefficients for OLS in format:
            [coef, std_err, ci_lower, ci_upper] for each coefficient + intercept
        """
        if X.ndim == 1: X = X.reshape(-1, 1)
        
        n_samples, n_features = X.shape
        X_ext = np.column_stack([X, np.ones(n_samples)])
        
        df = n_samples - n_features - 1
        mse = np.sum(residuals ** 2) / df
        
        try:
            XtX_inv = np.linalg.inv(X_ext.T @ X_ext)
        except np.linalg.LinAlgError:
            raise ValueError("Cannot compute confidence intervals: singular matrix")
        
        var_coef = np.diag(XtX_inv) * mse
        std_err = np.sqrt(var_coef)
        
        t_val = stats.t.ppf((1 + alpha) / 2, df)
        
        all_params = np.concatenate([self.coef_, [self.intercept_]])
        
        ci_lower = all_params - t_val * std_err
        ci_upper = all_params + t_val * std_err
        
        return np.column_stack([all_params, std_err, ci_lower, ci_upper])

    @property
    def name(self) -> str:
        """Returns a name of optimization algorithm"""
        return "OLS"