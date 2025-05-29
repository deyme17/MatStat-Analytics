from models.gofs.chi2_test import ChiSquaredGOFTest
from models.gofs.ks_test import KolmogorovSmirnovGOFTest
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

        :param test: instance of a class implementing BaseGOFTest
        """
        cls._tests[test.name()] = test

    @classmethod
    def run_tests(cls, data, dist, **kwargs) -> dict:
        """
        Run all registered GOF tests on given data and distribution.

        :param data: input data (pandas Series or numpy array)
        :param dist: fitted StatisticalDistribution object
        :param kwargs: optional parameters passed to each test
        :return: dictionary with test results by test name
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
GOFService.register(ChiSquaredGOFTest())
GOFService.register(KolmogorovSmirnovGOFTest())
