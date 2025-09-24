from .normal_homogen_test import NormalHomogenTest
from .wilcoxon_homogen_test import WilcoxonHomogenTest
from .mann_whitney_U_test import MannWhitneyUTest

homogens_tests = [
    NormalHomogenTest,
    WilcoxonHomogenTest,
    MannWhitneyUTest
]