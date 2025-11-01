from .chi2_test import ChiSquaredGOFTest
from .chi2_2d_test import ChiSquared2DGOFTest
from .ks_test import KolmogorovSmirnovGOFTest
from .base_gof_test import BaseGOFTest

gof_tests: list[BaseGOFTest] = [
    KolmogorovSmirnovGOFTest,
    ChiSquaredGOFTest,
    ChiSquared2DGOFTest
]