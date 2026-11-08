from models.homogens import BaseHomogenTest
import pandas as pd


class HomogenController:
    """
    Controller for managing and executing homogeneity tests.
    """
    def __init__(self, homogen_tests: list[BaseHomogenTest]):
        self._tests: dict[str, BaseHomogenTest] = {}
        self._register_tests(homogen_tests)

    def _register_tests(self, homogen_tests: list[BaseHomogenTest]):
        """Register all available homogeneity tests."""
        for homogen_test in homogen_tests:
            self._tests[homogen_test.name()] = homogen_test

    def run_test(self, 
                 test_name: str, 
                 samples: list[pd.Series|pd.DataFrame], 
                 alpha: float = 0.05, 
                 is_independent: bool = False) -> dict | None:
        """
        Run a homogeneity test for samples.
        Args:
            test_name: The name of the homogeneity test to run (must be registered in `_tests`).
            samples: Ssamples to test. Can be pandas Series, pandas DataFrame, or numpy arrays.
            alpha: Significance level for the statistical test.
            is_independent: True if the two samples are independent, False if paired/dependent.
        Returns:
            Dictionary with test results (statistic, p-value, decision), 
            or None if inputs are invalid or an error occurred.
        """
        if test_name not in self._tests:
            raise ValueError(f"Unknown test '{test_name}'. Available: {list(self._tests)}")

        clean_samples = []
        for i, data in enumerate(samples, 1):
            arr = data.dropna().to_numpy()
            if len(arr) == 0:
                raise ValueError(f"Sample {i} has no valid rows after removing NaN.")
            clean_samples.append(arr)

        try:
            result = self._tests[test_name].run(clean_samples, alpha, is_independent)
        except Exception as e:
            raise ValueError(f"'{test_name}' failed: {e}") from e

        if not result:
            raise ValueError(f"'{test_name}' returned no result.")
        return result