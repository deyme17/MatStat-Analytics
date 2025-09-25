from models.homogens import homogens_tests
import pandas as pd
from typing import Optional


class HomogenController:
    """
    Controller for managing and executing homogeneity tests.
    """
    def __init__(self):
        self._tests = {}
        self._register_tests()

    def _register_tests(self):
        """Register all available homogeneity tests."""
        for homogen_test in homogens_tests:
            test_instance = homogen_test()
            self._tests[test_instance.name()] = test_instance

    def run_test(self, test_name: str, samples: list[pd.Series], alpha: float = 0.05, is_independent: bool = False) -> Optional[dict]:
        """
        Run a homogeneity test for samples.
        Args:
            test_name: The name of the homogeneity test to run (must be registered in `_tests`).
            samples: Ssamples to test. Can be pandas Series or numpy arrays.
            alpha: Significance level for the statistical test.
            is_independent: True if the two samples are independent, False if paired/dependent.
        Returns:
            Dictionary with test results (statistic, p-value, decision), 
            or None if inputs are invalid or an error occurred.
        """
        if test_name not in self._tests: raise ValueError(f"Unknown test '{test_name}'. Available: {list(self._tests)}")
        try:
            clean_samples = []
            for data in samples:
                data = data.dropna().to_numpy()
                if len(data) == 0:
                    return None
                clean_samples.append(data)

            return self._tests[test_name].run(clean_samples, alpha, is_independent)
        except Exception as e:
           raise ValueError(e)