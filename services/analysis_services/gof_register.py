from models.gofs.chi2_test import ChiSquaredGOFTest
from models.gofs.ks_test import KolmogorovSmirnovGOFTest
import numpy as np

class GOFService:
    _tests = {}

    @classmethod
    def register(cls, test):
        cls._tests[test.name()] = test

    @classmethod
    def run_tests(cls, data, dist, **kwargs):
        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        results = {}
        for name, test in cls._tests.items():
            try:
                results[name] = test.run(data_clean, dist, **kwargs)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results

GOFService.register(ChiSquaredGOFTest())
GOFService.register(KolmogorovSmirnovGOFTest())
