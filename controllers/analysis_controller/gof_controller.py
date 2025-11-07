import pandas as pd
from typing import Optional, Dict, List
from models.stat_distributions.stat_distribution import StatisticalDistribution
from models.gofs import BaseGOFTest

class GOFController:
    """
    Controller for managing and executing goodness-of-fit (GOF) tests.
    """
    def __init__(self, gof_tests: List[type[BaseGOFTest]]):
        self._tests: Dict[str, BaseGOFTest] = {}
        self._register_tests(gof_tests)

    def _register_tests(self, gof_tests: List[type[BaseGOFTest]]):
        """Register all available GOF tests."""
        for gof_test in gof_tests:
            test_instance = gof_test()
            self._tests[test_instance.name()] = test_instance

    def run_test(self, test_name: str, data: pd.Series|pd.DataFrame, dist: StatisticalDistribution, alpha: float) -> Optional[Dict]:
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