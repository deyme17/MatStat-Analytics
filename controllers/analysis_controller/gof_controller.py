from models.gofs import gof_tests
import numpy as np
import pandas as pd
from typing import Optional
from models.stat_distributions.stat_distribution import StatisticalDistribution

class GOFController:
    """
    Controller for managing and executing goodness-of-fit (GOF) tests.
    """
    def __init__(self):
        self._tests = {}
        self._register_tests()

    def _register_tests(self):
        """Register all available GOF tests."""
        for gof_test in gof_tests:
            test_instance = gof_test()
            self._tests[test_instance.name()] = test_instance

    def run_test(self, test_name: str, data: pd.Series, dist: StatisticalDistribution, alpha: float) -> Optional[dict]:
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
        except Exception:
            return None

    def run_all_tests(self, data: pd.Series, dist: StatisticalDistribution, **kwargs) -> dict:
        """
        Run all registered GOF tests on given data and distribution.
        Args:
            data: Input data
            dist: Fitted StatisticalDistribution object
            kwargs: Optional parameters passed to each test
        Returns:
            Dictionary with test results by test name
        """
        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        results = {}
        for name, test in self._tests.items():
            try:
                results[name] = test.run(data_clean.values, dist, **kwargs)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results