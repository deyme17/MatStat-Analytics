from ..interfaces import IRegression, IOptimizationAlgorithm
from typing import Dict, Any, Optional, List, Tuple
from itertools import combinations_with_replacement
from scipy import stats
import numpy as np

class PolynomialRegression(IRegression):
    """Polynomial regression model"""
    def __init__(self, algorithm: IOptimizationAlgorithm, degree: int = 2):
        self.algorithm: IOptimizationAlgorithm = algorithm
        self.degree: int = degree

        self.X_: np.ndarray | None = None
        self.X_poly_: np.ndarray | None = None  # transformed features
        self.y_: np.ndarray | None = None

        self.features_: List[str] | None = None
        self.coef_: np.ndarray | None = None
        self.intercept_: float | None = None

        self.y_pred_: np.ndarray | None = None
        self.residuals_: np.ndarray | None = None
        self.r_squared_: float | None = None
        self.r_squared_adj_:  float | None = None

        self._model_signif_cache_: Dict[str, Any] | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Train model on data
        Args:
            X (np.ndarray): Feature matrix (n_samples,) or (n_samples, 1) for univariate.
            y (np.ndarray): Target Vector.
        """
        if X.ndim == 1: X = X.reshape(-1, 1)
        
        self.X_ = X
        self.y_ = y
        
        # create polynomial features
        self.X_poly_ = self._transform(X)
        
        # fit
        self.algorithm.fit(self.X_poly_, y)
        params = self.algorithm.get_params()
        self.coef_ = params.get("coef", None)
        self.intercept_ = params.get("intercept", None)
        
        # feature names
        self._generate_feature_names(X.shape[1])
        
        self._evaluate_model()
        self._model_signif_cache_ = None

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Returns prediction for X
        Args:
            X (np.ndarray): New feature matrix of shape (n_samples_new, n_features).
        Returns:
            Prediction for X (np.ndarray)
        """
        if self.coef_ is None: raise RuntimeError("Model not fitted yet")
        if X.ndim == 1: X = X.reshape(-1, 1)
        # add polynomial features
        X_poly = self._transform(X)
        return self.algorithm.predict(X_poly)

    def summary(self) -> Dict[str, Any]:
        """
        Returns model's summary (coefficients, intercept, metrics, etc.)
        """
        if self.coef_ is None:
            raise RuntimeError("Model not fitted yet")
        equation = self._generate_equation()
        return {
            "features": self.features_,
            "coefficients": self.coef_,
            "intercept": self.intercept_,
            "equation": equation,
            "degree": self.degree,
            "metrics": {
                "R^2": self.r_squared_,
                "Adjusted R^2": self.r_squared_adj_,
                "MSE": float(np.mean(self.residuals_ ** 2)),
                "RSE": float(np.std(self.residuals_)),
            }
        }

    def confidence_intervals(self, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with t-stat, p-value and confidence intervals for coefficients.
        """
        ci_result = self.algorithm.compute_confidence_intervals(
            self.X_poly_, self.residuals_, alpha=alpha
        )
        variables = np.array(self.features_ + ["intercept"]).reshape(-1, 1)
        ci_result["CI"] = np.column_stack([variables, ci_result["CI"]])
        return ci_result
    
    def predict_intervals(self, X_new: np.ndarray, alpha: float = 0.05) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        """
        Computes Confidence and Prediction Intervals for X_new.
        """
        if self.coef_ is None or self.X_poly_ is None or self.residuals_ is None:
            raise RuntimeError("Model must be fitted and training data stored to compute intervals.")

        if X_new.ndim == 1:
            X_new = X_new.reshape(-1, 1)
        
        X_new_poly = self._transform(X_new)
        y_hat_new = self.algorithm.predict(X_new_poly)
        
        se_results = self.algorithm.compute_prediction_standard_errors(
            X_new_poly, self.X_poly_, self.residuals_
        )
        SE_mean = se_results['SE_mean']
        SE_ind = se_results['SE_ind']
        
        n_samples, n_features = self.X_poly_.shape
        df = n_samples - n_features - 1
        
        t_val = stats.t.ppf(1 - alpha / 2, df)
        
        margin_mean = t_val * SE_mean
        CI_mean_lower = y_hat_new - margin_mean
        CI_mean_upper = y_hat_new + margin_mean
        
        margin_ind = t_val * SE_ind
        CI_ind_lower = y_hat_new - margin_ind
        CI_ind_upper = y_hat_new + margin_ind
        
        return {
            'CI_mean': (CI_mean_lower, CI_mean_upper),
            'CI_ind': (CI_ind_lower, CI_ind_upper),
        }
    
    def model_significance(self, alpha: float = 0.05) -> Optional[Dict[str, Any]]:
        """
        Returns dictionary with F-stat, p-value and conclusion of significance for model.
        """
        if not self._model_signif_cache_:
            self._model_signif_cache_ = self.algorithm.compute_model_significance(self.X_poly_, self.y_)
        self._model_signif_cache_["significant"] = self._model_signif_cache_["p_value"] < alpha
        return self._model_signif_cache_

    @property
    def name(self) -> str:
        """Returns a name of regression type"""
        return f"Polynomial Regression (degree={self.degree}, {self.algorithm.name})"
    
    def _transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform features to polynomial features.
        For univariate: [x] -> [x, x^2, x^3, ..., x^degree]
        For multivariate: includes interaction terms
        """
        if X.shape[1] == 1:
            X_poly = np.column_stack([X ** i for i in range(1, self.degree + 1)])
        else:
            # interaction terms
            X_poly = self._polynomial_features(X)
        
        return X_poly
    
    def _polynomial_features(self, X: np.ndarray) -> np.ndarray:
        """
        Generate polynomial features for multivariate input.
        Includes interaction terms.
        """
        n_samples, n_features = X.shape
        features = []
        
        for d in range(1, self.degree + 1):
            for combo in combinations_with_replacement(range(n_features), d):
                feature = np.prod([X[:, i] for i in combo], axis=0)
                features.append(feature)
        
        return np.column_stack(features)
    
    def _generate_feature_names(self, n_original_features: int) -> None:
        """Generate names for polynomial features"""
        if n_original_features == 1:
            self.features_ = [f"x^{i}" for i in range(1, self.degree + 1)]
        else:
            # multivariate with interactions
            self.features_ = []
            for d in range(1, self.degree + 1):
                for combo in combinations_with_replacement(range(n_original_features), d):
                    if len(combo) == 1:
                        self.features_.append(f"x{combo[0]}")
                    else:
                        term = "*".join([f"x{i}" for i in combo])
                        self.features_.append(term)
    
    def _evaluate_model(self) -> None:
        """Evaluates model and saves statistic and metrics"""
        self.y_pred_ = self.algorithm.predict(self.X_poly_)
        self.residuals_ = self.y_ - self.y_pred_

        # r-squared
        RSS = np.sum(self.residuals_ ** 2)
        TSS = np.sum((self.y_ - np.mean(self.y_)) ** 2)
        self.r_squared_ = 1 - RSS / TSS if TSS > 0 else np.nan

        # adjusted r-squared
        n, p = self.X_poly_.shape
        if n > p + 1 and not np.isnan(self.r_squared_):
            self.r_squared_adj_ = 1 - (1 - self.r_squared_) * (n - 1) / (n - p - 1)
        else:
            self.r_squared_adj_ = np.nan

    def _generate_equation(self) -> str:
        """Generate the string representation of the model equation"""
        equation = "y = "
        if self.features_:
            terms = [f"{coef:.4f}·{feat}" for coef, feat in zip(self.coef_, self.features_)]
            equation += " + ".join(terms)
        if self.intercept_ is not None:
            equation += f" + {self.intercept_:.4f}"
        return equation