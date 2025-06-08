from .chi2_test import ChiSquaredGOFTest
from .ks_test import KolmogorovSmirnovGOFTest

gof_tests = [
    KolmogorovSmirnovGOFTest,
    ChiSquaredGOFTest
]