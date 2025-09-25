from .two_samples_tests.normal_homogen_test import NormalHomogenTest
from .two_samples_tests.wilcoxon_test import WilcoxonTest
from .two_samples_tests.mann_whitney_U_test import MannWhitneyUTest
from .two_samples_tests.rank_mean_diff_test import RankMeanDiffTest
from .two_samples_tests.smirnov_kolmogorov_test import SmirnovKolmogorovTest
from .two_samples_tests.signs_criterion_test import SignsCriterionTest

homogens_tests = [
    NormalHomogenTest,
    WilcoxonTest,
    MannWhitneyUTest,
    RankMeanDiffTest,
    SmirnovKolmogorovTest,
    SignsCriterionTest,
]