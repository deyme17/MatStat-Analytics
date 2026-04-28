from typing import Tuple, Optional
from scipy import linalg
import numpy as np



class PCA:
    """Principal Component Analysis model."""
    def __init__(self):
        self.eigenvalues: Optional[np.ndarray] = None
        self.eigenvectors: Optional[np.ndarray] = None
        self.components_: Optional[np.ndarray] = None
        self.evr_: Optional[np.ndarray] = None
        self.mean_: Optional[np.ndarray] = None
        self.fitted: bool = False

    def fit(self, X: np.ndarray) -> None:
        """
        Fit the PCA model to the data.\n
        This method computes the principal components from the X matrix,
        sorts them by eigenvalues, and stores the results in the instance attributes.
        Args:
            X (np.ndarray): Data of shape (n_samples, n_features).
        """
        self.clear_state()
        self.X_orig_ = X
        self._calculate_pc(X)
        self._sort_pc()
        self.fitted = True

    def _calculate_pc(self, X: np.ndarray) -> None:
        """Calculates eigenvectors and eigenvalues."""
        # normalize
        self.mean_ = X.mean(axis=0)
        X_norm = X - self.mean_
        # cov matrix
        cov_matrix = np.cov(X_norm, rowvar=False)
        # eigendecomposition
        self.eigenvalues, self.eigenvectors = linalg.eigh(cov_matrix)

    def _sort_pc(self) -> None:
        """Sort eigenvectors by its eigenvalues"""
        if self.eigenvalues is None or self.eigenvectors is None:
            raise Exception("[ERROR] Eigendecomposition is not performed.")
        sort_idx = np.argsort(self.eigenvalues, axis=0)[::-1]
        self.eigenvalues = self.eigenvalues[sort_idx]
        self.eigenvectors = self.eigenvectors[:, sort_idx]

    def transform(self, X: np.ndarray,
                  n_components: Optional[int] = None,
                  ev_threshold: Optional[float] = None) -> np.ndarray:
        """
        Tranform data using PCA model.
        Args:
            X (np.ndarray): Data of shape (n_samples, n_features).
            n_components (int|None): Number of principal components.
            ev_threshold (float|None): Explained variance threshold,
                    that is used for principal components selection.
        Returns:
            np.ndarray: Transformed data of shape (n_samples, n_components).
        Note:
            If n_components is defined - ev_threshold is not used.
        """
        if not self.fitted:
            raise Exception("[ERROR] PCA model is not fitted yet.")
        
        # select components
        if n_components is not None:
            k = n_components
        elif ev_threshold is not None:
            k = self._select_n_components_by_ev(ev_threshold)
        else:
            k = self.eigenvectors.shape[1]

        self.components_ = self.eigenvectors[:, :k]
        return (X - self.mean_) @ self.components_

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Apply inverse PCA transform to data.
        Args:
            X (np.ndarray): Data of shape (n_samples, n_components).
        Returns:
            np.ndarray: Reconstructed data of shape (n_samples, n_features).
        """
        if not self.fitted:
            raise Exception("[ERROR] PCA model is not fitted yet.")
        return X @ self.components_.T + self.mean_

    def fit_transform(self, X: np.ndarray,
                      n_components: Optional[int] = None,
                      ev_threshold: Optional[float] = None) -> np.ndarray:
        """
        Tranform data using PCA model.
        Args:
            X (np.ndarray): Data of shape (n_samples, n_features).
            n_components (int|None): Number of principal components.
            ev_threshold (float|None): Explained variance threshold,
                    that is used for principal components selection.
        Returns:
            np.ndarray: Transformed data of shape (n_samples, n_components).
        """
        self.fit(X)
        return self.transform(X, n_components, ev_threshold)
    
    def _select_n_components_by_ev(self, threshold: float = 0.90) -> int:
        """Select n_components by Explained Variance threshold."""
        if self.eigenvalues is None:
            raise Exception("[ERROR] Eigendecomposition is not performed.")
        total_variance = np.sum(self.eigenvalues)
        explained_variance = 0.0
        for i, eig_val in enumerate(self.eigenvalues):
            explained_variance += eig_val / total_variance
            if explained_variance >= threshold:
                return i + 1
    
    def get_explained_variance(self) -> Tuple[float, np.ndarray]:
        """Return: (Explained Variance, Explained Variance ratio for each component)."""
        total_variance = np.sum(self.eigenvalues)
        evr = self.eigenvalues / total_variance
        if self.components_ is not None:
            k = self.components_.shape[1]
            explained_variance = np.sum(self.eigenvalues[:k])
            return explained_variance, evr[:k]
        else:
            explained_variance = np.sum(self.eigenvalues)
            return explained_variance, evr
    
    def clear_state(self) -> None:
        """Clear PCA model state."""
        self.eigenvalues = None
        self.eigenvectors = None
        self.components_ = None
        self.evr_ = None
        self.mean_ = None
        self.fitted = False