from models.gofs import gof_tests
import numpy as np

class GOFService:
    """
    Service for managing and executing goodness-of-fit (GOF) tests.
    """
    _tests = {}  # registered tests by name

    @classmethod
    def register(cls, test):
        """
        Register a new GOF test instance.
        Args:
            test: instance of a class implementing BaseGOFTest
        """
        cls._tests[test.name()] = test

    @classmethod
    def run_tests(cls, data, dist, **kwargs) -> dict:
        """
        Run all registered GOF tests on given data and distribution.
        Args:
            data: input data (pandas Series or numpy array)
            dist: fitted StatisticalDistribution object
            kwargs: optional parameters passed to each test
        Return:
            dictionary with test results by test name
        """
        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        results = {}
        for name, test in cls._tests.items():
            try:
                results[name] = test.run(data_clean, dist, **kwargs)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results


# Register default tests
for gof_test in gof_tests:
    GOFService.register(gof_test())
