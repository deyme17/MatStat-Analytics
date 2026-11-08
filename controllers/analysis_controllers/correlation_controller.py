from models.correlation_coeffs._significance_test_result import SignificanceTestResult
from models.correlation_coeffs import (
    BaseCorrelationCoefficient, MultipleCorrelation, PartialCorrelation
)
import pandas as pd


class CorrelationController:
    """
    Controller for calculating correlation coeficients and its confidance intervals.
    """
    def __init__(self, 
                 corr_coeffs: list[BaseCorrelationCoefficient],
                 partial_corr: PartialCorrelation,
                 multiple_corr: MultipleCorrelation):
        self._corr_coeffs: dict[str, BaseCorrelationCoefficient] = {}
        self._register_corr_coeffs(corr_coeffs)
        self._partial_corr = partial_corr
        self._multiple_corr = multiple_corr

    def _register_corr_coeffs(self, corr_coeffs: list[BaseCorrelationCoefficient]):
        """Register all available bivariate correlation coefficient tests."""
        for corr_coeff in corr_coeffs:
            self._corr_coeffs[corr_coeff.name()] = corr_coeff

    def calculate(self, corr_name: str, x: pd.Series, y: pd.Series) -> float:
        """
        Compute bivariate correlation coefficient between x and y using the selected method.
        """
        if corr_name not in self._corr_coeffs:
            raise ValueError(f"Unknown correlation method: {corr_name}")
        corr = self._corr_coeffs[corr_name]
        x, y = x.to_numpy(), y.to_numpy()
        return corr.fit(x, y)

    def test_significance(self, corr_name: str, x: pd.Series, y: pd.Series,
                          alpha: float = 0.05) -> SignificanceTestResult:
        """
        Test significance of bivariate correlation coefficient and calculate confidance intervals.
        Returns:
            SignificanceTestResult
        """
        if corr_name not in self._corr_coeffs:
            raise ValueError(f"Unknown correlation method: {corr_name}")
        corr = self._corr_coeffs[corr_name]
        x, y = x.to_numpy(), y.to_numpy()
        corr.fit(x, y)
        return corr.significance_test(alpha)
    
    def calculate_partial_correlation(self, x: pd.Series, y: pd.Series, controls: list[pd.Series]) -> float:
        """Compute partial correlation coefficient between x and y controlling for control variable."""
        x, y = x.to_numpy(), y.to_numpy()
        controls = [control.to_numpy() for control in controls]
        return self._partial_corr.fit(x, y, controls)
    
    def test_partial_correlation_significance(self, x: pd.Series, y: pd.Series, controls: list[pd.Series],
                                           alpha: float = 0.05) -> SignificanceTestResult:
        """Test significance of partial correlation coefficient and calculate confidance intervals."""
        x, y = x.to_numpy(), y.to_numpy()
        controls = [control.to_numpy() for control in controls]
        self._partial_corr.fit(x, y, controls)
        return self._partial_corr.significance_test(alpha)
    
    def calculate_multiple_correlation(self, y: pd.Series, predictors: list[pd.Series]) -> float:
        """Compute multiple correlation coefficient between all variables."""
        y = y.to_numpy()
        predictors = [p.to_numpy() for p in predictors]
        return self._multiple_corr.fit(y, predictors)
    
    def test_multiple_correlation_significance(self, y: pd.Series, predictors: list[pd.Series], alpha: float = 0.05) -> SignificanceTestResult:
        """Test significance of multiple correlation coefficient and calculate confidance intervals."""
        y = y.to_numpy()
        predictors = [p.to_numpy() for p in predictors]
        self._multiple_corr.fit(y, predictors)
        return self._multiple_corr.significance_test(alpha)
    
    @property
    def corr_coeffs(self) -> list[str]:
        """Return list of available correlation coefficient names (only bivariate)."""
        return list(self._corr_coeffs.keys())