from models.correlation_coeffs import corr_coefs
from models.correlation_coeffs import ICorrelationCoefficient
import pandas as pd
from typing import Optional

class CorrelationController:
    """
    Controller for calculating correlation coeficients and its confidance intervals.
    """
    def __init__(self):
        self._tests: dict[str, ICorrelationCoefficient] = {}
        self._register_tests()

    def _register_tests(self):
        """Register all available GOF tests."""
        for gof_test in corr_coefs:
            test_instance = gof_test()
            self._tests[test_instance.name()] = test_instance

    def calculate(self, test_name: str, x: pd.Series, y: pd.Series) -> float:
        """
        Compute correlation coefficient between x and y using the selected method.
        """
        if test_name not in self._tests:
            raise ValueError(f"Unknown correlation method: {test_name}")
        corr = self._tests[test_name]
        x, y = x.to_numpy(), y.to_numpy()
        return corr.fit(x, y)
        
    def get_confidence_interval(self, test_name: str, x: pd.Series, y: pd.Series,
                                confidence: float = 0.95) -> Optional[tuple[float, float]]:
        """
        Compute confidence interval for a given correlation method.
        """
        if test_name not in self._tests:
            raise ValueError(f"Unknown correlation method: {test_name}")
        corr = self._tests[test_name]
        x, y = x.to_numpy(), y.to_numpy()
        corr.fit(x, y)
        return corr.interval(confidence)