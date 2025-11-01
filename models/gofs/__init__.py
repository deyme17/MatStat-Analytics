from .chi2_test import ChiSquaredGOFTest
from .ks_test import KolmogorovSmirnovGOFTest
from .base_gof_test import BaseGOFTest

gof_tests: list[BaseGOFTest] = [
    KolmogorovSmirnovGOFTest,
    ChiSquaredGOFTest
]