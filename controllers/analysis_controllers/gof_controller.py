import pandas as pd
from typing import Optional, Dict, List
from models.stat_distributions.base import BaseDistribution
from models.gofs import BaseGOFTest


class GOFController:
    """
    Controller for managing and executing goodness-of-fit (GOF) tests.
    """
    def __init__(self, gof_tests: List[BaseGOFTest]):
        self._tests: Dict[str, BaseGOFTest] = {}
        self._register_tests(gof_tests)

    def _register_tests(self, gof_tests: List[BaseGOFTest]):
        """Register all available GOF tests."""
        for gof_test in gof_tests:
            self._tests[gof_test.name()] = gof_test

    def run_test(self, test_name: str, data: pd.Series|pd.DataFrame, dist: BaseDistribution, alpha: float) -> Optional[Dict]:
        """
        Run specific test by name and return result.
        Args:
            test_name: Name of the test to run ('ks', 'chi2', etc.)
            data: Sample data
            dist: Fitted distribution
            alpha: Significance level
        Returns:
            Dictionary with test results or None if test fails
        """
        try:
            if test_name not in self._tests:
                return None
            
            data_clean = data.dropna()
            if data_clean.empty:
                return None
                
            return self._tests[test_name].run(data_clean.values, dist, alpha=alpha)
        except Exception as e:
            print(f"Some troubles in GOFController: {e}")
            return None