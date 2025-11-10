import numpy as np

class SimpleLinearRegression:
    """
    Simple linear regression (OLS-based).
    """
    def __init__(self):
        self.coef_: float | None = None
        self.intercept_: float | None = None
        self.fitted: bool = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Fit model using closed-form OLS solution.
        Args:
            X (np.ndarray): feature array (n_samples,)
            y (np.ndarray): target array (n_samples,)
        """
        if X.ndim != 1:
            raise ValueError("X must be 1D array for simple OLS")
        if y.ndim != 1:
            raise ValueError("y must be 1D array")
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have same length")

        X_ext = np.column_stack([X, np.ones_like(X)])  # add intercept term
        beta = np.linalg.inv(X_ext.T @ X_ext) @ X_ext.T @ y

        self.coef_ = beta[0]
        self.intercept_ = beta[1]
        self.fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict target values.
        Args:
            X (np.ndarray): feature array (n_samples,)
        Returns:
            np.ndarray: predicted values
        """
        if not self.fitted:
            raise RuntimeError("Model not fitted yet")
        return self.coef_ * X + self.intercept_

    def get_params(self) -> dict:
        """
        Get trained model parameters.
        Returns: dict {
            "coef": float, 
            "intercept": float
        }
        """
        if not self.fitted:
            raise RuntimeError("Model not fitted yet")
        return {"coef": self.coef_, "intercept": self.intercept_}