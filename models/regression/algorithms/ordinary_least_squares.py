import numpy as np
from scipy import stats
from ..interfaces import IOptimizationAlgorithm
from typing import Any, Dict

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
        self._XtX_inv_: np.ndarray | None = None
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
        # reset cache
        self._std_err_ = None
        self._df_ = None
        self._all_params_ = None
        self._XtX_inv_ = None

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

    def compute_confidence_intervals(self, X: np.ndarray, residuals: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Returns dictionary with t-stat, p-value and confidance intervals for coefficients.
        Returns: 
            {
                't_stats': np.ndarray (`float` for each coefficient + intercept),
                'p_values': np.ndarray (`float` for each coefficient + intercept),
                'CI': np.ndarray ([coef, std_err, ci_lower, ci_upper] for each coefficient + intercept)
            }
        """
        if self._std_err_ is None:
            self._compute_std_errors(X, residuals)
        
        t_val = stats.t.ppf((1 + alpha) / 2, self._df_)

        t_stats = self._all_params_ / self._std_err_
        p_vala = 2 * (1 - stats.t.cdf(np.abs(t_stats), self._df_))
        
        ci_lower = self._all_params_ - t_val * self._std_err_
        ci_upper = self._all_params_ + t_val * self._std_err_
        
        return {
            't_stats': t_stats,
            'p_values': p_vala,
            'CI': np.column_stack([self._all_params_, self._std_err_, ci_lower, ci_upper])
        }
    
    def compute_prediction_standard_errors(self, X_new: np.ndarray, X: np.ndarray, residuals: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Compute standard errors for prediction at X_new.
        Args:
            X_new (np.ndarray): New feature matrix (x0) of shape (n_samples_new, n_features).
            X (np.ndarray): Training feature matrix.
            residuals (np.ndarray): Residuals from the training data.
        Returns:
            Dict[str, np.ndarray]: {
                'SE_mean': np.ndarray (Std error for the mean response (Confidence Interval))
                'SE_ind': np.ndarray (Std error for the individual prediction (Prediction Interval))
            }
        """
        if not self.fitted:
            raise RuntimeError("Model not fitted yet")
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X_new.ndim == 1:
            X_new = X_new.reshape(-1, 1)
        if self._XtX_inv_ is None or self._df_ is None:
            self._compute_std_errors(X, residuals)
        
        MSE = np.sum(residuals ** 2) / self._df_
        
        # add intercept
        X_new_ext = np.column_stack([X_new, np.ones(X_new.shape[0])])

        var_mean = np.array([
            MSE * (x_ext @ self.XtX_inv @ x_ext.T) for x_ext in X_new_ext
        ])
        SE_mean = np.sqrt(var_mean)
        var_ind = var_mean + MSE
        SE_ind = np.sqrt(var_ind)
        
        return {
            'SE_mean': SE_mean,
            'SE_ind': SE_ind,
        }
    
    def compute_model_sagnificance(self, X: np.ndarray, y: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Returns dictionary with F-stat, p-value and conclusion of significance for model.
        Returns: 
            {
                'stat': {'name': 'F_stat', 'val': float},
                'p_value': float,
            }
        """
        if not self.fitted:
            raise RuntimeError("Model not fitted yet")
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        
        n_samples, n_features = X.shape
        
        y_pred = self.predict(X)
        residuals = y - y_pred
        df_residual = n_samples - n_features - 1
        y_mean = np.mean(y)

        SST = np.sum((y - y_mean) ** 2)
        SSR = np.sum(residuals ** 2)
        SSE = SST - SSR
        
        df_model = n_features
        
        MSE_model = SSE / df_model
        MSE_residual = SSR / df_residual
        
        # F-statistic
        f_stat = MSE_model / MSE_residual
        # p-value
        p_value = 1 - stats.f.cdf(f_stat, df_model, df_residual)
        
        return {
            'stat': {'name': 'F_stat', 'val': f_stat},
            'p_value': p_value,
        }

    def _compute_std_errors(self, X: np.ndarray, residuals: np.ndarray) -> None:
        """
        Calculate and cache std errors
        """
        if X.ndim == 1: X = X.reshape(-1, 1)
        
        n_samples, n_features = X.shape
        X_ext = np.column_stack([X, np.ones(n_samples)])
        
        self._df_ = n_samples - n_features - 1
        
        MSE = np.sum(residuals ** 2) / self._df_
        
        try:
            self.XtX_inv = np.linalg.inv(X_ext.T @ X_ext)
        except np.linalg.LinAlgError:
            raise ValueError("Cannot compute confidence intervals: singular matrix")
        
        var_coef = np.diag(self.XtX_inv) * MSE
        self._std_err_ = np.sqrt(var_coef)
        
        self._all_params_ = np.concatenate([self.coef_, [self.intercept_]])

    @property
    def name(self) -> str:
        """Returns a name of optimization algorithm"""
        return "OLS"