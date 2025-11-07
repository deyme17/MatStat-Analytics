from models.correlation_coeffs import ICorrelationCoefficient
import pandas as pd
from typing import Optional

class CorrelationController:
    """
    Controller for calculating correlation coeficients and its confidance intervals.
    """
    def __init__(self, corr_coeffs: list[type[ICorrelationCoefficient]]):
        self._corr_coeffs: dict[str, ICorrelationCoefficient] = {}
        self._register_corr_coeffs(corr_coeffs)

    def _register_corr_coeffs(self, corr_coeffs: list[type[ICorrelationCoefficient]]):
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
        
    def get_confidence_interval(self, corr_name: str, x: pd.Series, y: pd.Series,
                                confidence: float = 0.95) -> Optional[tuple[float, float]]:
        """
        Compute confidence interval for a given correlation method.
        """
        if corr_name not in self._corr_coeffs:
            raise ValueError(f"Unknown correlation method: {corr_name}")
        corr = self._corr_coeffs[corr_name]
        x, y = x.to_numpy(), y.to_numpy()
        corr.fit(x, y)
        return corr.interval(confidence)