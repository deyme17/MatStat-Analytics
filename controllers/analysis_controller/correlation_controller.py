from models.correlation_coeffs._significance_test_result import SignificanceTestResult
from models.correlation_coeffs import ICorrelationCoefficient
from typing import  List, Dict
import pandas as pd


class CorrelationController:
    """
    Controller for calculating correlation coeficients and its confidance intervals.
    """
    def __init__(self, corr_coeffs: List[type[ICorrelationCoefficient]]):
        self._corr_coeffs: Dict[str, ICorrelationCoefficient] = {}
        self._register_corr_coeffs(corr_coeffs)

    def _register_corr_coeffs(self, corr_coeffs: List[type[ICorrelationCoefficient]]):
        """Register all available GOF tests."""
        for corr_coeff in corr_coeffs:
            coeff_instance = corr_coeff()
            self._corr_coeffs[coeff_instance.name()] = coeff_instance

    def calculate(self, corr_name: str, x: pd.Series, y: pd.Series) -> float:
        """
        Compute correlation coefficient between x and y using the selected method.
        """
        if corr_name not in self._corr_coeffs:
            raise ValueError(f"Unknown correlation method: {corr_name}")
        corr = self._corr_coeffs[corr_name]
        x, y = x.to_numpy(), y.to_numpy()
        return corr.fit(x, y)

    def test_significance(self, corr_name: str, x: pd.Series, y: pd.Series,
                        alpha: float = 0.05) -> SignificanceTestResult:
        """
        Test significance of correlation coefficient and calculate confidance intervals.
        Returns:
            SignificanceTestResult
        """
        if corr_name not in self._corr_coeffs:
            raise ValueError(f"Unknown correlation method: {corr_name}")
        corr = self._corr_coeffs[corr_name]
        x, y = x.to_numpy(), y.to_numpy()
        corr.fit(x, y)
        return corr.significance_test(alpha)
    
    @property
    def corr_coeffs(self) -> List[str]:
        """Return list of available correlation coefficient names."""
        return list(self._corr_coeffs.keys())