from .chi2_test import ChiSquaredGOFTest
from .ks_test import KolmogorovSmirnovGOFTest
from .normal2d_chi2_test import Normal2DChi2GOFTest
from .base_gof_test import BaseGOFTest

gof_tests: list[BaseGOFTest] = [
    KolmogorovSmirnovGOFTest,
    ChiSquaredGOFTest
]