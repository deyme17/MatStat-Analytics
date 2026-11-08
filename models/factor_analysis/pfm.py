from .communality.base import BaseCommunalityEstimator
from enum import Enum
import numpy as np



class PFMFittingResult(Enum):
    NOT_FITTED = "Not fitted"
    CONVERGED = "Converged"
    OBJECTIVE_INCREASED = "Objective increased"
    COMMUNALITY_EXCEEDED = "Communality exceeded"
    MAX_ITER = "Max iterations exceeded"


class PFM:
    """Principal Factor Method (iterative exploratory factor analysis)."""
    def __init__(self, 
                 h2_estimators: list[BaseCommunalityEstimator],
                 max_iter: int = 100,
                 eps: float = 1e-8,
                 h2_tol: float = 1e-8):
        """
        Args:
            h2_estimators: list of communality estimation methods.
            max_iter: Iteration limit.
            eps: Stop when squared difference of communalities <= eps.
            h2_tol: Tolerance threshold for Heywood cases (h^2 > 1.0 + h2_tol).
        """
        self.h2_estimators: dict[str, BaseCommunalityEstimator] = {}
        self._register_h2_estimators(h2_estimators)
        self.max_iter = max_iter
        self.eps = eps
        self.h2_tol = h2_tol
        self.clear_state()

    def clear_state(self) -> None:
        """Clear PFM model state."""
        self.X_orig_: np.ndarray | None = None
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None
        self.correlation_matrix_: np.ndarray | None = None
        self.reduction_matrix_: np.ndarray | None = None
        self.eigenvalues_: np.ndarray | None = None
        self.loadings_: np.ndarray | None = None
        self.communality_: np.ndarray | None = None
        self.h2_estimator_name_: str | None  = None
        self.initial_communality_: np.ndarray | None = None
        self.n_factors_: int | None = None
        self.n_iter_: int | None = None
        self.objective_: float | None = None
        self.history: list[dict] = []
        self._R_inv_A: np.ndarray | None = None
        self.fitting_result: PFMFittingResult = PFMFittingResult.NOT_FITTED

    def _register_h2_estimators(self, methods: list[BaseCommunalityEstimator]) -> None:
        for method in methods:
            self.h2_estimators[method.name()] = method

    @property
    def uniqueness_(self) -> np.ndarray | None:
        return None if self.communality_ is None else 1. - self.communality_

    @property
    def factor_var_contributions_(self) -> np.ndarray | None:
        return (self.loadings_**2).sum(axis=0) if self.loadings_ is not None else None

    @property
    def fitted(self) -> bool:
        return (self.fitting_result != PFMFittingResult.NOT_FITTED and 
                self.loadings_ is not None)

    # === api ===

    def fit(self,
            X: np.ndarray, 
            h2_estimator_name: str | None = None,
            n_factors: int | None = None) -> None:
        """
        Fit the PFM model by iteratively estimating communalities and factor loadings.
        Args:
            X: Input data of shape (n_samples, n_features).
            h2_estimator_name: Communality estimation method.
            n_factors: Number of factors to retain.
        """
        try:
            self.clear_state()
            self.X_orig_ = X

            # n features
            n = X.shape[1]
            if n < 3:
                raise ValueError("Factor analysis requires at least 3 features.")
            if X.shape[0] <= n:
                raise ValueError("Number of samples must exceed number of features.")
            if not np.isfinite(X).all():
                raise ValueError("Data contains NaN or infinite values.")

            # mean, std
            mean = X.mean(axis=0)
            std = X.std(axis=0, ddof=1)
            if np.any(std == 0):
                raise ValueError("Constant feature found (zero variance).")
            self.mean_, self.std_ = mean, std

            # correlation matrix
            R = np.corrcoef(X, rowvar=False)
            self.correlation_matrix_ = R

            # n factors
            w = n_factors if n_factors is not None else self._kaiser_criterion(R)
            if not 1 <= w < n:
                raise ValueError(f"n_factors must be in [1, {n - 1}], got {w}.")
            self.n_factors_ = w

            # init communality
            h2 = self._init_communality(R, w, h2_estimator_name)

            # optimization
            f = f_prev = np.inf
            A = R_h = None
            eigenvals = None
            self.fitting_result = PFMFittingResult.MAX_ITER

            for i in range(1, self.max_iter + 1):
                A_new, h2_new, eigenvals_new, R_h_new, f_new = self._optimization_step(R, h2, w)
                
                if np.any(h2_new > 1.0 + self.h2_tol):
                    if A is None:
                        h2 = np.minimum(h2_new, 1.0)
                        continue
                    self.fitting_result = PFMFittingResult.COMMUNALITY_EXCEEDED
                    break

                if f_new >= f_prev:
                    self.fitting_result = PFMFittingResult.OBJECTIVE_INCREASED
                    break

                A, eigenvals, R_h, f = A_new, eigenvals_new, R_h_new, f_new
                self.history.append({
                    "iter": i, 
                    "Rh": R_h.copy(), 
                    "A": A.copy(),
                    "h2": h2_new.copy(), 
                    "f": f
                })

                if ((h2_new - h2)**2).sum() <= self.eps:
                    self.fitting_result = PFMFittingResult.CONVERGED
                    break

                h2, f_prev = h2_new, f

            if A is None:
                raise ValueError("Factor model did not reach a valid solution.")

            self.n_iter_ = len(self.history)    
            A = self._fix_signs(A)
            self.reduction_matrix_ = R_h
            self.eigenvalues_ = eigenvals
            self.loadings_ = A
            self.communality_ = np.minimum((A**2).sum(axis=1), 1.0)
            self.objective_ = f
            self._R_inv_A = np.linalg.pinv(R) @ A
            
        except Exception:
            self.clear_state()
            raise

    def _init_communality(self, R: np.ndarray, w: int, h2_estimator_name: str | None = None) -> np.ndarray:
        """Estimate initial feature communalities (h^2) using a registered estimator."""
        if not self.h2_estimators:
            raise ValueError("No communality estimators registered.")
        
        h2_estimator_name = (h2_estimator_name if h2_estimator_name is not None
                             else self.get_h2_estimators_names()[0])

        h2_estimator = self.h2_estimators.get(h2_estimator_name)
        if h2_estimator is None:
            raise ValueError(f"Unknown communality estimation method: {h2_estimator_name}")
        
        h2 = h2_estimator.estimate(R, n_factors=w)
        self.initial_communality_ = h2.copy()
        self.h2_estimator_name_ = h2_estimator_name
        return h2
        
    def _optimization_step(self, R: np.ndarray, h2: np.ndarray, w: int) -> tuple[np.ndarray, np.ndarray,
                                                                                 np.ndarray, np.ndarray, float]:
        """
        One principal-factor pass: put h^2 on the diagonal of R, take top-w eigevalues.
        Returns (loadings A, new h^2, eigenvalues of R_h, R_h, objective f).
        """
        # R_h
        R_h = R.copy()
        np.fill_diagonal(R_h, h2)

        # eigenvalues
        eigenvalues, eigenvects = self._eigh_sorted(R_h)

        # A
        lambdas = np.clip(eigenvalues[:w], 0.0, None)
        A = eigenvects[:, :w] * np.sqrt(lambdas)

        # h2
        new_h2 = (A**2).sum(axis=1)

        # f
        R_res = R_h - (A @ A.T)
        np.fill_diagonal(R_res, 0.0)
        f = float((R_res**2).sum())

        return A, new_h2, eigenvalues, R_h, f

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Factor scores by the regression (Thomson) method: F = Z R⁻¹ A.
        Args:
            X: Input data of shape (n_samples, n_features).
        Returns:
            Factor scores of shape (n_samples, n_factors).
        """
        if not self.fitted:
            raise Exception("[ERROR] PFM model is not fitted on raw data yet.")
        Z = (X - self.mean_) / self.std_
        return Z @ self._R_inv_A

    def fit_transform(self,
                      X: np.ndarray, 
                      h2_estimator_name: str | None = None,
                      n_factors: int | None = None) -> np.ndarray:
        """
        Fit the PFM model and estimate factor scores.
        Args:
            X: Input data of shape (n_samples, n_features).
            h2_estimator_name: Communality estimation method.
            n_factors: Number of factors to retain.
        Returns:
            Factor scores of shape (n_samples, n_factors).
        """
        self.fit(X, h2_estimator_name, n_factors)
        return self.transform(X)

    def get_h2_estimators_names(self) -> list[str]:
        """Return list of names of available h2 estimators."""
        return list(self.h2_estimators.keys())

    # === helpers ===

    def _kaiser_criterion(self, R: np.ndarray) -> int:
        """Number of eigenvalues of R greater than 1 (lower-bound rule)."""
        eigenvals, _ = self._eigh_sorted(R)
        return max(1, int((eigenvals > 1.0).sum()))

    def _reduced_matrix_criterion(self, R_h: np.ndarray) -> int:
        """Number of eigenvalues of R_h greater than its mean."""
        eigenvals, _ = self._eigh_sorted(R_h)
        eigenvals_mean = eigenvals.mean()
        return max(1, int((eigenvals > eigenvals_mean).sum()))

    @staticmethod
    def _eigh_sorted(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        eigen_vals, eigen_vects = np.linalg.eigh(X)
        idx = np.argsort(eigen_vals)[::-1]
        return eigen_vals[idx], eigen_vects[:, idx]

    @staticmethod
    def _fix_signs(A: np.ndarray) -> np.ndarray:
        """Make the largest-|loading| of each factor positive."""
        A = A.copy()
        maxval_indices = np.argmax(np.abs(A), axis=0)
        indices = np.arange(A.shape[1])
        signs = np.sign(A[maxval_indices, indices])
        signs = np.where(signs==0, 1.0, signs)
        A *= signs
        return A